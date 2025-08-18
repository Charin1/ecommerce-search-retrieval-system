import React, { useState } from 'react';

export default function SearchBar({ onSearch, loading, initialQuery }) {
  const [q, setQ] = useState(initialQuery || '');

  const handleSearch = () => {
    if (q.trim()) {
      onSearch(q);
    }
  };

  return (
    <div className="flex gap-2 w-full">
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter') handleSearch(); }}
        className="flex-grow px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        placeholder="Search for products..."
      />
      <button
        disabled={loading}
        onClick={handleSearch}
        className="bg-indigo-600 text-white px-5 py-2 rounded-md font-semibold hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed"
      >
        {loading ? '...' : 'Search'}
      </button>
    </div>
  );
}