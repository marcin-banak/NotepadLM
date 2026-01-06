import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';

const NoteCard = ({ note, onDelete }) => {
  const navigate = useNavigate();

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this note?')) {
      const result = await noteService.deleteNote(note.id);
      if (result.success) {
        onDelete();
      } else {
        alert(result.error || 'Failed to delete note');
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="note-card" onClick={() => navigate(`/notes/${note.id}`)}>
      <div className="note-card-header">
        <h3 className="note-card-title">{note.title}</h3>
        <div className="note-card-actions">
          <button
            className="btn btn-small btn-secondary"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/notes/${note.id}`);
            }}
          >
            Edit
          </button>
          <button
            className="btn btn-small btn-danger"
            onClick={handleDelete}
          >
            Delete
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

