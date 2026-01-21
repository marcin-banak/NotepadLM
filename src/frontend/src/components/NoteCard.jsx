import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';

const NoteCard = ({ note, onDelete, isSelected = false, onSelect }) => {
  const navigate = useNavigate();

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this note?')) {
      const result = await noteService.deleteNote(note.id);
      if (result.success) {
        onDelete(note.id);
      } else {
        alert(result.error || 'Failed to delete note');
      }
    }
  };

  const handleSelect = (e) => {
    e.stopPropagation();
    if (onSelect) {
      onSelect();
    }
  };

  const handleCardClick = (e) => {
    // Don't navigate if clicking checkbox or buttons
    if (e.target.type === 'checkbox' || e.target.closest('button') || e.target.closest('.note-card-checkbox')) {
      return;
    }
    navigate(`/notes/${note.id}`);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`note-card ${isSelected ? 'selected' : ''}`} onClick={handleCardClick}>
      {onSelect && (
        <div className="note-card-checkbox" onClick={handleSelect}>
          <input
            type="checkbox"
            checked={isSelected}
            onChange={handleSelect}
            onClick={(e) => e.stopPropagation()}
            style={{ width: '18px', height: '18px', cursor: 'pointer' }}
          />
        </div>
      )}
      <div className="note-card-header">
        <h3 className="note-card-title">{note.title}</h3>
        <div className="note-card-actions">
          <button
            className="btn btn-small btn-primary"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/notes/${note.id}/edit`);
            }}
          >
            Edit
          </button>
        </div>
      </div>
      <p className="note-card-content">{note.content}</p>
      <div className="note-card-footer">
        <span className="note-card-date">
          Updated: {formatDate(note.updated_at)}
        </span>
      </div>
    </div>
  );
};

export default NoteCard;

