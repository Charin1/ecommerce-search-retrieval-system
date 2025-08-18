import React from 'react';

const ProductCard = ({ product }) => (
  <div className="bg-white rounded-lg shadow border overflow-hidden transition-transform duration-200 hover:shadow-xl hover:-translate-y-1">
    <img
      src={product.image_url || 'https://via.placeholder.com/200x150?text=No+Image'}
      alt={product.title}
      className="w-full h-48 object-contain bg-gray-50 p-2"
    />
    <div className="p-4 flex flex-col flex-grow">
      <div className="flex-grow mb-2">
        <div className="text-xs text-gray-500 mb-1">{product.brand}</div>
        <h3 className="font-semibold text-sm text-gray-800 line-clamp-2">{product.title}</h3>
      </div>
      <div className="flex items-center justify-between mt-2">
        <div className="text-xl font-bold text-gray-900">${product.price?.toFixed(2)}</div>
        {product.rating && <div className="text-sm text-gray-600 bg-yellow-100 px-2 py-1 rounded-full">⭐ {product.rating}</div>}
      </div>
    </div>
  </div>
);

const SkeletonCard = () => (
  <div className="bg-white rounded-lg shadow border overflow-hidden animate-pulse">
    <div className="w-full h-48 bg-gray-200"></div>
    <div className="p-4">
      <div className="h-3 bg-gray-200 rounded w-1/4 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
      <div className="flex items-center justify-between">
        <div className="h-6 bg-gray-200 rounded w-1/3"></div>
        <div className="h-6 bg-gray-200 rounded w-1/4"></div>
      </div>
    </div>
  </div>
);

const SortDropdown = ({ sortBy, setSortBy }) => (
  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    className="border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
  >
    <option value="relevance">Relevance</option>
    <option value="price_asc">Price: Low to High</option>
    <option value="price_desc">Price: High to Low</option>
  </select>
);

export default function ResultsSection({ response, loading, sortBy, setSortBy }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 9 }).map((_, i) => <SkeletonCard key={i} />)}
      </div>
    );
  }

  if (!response) {
    return <div className="text-center py-10 text-gray-500">Enter a query to start searching.</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4 bg-white p-3 rounded-lg shadow-sm">
        <div className="text-sm text-gray-700">
          Found <span className="font-bold">{response.results.length}</span> results
          {response.search_time && ` in ${response.search_time}s`}
        </div>
        <SortDropdown sortBy={sortBy} setSortBy={setSortBy} />
      </div>

      {response.results.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {response.results.map((r) => <ProductCard key={r.product_id} product={r} />)}
        </div>
      ) : (
        <div className="text-center py-10 text-gray-500">No results found. Try adjusting your search or filters.</div>
      )}
    </div>
  );
}