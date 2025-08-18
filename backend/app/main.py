from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- 1. IMPORT THIS
from app.api import search
from app.services.search_service import SearchService
import os

# This is a placeholder for a more robust startup/shutdown event handler
# In a real app, you would load the service during the startup event.
search_service = SearchService(
    data_path=None, # These paths are now calculated inside the service
    bi_encoder_path=None,
    cross_encoder_path=None,
    faiss_index_path=None
)

app = FastAPI(
    title="E-commerce Search API",
    description="API for semantic product search and reranking."
)

# Store the service in the app state to be accessible in path operations
app.state.search_service = search_service

# --- 2. ADD THE CORS MIDDLEWARE ---
# This is the crucial part that fixes the "Search failed" error.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. For production, you'd list your frontend's domain.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.).
    allow_headers=["*"],  # Allows all headers.
)

# --- Routers ---
app.include_router(search.router, prefix="/api/v1", tags=["Search"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}