import React from 'react';

const Facet = ({ facet, selectedValues, onFilterChange }) => (
  <div className="py-4 border-b border-gray-200">
    <h3 className="font-semibold mb-2">{facet.name}</h3>
    <ul className="space-y-1">
      {facet.buckets.map(bucket => (
        <li key={bucket.value}>
          <label className="flex items-center text-sm cursor-pointer">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              checked={selectedValues.includes(bucket.value)}
              onChange={() => onFilterChange(facet.name, bucket.value)}
            />
            <span className="ml-2 text-gray-700">{bucket.value}</span>
            <span className="ml-auto text-xs text-gray-500">{bucket.count}</span>
          </label>
        </li>
      ))}
    </ul>
  </div>
);

export default function Sidebar({ facets, selectedFilters, onFilterChange }) {
  if (!facets || facets.length === 0) {
    return (
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-bold mb-4">Filters</h2>
        <p className="text-sm text-gray-500">Perform a search to see available filters.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-bold mb-2">Filters</h2>
      {facets.map(facet => (
        <Facet
          key={facet.name}
          facet={facet}
          selectedValues={selectedFilters[facet.name] || []}
          onFilterChange={onFilterChange}
        />
      ))}
    </div>
  );
}