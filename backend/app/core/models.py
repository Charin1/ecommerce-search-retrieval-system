from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ... (SearchRequest remains the same) ...
class SearchRequest(BaseModel):
    query: str
    top_k: int = 20
    rewrite_on: bool = True
    rerank_on: bool = True
    # NEW: Add filters and sort_by to the request
    filters: Optional[Dict[str, Any]] = None
    sort_by: Optional[str] = 'relevance'

# ... (RewrittenQuery and ProductResult remain the same) ...
class RewrittenQuery(BaseModel):
    rewritten: str
    filters: Dict[str, Any]

class ProductResult(BaseModel):
    product_id: str
    title: str
    brand: Optional[str]
    price: Optional[float]
    rating: Optional[float]
    image_url: Optional[str]
    description: Optional[str]
    score: Optional[float] = None

# NEW: Define a model for the facets
class Facet(BaseModel):
    name: str
    buckets: List[Dict[str, Any]]

class SearchResponse(BaseModel):
    original_query: str
    rewritten_query: Optional[RewrittenQuery]
    results: List[ProductResult]
    # NEW: Add facets to the response
    facets: List[Facet] = []