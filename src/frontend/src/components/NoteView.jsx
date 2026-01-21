import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';
import CitationTooltip from './CitationTooltip';

const NoteView = ({ noteId, onDelete }) => {
  const [note, setNote] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNote = async () => {
      setLoading(true);
      const result = await noteService.getNote(noteId);
      setLoading(false);

      if (result.success) {
        setNote(result.data);
      } else {
        setError(result.error || 'Failed to load note');
      }
    };
    fetchNote();
  }, [noteId]);

  const handleEdit = () => {
    navigate(`/notes/${noteId}/edit`);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      const result = await noteService.deleteNote(noteId);
      if (result.success) {
        if (onDelete) {
          onDelete();
        } else {
          navigate('/notes');
        }
      } else {
        alert(result.error || 'Failed to delete note');
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Parse citations from note content if references exist
  const parseContentWithCitations = (content, references) => {
    if (!references || Object.keys(references).length === 0) {
      // No references, return null to use default paragraph rendering
      return null;
    }

    // Parse citations similar to AnswerDetailPage
    const citationPattern = /\[(\d+)\]/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = citationPattern.exec(content)) !== null) {
      // Add text before citation
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.substring(lastIndex, match.index)
        });
      }

      // Add citation
      const citationNum = match[1];
      const reference = references[citationNum];
      if (reference) {
        parts.push({
          type: 'citation',
          citationNumber: citationNum,
          chunkText: reference.chunk_text,
          noteId: reference.note_id
        });
      } else {
        // Reference not found, just show as text
        parts.push({
          type: 'text',
          content: match[0]
        });
      }

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.substring(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content }];
  };

  const handleCitationClick = (noteId) => {
    navigate(`/notes/${noteId}`);
  };

  if (loading) {
    return <div className="loading">Loading note...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!note) {
    return <div className="error-message">Note not found</div>;
  }

  const contentParts = parseContentWithCitations(note.content, note.references);

  return (
    <div className="note-view">
      <div className="note-view-header">
        <h1 className="note-view-title">{note.title}</h1>
        <div className="note-view-actions">
          <button
            className="btn btn-primary"
            onClick={handleEdit}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      </div>
      <div className="note-view-meta">
        <span className="note-view-date">
          Updated: {formatDate(note.updated_at)}
        </span>
        {note.created_at !== note.updated_at && (
          <span className="note-view-date">
            Created: {formatDate(note.created_at)}
          </span>
        )}
      </div>
      <div className="note-view-content">
        {contentParts ? (
          // Render with citations
          contentParts.map((part, index) => {
            if (part.type === 'citation') {
              return (
                <CitationTooltip
                  key={index}
                  citationNumber={part.citationNumber}
                  chunkText={part.chunkText}
                  noteId={part.noteId}
                  onNavigate={handleCitationClick}
                />
              );
            } else {
              // Regular text - preserve newlines
              return <span key={index}>{part.content}</span>;
            }
          })
        ) : (
          // Default rendering without citations
          note.content.split('\n').map((paragraph, index) => (
            paragraph.trim() ? (
              <p key={index}>{paragraph}</p>
            ) : (
              <br key={index} />
            )
          ))
        )}
      </div>
    </div>
  );
};

export default NoteView;
