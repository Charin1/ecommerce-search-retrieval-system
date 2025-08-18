import React from 'react';

export default function Controls({ config, setConfig }) {
  return (
    <div className="flex items-center gap-4 bg-white p-3 rounded-lg shadow-sm border">
      <label className="flex items-center text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={config.rewrite_on}
          onChange={(e) => setConfig({ ...config, rewrite_on: e.target.checked })}
          className="ml-2 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
        <span className="ml-2 text-gray-700">Query Rewrite</span>
      </label>
      <label className="flex items-center text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={config.rerank_on}
          onChange={(e) => setConfig({ ...config, rerank_on: e.target.checked })}
          className="ml-2 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
        <span className="ml-2 text-gray-700">Neural Rerank</span>
      </label>
    </div>
  );
}