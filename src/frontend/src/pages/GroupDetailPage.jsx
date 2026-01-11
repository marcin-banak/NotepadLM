import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import * as groupService from '../services/groupService';
import NoteCard from '../components/NoteCard';

const GroupDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGroup = async () => {
      setLoading(true);
      setError('');
      const result = await groupService.getGroup(id);
      setLoading(false);

      if (result.success) {
        setGroup(result.data);
      } else {
        setError(result.error || 'Failed to load group');
      }
    };

    if (id) {
      fetchGroup();
    }
  }, [id]);

  const handleNoteDelete = () => {
    // Refresh group data after note deletion
    const fetchGroup = async () => {
      const result = await groupService.getGroup(id);
      if (result.success) {
        setGroup(result.data);
      }
    };
    fetchGroup();
  };

  if (loading) {
    return <div className="loading">Loading group...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!group) {
    return <div className="error-message">Group not found</div>;
  }

  const notes = group.notes || [];

  return (
    <div className="note-detail-page">
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/groups')}
          style={{ marginBottom: 'var(--spacing-md)' }}
        >
          ← Back to Groups
        </button>
        <h1>{group.summary || `Group ${group.id}`}</h1>
        {group.summary && (
          <p style={{ color: 'var(--text-secondary)', marginTop: 'var(--spacing-md)' }}>
            {group.summary}
          </p>
        )}
      </div>

      <div>
        <h2 style={{ marginBottom: 'var(--spacing-lg)', color: 'var(--text-primary)' }}>
          Notes in this group ({notes.length})
        </h2>
        {notes.length === 0 ? (
          <div className="empty-state">
            <p>No notes in this group yet.</p>
          </div>
        ) : (
          <div className="note-grid">
            {notes.map((note) => (
              <NoteCard key={note.id} note={note} onDelete={handleNoteDelete} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default GroupDetailPage;

