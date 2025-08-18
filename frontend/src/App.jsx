import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import ResultsSection from './components/ResultsSection';
import Sidebar from './components/Sidebar';
import Controls from './components/Controls';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [query, setQuery] = useState('cheap wireless headphones under 100 for gym');
  const [searchResponse, setSearchResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // UI State
  const [config, setConfig] = useState({ rewrite_on: true, rerank_on: true });
  const [selectedFilters, setSelectedFilters] = useState({});
  const [sortBy, setSortBy] = useState('relevance');

  const doSearch = async (q, filters, sort) => {
    if (!q) return;
    setLoading(true);
    setSearchResponse(null);

    try {
      const resp = await axios.post(`${API_URL}/api/v1/search`, {
        query: q,
        rewrite_on: config.rewrite_on,
        rerank_on: config.rerank_on,
        top_k: 40,
        filters: filters,
        sort_by: sort,
      });
      setSearchResponse(resp.data);
    } catch (e) {
      console.error(e);
      alert('Search failed. Is the backend running and accessible?');
    } finally {
      setLoading(false);
    }
  };
  
  // Effect to trigger search when filters or sort order change
  useEffect(() => {
    // Don't search on initial load if there's no query
    if (query) {
      doSearch(query, selectedFilters, sortBy);
    }
  }, [selectedFilters, sortBy, config]);

  const handleSearch = (q) => {
    setQuery(q);
    // Reset filters and sort on new search
    setSelectedFilters({});
    setSortBy('relevance');
    doSearch(q, {}, 'relevance');
  };

  const handleFilterChange = (facetName, value) => {
    setSelectedFilters(prevFilters => {
      const currentValues = prevFilters[facetName] || [];
      const newValues = currentValues.includes(value)
        ? currentValues.filter(v => v !== value) // Toggle off
        : [...currentValues, value]; // Toggle on
      
      // For price, we only allow one selection
      if (facetName === 'Price') {
        return { ...prevFilters, [facetName]: newValues.slice(-1) };
      }
      return { ...prevFilters, [facetName]: newValues };
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <h1 className="text-2xl font-bold text-gray-800">E-commerce Search & Retrieve System</h1>
            <div className="w-full sm:w-auto">
              <SearchBar onSearch={handleSearch} loading={loading} initialQuery={query} />
            </div>
            <Controls config={config} setConfig={setConfig} />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col lg:flex-row gap-8">
          <aside className="w-full lg:w-1/4">
            <Sidebar
              facets={searchResponse?.facets}
              selectedFilters={selectedFilters}
              onFilterChange={handleFilterChange}
            />
          </aside>
          <div className="flex-1">
            <ResultsSection
              response={searchResponse}
              loading={loading}
              sortBy={sortBy}
              setSortBy={setSortBy}
            />
          </div>
        </div>
      </main>
    </div>
  );
}