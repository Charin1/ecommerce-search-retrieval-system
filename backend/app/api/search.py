from fastapi import APIRouter, Depends, Request
from app.core.models import SearchRequest, SearchResponse
from app.services.search_service import SearchService

# --- FIX: Create an instance of the APIRouter ---
router = APIRouter()

def get_search_service(request: Request) -> SearchService:
    """Dependency to get the search service instance from the app state."""
    # This is a placeholder for a more robust dependency injection system
    # In a real app, you might use a global state or a dependency management library.
    # For now, we assume the service is initialized and attached in main.py
    return request.app.state.search_service

# --- FIX: Use the router instance as a decorator for your endpoint ---
@router.post("/search", response_model=SearchResponse)
def perform_search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service)
):
    """
    Performs a search request using the configured pipeline.
    """
    # The service is now loaded once at startup and accessed via dependency injection
    results = service.search(
        query=request.query,
        top_k=request.top_k,
        rewrite_on=request.rewrite_on,
        rerank_on=request.rerank_on,
        filters=request.filters,
        sort_by=request.sort_by
    )
    return results