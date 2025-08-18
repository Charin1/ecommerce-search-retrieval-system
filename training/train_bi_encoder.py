from sentence_transformers import SentenceTransformer, InputExample, losses, models
from torch.utils.data import DataLoader
import json
import os

def main():
    print("--- Starting Bi-Encoder Training ---")
    # --- 1. Configuration ---
    MODEL_NAME = 'distilbert-base-uncased'
    BATCH_SIZE = 16
    EPOCHS = 1
    MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models', 'bi-encoder')

    # --- 2. Load Model ---
    word_embedding_model = models.Transformer(MODEL_NAME, max_seq_length=256)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

    print(f"Loaded base model: {MODEL_NAME}")

    # --- 3. Load Dataset ---
    train_samples = []
    # --- THIS IS THE FIX ---
    data_path = os.path.join(os.path.dirname(__file__), 'bi_encoder_triplets_train.jsonl')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            train_samples.append(InputExample(texts=[item['query'], item['positive'], item['negative']]))

    print(f"Loaded {len(train_samples)} training samples.")

    # --- 4. Define Dataloader and Loss ---
    train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=BATCH_SIZE)
    train_loss = losses.MultipleNegativesRankingLoss(model=model)

    # --- 5. Train the Model ---
    print(f"Starting training for {EPOCHS} epoch(s)...")
    model.fit(train_objectives=[(train_dataloader, train_loss)],
              epochs=EPOCHS,
              warmup_steps=100,
              output_path=MODEL_SAVE_PATH,
              show_progress_bar=True)
              
    print(f"✅ Bi-Encoder model saved to {MODEL_SAVE_PATH}")
    print("--- Bi-Encoder Training Complete ---")

if __name__ == "__main__":
    main()