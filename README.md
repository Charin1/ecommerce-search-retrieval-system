# E-commerce Search & Retrieve System

This project is a full-stack, production-ready search engine for e-commerce. It implements an advanced NLP-powered pipeline to understand complex user queries, retrieve relevant products from a catalog, and rank them intelligently using a state-of-the-art two-stage architecture.

### Core Features

-   **Advanced Query Understanding**: Utilizes a pre-trained **Named Entity Recognition (NER)** model to parse messy user queries, extracting structured filters like price and brand for more accurate results.
-   **Two-Stage Search Funnel**:
    -   **Stage 1 (Retrieval)**: A fine-tuned **Bi-Encoder** (Sentence Transformer) and a **FAISS** vector index scan the entire catalog in milliseconds to find hundreds of semantically relevant candidates.
    -   **Stage 2 (Reranking)**: A powerful **Cross-Encoder** model performs a deep analysis on the candidates, reranking them with high precision to ensure the top results are the most relevant.
-   **Feature-Rich UI**: A modern React frontend provides a complete search experience with faceted filtering (by brand, price), sorting options, and a clean, responsive layout.
-   **Full-Stack & Containerized**: A robust **FastAPI** backend serves the ML models, and the entire application is containerized with **Docker** for easy, reproducible deployment.

---

### Tech Stack

| Backend          | Frontend         | Training & Machine Learning      |
| ---------------- | ---------------- | -------------------------------- |
| Python 3.11      | React            | PyTorch                          |
| FastAPI          | Vite             | Hugging Face `transformers`      |
| Uvicorn          | Tailwind CSS     | `sentence-transformers`          |
| Docker           | Axios            | FAISS (for vector search)        |
|                  |                  | Pandas & Scikit-learn            |

---

### Project Structure

```
ecommerce-search-retrieve-system/
├── backend/                # FastAPI application
│   ├── app/
│   ├── models/             # <-- Populated by training scripts
│   └── index/              # <-- Populated by training scripts
├── frontend/               # React UI application
├── training/               # Scripts for data prep, training, and indexing
│   └── data/               # Raw sample data
├── venv/                   # <-- Unified Python virtual environment
├── docker-compose.yml      # Docker orchestrator
├── requirements.txt        # Master list of all Python dependencies
└── README.md               # This file
```

---

## Getting Started: Step-by-Step Instructions

Follow these steps to set up the environment, train the models, and run the full application.

### Prerequisites

-   **Python 3.11**: This project is tested and stable with Python 3.11.
-   **Docker Desktop**: Required for the containerized deployment.
-   **Node.js v16+**: Required for the frontend build process within Docker.

### Phase 1: The Training Pipeline (One-Time Setup)

This phase prepares the data, trains the ML models, and builds the search index.

**1. Setup a Unified Python Environment**

We use a single virtual environment to ensure consistency between training and serving.

```bash
# Navigate to the project's root directory
cd ecommerce-search-retrieve-system/

# Create a virtual environment using Python 3.11
python3.11 -m venv venv

# Activate the environment
source venv/bin/activate

# Install all required dependencies
pip install -r requirements.txt
```

**2. Run the Training Scripts in Sequence**

With the environment active, run the following scripts from the project's root directory.

```bash
# Step A: Prepare the data for training
python training/data_prep.py

# Step B: Train the Bi-Encoder (retriever) model
python training/train_bi_encoder.py

# Step C: Train the Cross-Encoder (reranker) model
python training/train_cross_encoder.py

# Step D: Build the FAISS index with the new bi-encoder
python training/build_index.py
```

After this, your `backend/models/` and `backend/index/` directories will be populated with the necessary ML artifacts.

### Phase 2: Running the Application

You have two options to run the application.

#### Option A: Run with Docker (Recommended)

This is the easiest and most reliable way to run the full stack.

```bash
# From the project's root directory
docker-compose up --build
```

-   **Frontend UI**: Access at `http://localhost:5173`
-   **Backend API Docs**: Access at `http://localhost:8000/docs`

#### Option B: Run Natively (For Development)

This is useful if you want to actively develop the backend or frontend separately.

**1. Run the Backend Server:**
```bash
# Make sure your unified venv is active
# source venv/bin/activate

# Navigate to the backend directory
cd backend/

# Run the Uvicorn server with auto-reload
uvicorn app.main:app --reload
```
The backend will be running on `http://localhost:8000`.

**2. Run the Frontend Server (in a separate terminal):**
```bash
# Navigate to the frontend directory
cd frontend/

# Install Node.js dependencies
npm install

# Start the Vite development server
npm run dev
```
The frontend will be running on `http://localhost:5173`.

---

## Future Upgrades & Roadmap

This project provides a strong foundation. Here are potential next steps to make it even more powerful:

### Tier 1: Core Model Improvements

-   **Fine-Tune a Custom E-commerce NER Model**: Train a model to recognize specific entities like `[ATTRIBUTE]`, `[COLOR]`, and `[PRODUCT_TYPE]` for more precise query understanding.
-   **Implement Hard Negative Mining**: Improve the bi-encoder's accuracy by training it on "hard negatives" (semantically similar but incorrect products) instead of random ones.
-   **Upgrade to a Learning to Rank (LTR) Model**: Replace the cross-encoder with a model (like XGBoost) that can rank products based on a mix of text relevance, business metrics (price, rating), and popularity.

### Tier 2: Production-Hardening & MLOps

-   **Migrate to a Vector Database**: Replace the local FAISS index with a managed vector database like Pinecone, Weaviate, or Milvus for real-time updates and metadata filtering at scale.
-   **Implement an A/B Testing Framework**: Build a feature in the backend to route a small percentage of traffic to new experimental models and measure their impact on business metrics (CTR, conversion).
-   **Automate the Training Pipeline (CI/CD for ML)**: Use a tool like GitHub Actions to automatically retrain and evaluate models when new data is available.

### Tier 3: Advanced Features

-   **Deep Personalization**: Incorporate user history (past clicks, purchases, brand affinities) as features into the reranking model to provide personalized results for each user.
-   **Multimodal Search**: Use a model like CLIP to create combined text-and-image embeddings, enabling search that understands visual concepts and paving the way for image-based search.
-   **Generative Search Summaries**: Use an LLM to generate a conversational summary of the top search results, providing a direct answer to the user's query.
