import faiss
import numpy as np
import json
import re
import os
import time
from collections import Counter
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Any
from transformers import pipeline

class SearchService:
    def __init__(self, data_path: str, bi_encoder_path: str, cross_encoder_path: str, faiss_index_path: str):
        print("--- Initializing Search Service ---")

        # --- THIS IS THE FIX ---
        # Build robust paths relative to THIS file's location, not the current working directory.
        # This makes the service runnable from anywhere.
        SERVICE_ROOT = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(os.path.join(SERVICE_ROOT, '..', '..', '..'))

        # Construct the correct, absolute paths
        abs_data_path = os.path.join(PROJECT_ROOT, 'training', 'data', 'products.jsonl')
        abs_bi_encoder_path = os.path.join(PROJECT_ROOT, 'backend', 'models', 'bi-encoder')
        abs_cross_encoder_path = os.path.join(PROJECT_ROOT, 'backend', 'models', 'cross-encoder')
        abs_faiss_index_path = os.path.join(PROJECT_ROOT, 'backend', 'index', 'products.faiss')
        
        # Now, use these absolute paths to load everything
        self.products = self._load_products(abs_data_path)
        self.product_map = {p['product_id']: p for p in self.products}
        
        print("Loading models...")
        self.bi_encoder = SentenceTransformer(abs_bi_encoder_path, device='mps')
        self.cross_encoder = CrossEncoder(abs_cross_encoder_path, device='mps')
        
        print("Loading NER pipeline...")
        self.ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True, device=0)
        
        print("Loading FAISS index...")
        self.faiss_index = faiss.read_index(abs_faiss_index_path)
        print("--- Search Service Initialized Successfully ---")

    def _load_products(self, path: str) -> List[Dict[str, Any]]:
        """Loads product data from a .jsonl file."""
        if not os.path.exists(path):
            # The error message now shows the absolute path, which is much better for debugging
            raise FileNotFoundError(f"Product data not found at the absolute path: {path}")
        
        products = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                products.append(json.loads(line))
        return products

    # ... (The rest of the file: understand_query, _calculate_facets, search) ...
    # ... (NO OTHER CHANGES ARE NEEDED IN THE REST OF THE FILE) ...
    def understand_query(self, query: str) -> Dict[str, Any]:
        entities = self.ner_pipeline(query)
        rewritten_parts = []
        filters = {}
        processed_indices = set()
        price_match = re.search(r'(under|less than|below)\s*\$?(\d+\.?\d*)', query, flags=re.IGNORECASE)
        if price_match:
            filters['price_max'] = float(price_match.group(2))
            for i in range(price_match.start(), price_match.end()):
                processed_indices.add(i)
        for entity in entities:
            if entity['entity_group'] == 'ORG':
                filters.setdefault('brand', []).append(entity['word'])
            elif entity['entity_group'] == 'MISC':
                rewritten_parts.append(entity['word'])
            for i in range(entity['start'], entity['end']):
                processed_indices.add(i)
        words = query.split()
        current_pos = 0
        unprocessed_words = []
        for word in words:
            word_start = query.find(word, current_pos)
            word_end = word_start + len(word)
            if (word_start + word_end) // 2 not in processed_indices:
                unprocessed_words.append(word)
            current_pos = word_end
        final_rewritten_parts = rewritten_parts + unprocessed_words
        rewritten_query = " ".join(sorted(set(final_rewritten_parts), key=final_rewritten_parts.index))
        return {"rewritten": rewritten_query.strip(), "filters": filters}

    def _calculate_facets(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not products:
            return []
        brand_counts = Counter(p['brand'] for p in products if p.get('brand'))
        brand_facet = {
            "name": "Brand",
            "buckets": [{"value": brand, "count": count} for brand, count in brand_counts.most_common(10)]
        }
        prices = [p['price'] for p in products if p.get('price')]
        price_buckets = [
            {"value": "0-50", "count": sum(1 for p in prices if 0 <= p < 50)},
            {"value": "50-100", "count": sum(1 for p in prices if 50 <= p < 100)},
            {"value": "100-250", "count": sum(1 for p in prices if 100 <= p < 250)},
            {"value": "250+", "count": sum(1 for p in prices if p >= 250)},
        ]
        price_facet = {
            "name": "Price",
            "buckets": [b for b in price_buckets if b['count'] > 0]
        }
        return [brand_facet, price_facet]

    def search(self, query: str, top_k: int, rewrite_on: bool, rerank_on: bool, filters: Dict = None, sort_by: str = 'relevance') -> Dict[str, Any]:
        start_time = time.time()
        rewritten_info = self.understand_query(query) if rewrite_on else {"rewritten": query, "filters": {}}
        search_query = rewritten_info['rewritten'] or query
        query_embedding = self.bi_encoder.encode([search_query], convert_to_numpy=True).astype('float32')
        num_candidates = 200
        distances, ids = self.faiss_index.search(query_embedding, num_candidates)
        retrieved_pids = [str(pid) for pid in ids[0] if pid != -1]
        candidate_products = [self.product_map[pid] for pid in retrieved_pids if pid in self.product_map]
        facets = self._calculate_facets(candidate_products)
        if filters:
            if 'Brand' in filters and filters['Brand']:
                candidate_products = [p for p in candidate_products if p.get('brand') in filters['Brand']]
            if 'Price' in filters and filters['Price']:
                min_price, max_price = filters['Price'][0].split('-')
                max_price = float(max_price) if max_price != '+' else float('inf')
                candidate_products = [p for p in candidate_products if p.get('price') and float(min_price) <= p['price'] < max_price]
        if rerank_on and sort_by == 'relevance':
            if candidate_products:
                pairs = [[search_query, f"{p['title']}. {p.get('description', '')}"] for p in candidate_products]
                scores = self.cross_encoder.predict(pairs)
                for product, score in zip(candidate_products, scores):
                    product['score'] = float(score)
                final_products = sorted(candidate_products, key=lambda x: x['score'], reverse=True)
            else:
                final_products = []
        else:
            if sort_by == 'price_asc':
                final_products = sorted(candidate_products, key=lambda x: x.get('price', float('inf')))
            elif sort_by == 'price_desc':
                final_products = sorted(candidate_products, key=lambda x: x.get('price', float('-inf')), reverse=True)
            else:
                final_products = candidate_products
        end_time = time.time()
        return {
            "original_query": query,
            "rewritten_query": rewritten_info,
            "results": final_products[:top_k],
            "facets": facets,
            "search_time": round(end_time - start_time, 2)
        }