import json
import pandas as pd
import os
from tqdm import tqdm
from sklearn.model_selection import train_test_split

def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def create_examples(df, all_products):
    bi_encoder_triplets = []
    cross_encoder_pairs = []
    
    # --- FIX: Add a counter for skipped clicks ---
    skipped_clicks_count = 0

    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        query = row['raw_query']
        positive_pid = row['product_id']
        
        # --- THIS IS THE FIX ---
        # 1. Search for the product
        product_search_result = all_products[all_products['product_id'] == positive_pid]
        
        # 2. Check if the search returned any results
        if not product_search_result.empty:
            # 3. Only if the product exists, proceed with creating examples
            positive_product = product_search_result.iloc[0]
            positive_text = positive_product['text']
            
            cross_encoder_pairs.append({"query": query, "product_text": positive_text, "label": 1, "query_id": row['query_id']})
            
            negative_sample = all_products[all_products['product_id'] != positive_pid].sample(1).iloc[0]
            negative_text = negative_sample['text']

            bi_encoder_triplets.append({"query": query, "positive": positive_text, "negative": negative_text})
            cross_encoder_pairs.append({"query": query, "product_text": negative_text, "label": 0, "query_id": row['query_id']})
        else:
            # If the product_id from the click was not found in products.jsonl, skip it.
            skipped_clicks_count += 1
            
    # --- FIX: Report how many clicks were skipped ---
    if skipped_clicks_count > 0:
        print(f"\n⚠️  Warning: Skipped {skipped_clicks_count} click records because their product_id was not found in the product catalog.")
        
    return bi_encoder_triplets, cross_encoder_pairs

def main():
    print("--- Starting Data Preparation with Train/Test Split ---")
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    
    products_df = load_jsonl(os.path.join(DATA_DIR, 'products.jsonl'))
    queries_df = load_jsonl(os.path.join(DATA_DIR, 'queries.jsonl'))
    clicks_df = load_jsonl(os.path.join(DATA_DIR, 'clicks.jsonl'))

    merged_df = pd.merge(clicks_df, queries_df, on='query_id')
    positive_interactions = merged_df[merged_df['clicked'] == True].copy()
    
    train_df, test_df = train_test_split(positive_interactions, test_size=0.2, random_state=42)

    all_products = products_df.copy()
    all_products['text'] = all_products['title'] + ". " + all_products['description'].fillna('')
    
    print("Generating training examples...")
    bi_train, cross_train = create_examples(train_df, all_products)
    
    print("Generating testing examples...")
    _, cross_test = create_examples(test_df, all_products)

    output_dir = os.path.dirname(__file__)
    for name, data in [
        ('bi_encoder_triplets_train.jsonl', bi_train),
        ('cross_encoder_pairs_train.jsonl', cross_train),
        ('cross_encoder_pairs_test.jsonl', cross_test)
    ]:
        path = os.path.join(output_dir, name)
        with open(path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
        print(f"✅ Saved {len(data)} examples to {path}")

if __name__ == "__main__":
    main()