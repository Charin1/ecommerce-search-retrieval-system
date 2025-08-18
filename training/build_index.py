import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def main():
    print("--- Starting FAISS Index Build ---")

    # --- 1. Configuration ---
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models', 'bi-encoder')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'products.jsonl')
    INDEX_SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'backend', 'index')
    INDEX_FILE = os.path.join(INDEX_SAVE_DIR, 'products.faiss')
    
    # Ensure the save directory exists
    os.makedirs(INDEX_SAVE_DIR, exist_ok=True)

    # --- 2. Load Model and Data ---
    print("Loading bi-encoder model...")
    model = SentenceTransformer(MODEL_PATH)
    
    print("Loading product data...")
    products = load_jsonl(DATA_PATH)
    
    # We need a consistent mapping from index position to product_id
    product_ids = [p['product_id'] for p in products]
    
    # Create text representation for each product
    product_texts = [f"{p['title']}. {p.get('description', '')}" for p in products]

    # --- 3. Encode Products ---
    print("Encoding all products... (This may take a while)")
    embeddings = model.encode(product_texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype('float32') # FAISS requires float32
    
    embedding_dim = embeddings.shape[1]
    print(f"Created {len(embeddings)} embeddings of dimension {embedding_dim}.")

    # --- 4. Build and Save FAISS Index ---
    index = faiss.IndexFlatL2(embedding_dim)  # Using a simple L2 distance index
    index = faiss.IndexIDMap(index) # Map from FAISS index position to our product_id
    
    # FAISS requires integer IDs, so we create a mapping
    ids_array = np.array([int(pid) for pid in product_ids])

    index.add_with_ids(embeddings, ids_array)
    
    print(f"Index built. Total entries: {index.ntotal}")
    
    faiss.write_index(index, INDEX_FILE)
    print(f"✅ FAISS index saved to {INDEX_FILE}")
    print("--- FAISS Index Build Complete ---")

if __name__ == "__main__":
    main()