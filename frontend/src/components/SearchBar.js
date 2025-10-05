import React, { useState, useRef, useEffect, useMemo } from 'react';

const SearchBar = ({ searchTerm, onSearchChange, isSearching }) => {
  const [isFocused, setIsFocused] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const inputRef = useRef(null);

  const quickSearches = useMemo(() => [
    'microgravity', 'gene expression', 'muscle atrophy', 'arabidopsis',
    'cardiac function', 'bone density', 'spaceflight', 'ISS'
  ], []);

  useEffect(() => {
    if (searchTerm.length > 1) {
      const filtered = quickSearches.filter(term => 
        term.toLowerCase().includes(searchTerm.toLowerCase()) &&
        term.toLowerCase() !== searchTerm.toLowerCase()
      );
      setSuggestions(filtered.slice(0, 4));
    } else {
      setSuggestions([]);
    }
  }, [searchTerm, quickSearches]);

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      inputRef.current?.blur();
      setIsFocused(false);
    }
  };

  return (
    <div className="relative max-w-4xl mx-auto">
      <div className="glass-morphism cyber-glow relative">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            {isSearching ? (
              <div className="w-5 h-5 border-2 border-cosmic-purple/30 border-t-cosmic-purple rounded-full animate-spin"></div>
            ) : (
              <svg className="h-5 w-5 text-cosmic-purple" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            )}
          </div>
          <input
            ref={inputRef}
            type="text"
            className="block w-full pl-12 pr-16 py-4 bg-transparent text-star-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cosmic-purple focus:border-transparent rounded-lg text-lg"
            placeholder="Search NASA bioscience experiments, organisms, missions..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setTimeout(() => setIsFocused(false), 200)}
            onKeyDown={handleKeyDown}
          />
          {searchTerm && (
            <button
              onClick={() => onSearchChange('')}
              className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-white transition-colors"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>
      
      {/* Search Suggestions */}
      {isFocused && (suggestions.length > 0 || (!searchTerm && quickSearches.length > 0)) && (
        <div className="absolute top-full left-0 right-0 mt-2 glass-morphism rounded-lg p-4 z-50 shadow-2xl">
          <h4 className="text-cosmic-purple text-sm font-semibold mb-3">
            {searchTerm ? 'Suggestions' : 'Quick Searches'}
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {(searchTerm ? suggestions : quickSearches.slice(0, 8)).map((term) => (
              <button
                key={term}
                onClick={() => {
                  onSearchChange(term);
                  inputRef.current?.blur();
                }}
                className="text-left px-3 py-2 rounded-lg bg-slate-800/50 hover:bg-cosmic-purple/20 text-star-white/80 hover:text-star-white text-sm transition-all duration-200 hover:scale-105"
              >
                {term}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Active Search Indicator */}
      {searchTerm && (
        <div className="absolute -bottom-8 left-0 right-0">
          <div className="flex items-center justify-center space-x-2 text-sm">
            <span className="text-cosmic-purple">Filtering by:</span>
            <span className="bg-cosmic-purple/20 text-cosmic-purple px-3 py-1 rounded-full font-mono">
              "{searchTerm}"
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;