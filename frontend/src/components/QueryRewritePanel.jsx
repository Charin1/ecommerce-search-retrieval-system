import React from 'react';

export default function QueryRewritePanel({ rewrite }) {
  const hasFilters = rewrite.filters && Object.keys(rewrite.filters).length > 0;

  return (
    <div className="mt-4 bg-white p-4 rounded-lg shadow border flex flex-wrap gap-x-8 gap-y-4">
      <div>
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Rewritten Query</div>
        <div className="font-medium text-indigo-700">{rewrite.rewritten}</div>
      </div>
      {hasFilters && (
        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Extracted Filters</div>
          <div className="flex gap-2 mt-1">
            {Object.entries(rewrite.filters).map(([k, v]) => (
              <span key={k} className="bg-gray-100 px-2 py-1 rounded-md text-sm font-mono">
                {k}: {String(v)}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}