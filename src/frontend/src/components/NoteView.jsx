import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';

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

  if (loading) {
    return <div className="loading">Loading note...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!note) {
    return <div className="error-message">Note not found</div>;
  }

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
        {note.content.split('\n').map((paragraph, index) => (
          paragraph.trim() ? (
            <p key={index}>{paragraph}</p>
          ) : (
            <br key={index} />
          )
        ))}
      </div>
    </div>
  );
};

export default NoteView;
