import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';
import NoteCard from './NoteCard';

const NoteList = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchNotes = async () => {
    setLoading(true);
    setError('');
    const result = await noteService.getNotes();
    setLoading(false);

    if (result.success) {
      setNotes(result.data);
    } else {
      setError(result.error || 'Failed to load notes');
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleCreateNote = () => {
    navigate('/notes/new');
  };

  if (loading) {
    return <div className="loading">Loading notes...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="note-list">
      <div className="note-list-header">
        <h1>My Notes</h1>
        <button className="btn btn-primary" onClick={handleCreateNote}>
          Create New Note
        </button>
      </div>
      {notes.length === 0 ? (
        <div className="empty-state">
          <p>No notes yet. Create your first note!</p>
        </div>
      ) : (
        <div className="note-grid">
          {notes.map((note) => (
            <NoteCard key={note.id} note={note} onDelete={fetchNotes} />
          ))}
        </div>
      )}
    </div>
  );
};

export default NoteList;

