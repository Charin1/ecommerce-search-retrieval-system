from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers import InputExample
from torch.utils.data import DataLoader
import json
import os

def main():
    print("--- Starting Cross-Encoder Training ---")

    # --- 1. Configuration ---
    MODEL_NAME = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
    BATCH_SIZE = 16
    EPOCHS = 1
    MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models', 'cross-encoder')

    # --- 2. Load Model ---
    model = CrossEncoder(MODEL_NAME, num_labels=1)
    print(f"Loaded base model: {MODEL_NAME}")

    # --- 3. Load Dataset ---
    train_samples = []
    # --- THIS IS THE FIX ---
    data_path = os.path.join(os.path.dirname(__file__), 'cross_encoder_pairs_train.jsonl')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            train_samples.append(InputExample(texts=[item['query'], item['product_text']], label=float(item['label'])))
            
    print(f"Loaded {len(train_samples)} training samples.")

    # --- 4. Define Dataloader ---
    train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=BATCH_SIZE)

    # --- 5. Train the Model ---
    print(f"Starting training for {EPOCHS} epoch(s)...")
    model.fit(train_dataloader=train_dataloader,
              epochs=EPOCHS,
              warmup_steps=100)
    model.save(MODEL_SAVE_PATH)

    print(f"✅ Cross-Encoder model saved to {MODEL_SAVE_PATH}")
    print("--- Cross-Encoder Training Complete ---")

if __name__ == "__main__":
    main()