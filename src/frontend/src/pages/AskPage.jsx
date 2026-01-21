import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { askQuestion } from '../services/answerService';

const AskPage = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);

    const result = await askQuestion(query.trim());
    
    setLoading(false);

    if (result.success) {
      const answer = result.data;
      // Navigate to answer detail page
      navigate(`/answer/${answer.answer_id}`);
      setQuery(''); // Clear query after successful answer
    } else {
      setError(result.error || 'Failed to get answer');
    }
  };

  return (
    <div className="ask-page">
      <div className="ask-page-container">
        {/* Main content area */}
        <div className="ask-page-main">
          <div className="ask-page-main-content">
            <div className="ask-page-header">
              <h1>Ask a Question</h1>
            </div>

            <form onSubmit={handleSubmit} className="ask-form">
              <div className="form-group">
                <label htmlFor="query">Your Question</label>
                <textarea
                  id="query"
                  className="form-input form-textarea"
                  placeholder="Enter your question here..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={loading}
                  rows={4}
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !query.trim()}
              >
                {loading ? 'Generating Answer...' : 'Ask Question'}
              </button>
            </form>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {loading && (
              <div className="loading">
                Generating answer...
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AskPage;

