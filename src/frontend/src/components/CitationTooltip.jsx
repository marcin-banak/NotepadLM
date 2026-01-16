import { useState } from 'react';

const CitationTooltip = ({ citationNumber, chunkText, noteId, onNavigate }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  const handleClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (onNavigate && noteId) {
      onNavigate(noteId);
    }
  };

  return (
    <span className="citation-wrapper">
      <span
        className="citation-link"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        onClick={handleClick}
      >
        [{citationNumber}]
      </span>
      {showTooltip && (
        <div className="citation-tooltip">
          <div className="citation-tooltip-content">
            <p className="citation-tooltip-text">{chunkText}</p>
            {noteId && (
              <button
                className="citation-tooltip-link"
                onClick={handleClick}
              >
                View source note →
              </button>
            )}
          </div>
        </div>
      )}
    </span>
  );
};

export default CitationTooltip;

