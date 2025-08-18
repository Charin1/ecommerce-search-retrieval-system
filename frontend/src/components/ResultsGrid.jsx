import React from 'react';
const ProductCard = ({ product }) => (
<div className="bg-white shadow-md rounded-lg p-4 border flex flex-col transition-transform duration-200 hover:scale-105">
<img
src={product.image_url || 'https://via.placeholder.com/200x150?text=No+Image'}
alt={product.title}
className="w-full h-40 object-contain mb-3"
/>
<div className="flex-grow">
<div className="font-semibold text-sm text-gray-800 mb-1 line-clamp-2">{product.title}</div>
<div className="text-xs text-gray-500 mb-2">{product.brand}</div>
</div>
<div className="mt-2 flex items-center justify-between">
<div className="text-lg font-bold text-gray-900">${product.price}</div>
{product.rating && <div className="text-xs text-gray-600 bg-yellow-100 px-2 py-1 rounded">⭐ {product.rating}</div>}
</div>
</div>
);
export default function ResultsGrid({ results, loading }) {
if (loading) {
return <div className="text-center mt-10">Loading results...</div>;
}
if (results.length === 0) {
return <div className="text-center mt-10 text-gray-500">No results to display.</div>;
}
return (
<div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
{results.map((r) => (
<ProductCard key={r.product_id} product={r} />
))}
</div>
);
}