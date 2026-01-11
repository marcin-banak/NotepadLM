import { useState } from 'react';
import { searchNotes } from '../services/noteService';
import SearchResultCard from '../components/SearchResultCard';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);

    const result = await searchNotes(query.trim());
    
    setLoading(false);

    if (result.success) {
      // Sort results by relevance_score descending
      const sortedResults = result.data.results.sort(
        (a, b) => b.relevance_score - a.relevance_score
      );
      setResults(sortedResults);
    } else {
      setError(result.error || 'Failed to search notes');
      setResults([]);
    }
  };

  return (
    <div className="search-page">
      <div className="search-page-header">
        <h1>Search Notes</h1>
        <p className="search-page-subtitle">
          Find relevant notes by entering a search query
        </p>
      </div>

      <form onSubmit={handleSearch} className="search-form">
        <div className="form-group">
          <input
            type="text"
            className="form-input"
            placeholder="Enter your search query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
        </div>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !query.trim()}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          Searching...
        </div>
      )}

      {!loading && hasSearched && results.length === 0 && !error && (
        <div className="empty-state">
          <p>No notes found matching your query.</p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div className="search-results">
          <div className="search-results-header">
            <h2>Search Results ({results.length})</h2>
          </div>
          <div className="search-results-list">
            {results.map((result, index) => (
              <SearchResultCard key={`${result.note.id}-${index}`} result={result} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPage;

