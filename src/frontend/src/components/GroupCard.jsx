import { useNavigate } from 'react-router-dom';
import * as groupService from '../services/groupService';

const GroupCard = ({ group, onDelete }) => {
  const navigate = useNavigate();

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this group?')) {
      const result = await groupService.deleteGroup(group.id);
      if (result.success) {
        onDelete();
      } else {
        alert(result.error || 'Failed to delete group');
      }
    }
  };

  const noteCount = group.notes ? group.notes.length : 0;

  return (
    <div className="note-card" onClick={() => navigate(`/groups/${group.id}`)}>
      <div className="note-card-header">
        <h3 className="note-card-title">
          {group.summary || `Group ${group.id}`}
        </h3>
        <div className="note-card-actions">
          <button
            className="btn btn-small btn-secondary"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/groups/${group.id}`);
            }}
          >
            View
          </button>
          <button
            className="btn btn-small btn-danger"
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      </div>
      <p className="note-card-content">
        {group.summary || 'No summary available'}
      </p>
      <div className="note-card-footer">
        <span className="note-card-date">
          {noteCount} {noteCount === 1 ? 'note' : 'notes'}
        </span>
      </div>
    </div>
  );
};

export default GroupCard;

