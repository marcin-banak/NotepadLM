import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SearchResultCard = ({ result }) => {
  const [showPreview, setShowPreview] = useState(false);
  const navigate = useNavigate();
  const { note, chunk_text, chunk_start, chunk_end, relevance_score } = result;

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatRelevanceScore = (score) => {
    return (score * 100).toFixed(1);
  };

  const highlightChunk = (content, chunkStart, chunkEnd) => {
    if (chunkStart === undefined || chunkEnd === undefined) {
      return content;
    }

    const before = content.substring(0, chunkStart);
    const chunk = content.substring(chunkStart, chunkEnd);
    const after = content.substring(chunkEnd);

    return (
      <>
        {before}
        <mark style={{ backgroundColor: '#fef08a', padding: '2px 4px', borderRadius: '3px' }}>
          {chunk}
        </mark>
        {after}
      </>
    );
  };

  const handleCardClick = () => {
    setShowPreview(!showPreview);
  };

  const handleViewNote = (e) => {
    e.stopPropagation();
    navigate(`/notes/${note.id}`);
  };

  return (
    <div className="search-result-card" onClick={handleCardClick}>
      <div className="search-result-header">
        <div className="search-result-title-section">
          <h3 className="search-result-title">{note.title}</h3>
          <span className="search-result-score">
            Relevance: {formatRelevanceScore(relevance_score)}%
          </span>
        </div>
        <button
          className="btn btn-small btn-primary"
          onClick={handleViewNote}
        >
          View Note
        </button>
      </div>
      
      {showPreview ? (
        <div className="search-result-preview">
          <div className="search-result-chunk">
            <strong>Relevant note:</strong>
            <div className="chunk-text">
              {highlightChunk(note.content, chunk_start, chunk_end)}
            </div>
          </div>
        </div>
      ) : (
        <div className="search-result-snippet">
          <p>{chunk_text || note.content.substring(0, 200)}...</p>
        </div>
      )}
      
      <div className="search-result-footer">
        <span className="search-result-date">
          Updated: {formatDate(note.updated_at)}
        </span>
        <span className="search-result-hint">
          {showPreview ? 'Click to collapse' : 'Click to preview'}
        </span>
      </div>
    </div>
  );
};

export default SearchResultCard;

