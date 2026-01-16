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
        <div 
          className="citation-tooltip"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <div className="citation-tooltip-content">
            <p className="citation-tooltip-text">{chunkText}</p>
          </div>
        </div>
      )}
    </span>
  );
};

export default CitationTooltip;

