import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as noteService from '../services/noteService';
import NoteCard from './NoteCard';

const NoteList = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [viewMode, setViewMode] = useState('tiles'); // 'tiles' or 'list'
  const [selectedNotes, setSelectedNotes] = useState(new Set());
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

  const handleNoteDelete = (deletedNoteId) => {
    // Remove deleted note from local state instead of reloading all notes
    setNotes(notes.filter(note => note.id !== deletedNoteId));
    setSelectedNotes(prev => {
      const newSet = new Set(prev);
      newSet.delete(deletedNoteId);
      return newSet;
    });
  };

  const handleSelectNote = (noteId) => {
    setSelectedNotes(prev => {
      const newSet = new Set(prev);
      if (newSet.has(noteId)) {
        newSet.delete(noteId);
      } else {
        newSet.add(noteId);
      }
      return newSet;
    });
  };

  const handleSelectAll = () => {
    if (selectedNotes.size === notes.length) {
      setSelectedNotes(new Set());
    } else {
      setSelectedNotes(new Set(notes.map(note => note.id)));
    }
  };

  const handleBulkDelete = async () => {
    if (selectedNotes.size === 0) return;
    
    if (window.confirm(`Are you sure you want to delete ${selectedNotes.size} note(s)?`)) {
      const deletePromises = Array.from(selectedNotes).map(noteId => 
        noteService.deleteNote(noteId)
      );
      
      const results = await Promise.all(deletePromises);
      const failed = results.filter(r => !r.success);
      
      if (failed.length === 0) {
        setNotes(notes.filter(note => !selectedNotes.has(note.id)));
        setSelectedNotes(new Set());
      } else {
        alert(`Failed to delete ${failed.length} note(s)`);
        fetchNotes(); // Reload to sync state
      }
    }
  };

  const handleNoteClick = (noteId, e) => {
    // If clicking checkbox, don't navigate
    if (e.target.type === 'checkbox' || e.target.closest('.note-list-item-checkbox')) {
      return;
    }
    navigate(`/notes/${noteId}`);
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
        <div className="note-list-header-actions">
          <div className="view-toggle">
            <button
              className={`view-toggle-btn ${viewMode === 'tiles' ? 'active' : ''}`}
              onClick={() => setViewMode('tiles')}
              title="Tile view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="1" y="1" width="6" height="6" rx="1"/>
                <rect x="9" y="1" width="6" height="6" rx="1"/>
                <rect x="1" y="9" width="6" height="6" rx="1"/>
                <rect x="9" y="9" width="6" height="6" rx="1"/>
              </svg>
            </button>
            <button
              className={`view-toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
              title="List view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="1" y="2" width="14" height="2" rx="0.5"/>
                <rect x="1" y="7" width="14" height="2" rx="0.5"/>
                <rect x="1" y="12" width="14" height="2" rx="0.5"/>
              </svg>
            </button>
          </div>
          <button className="btn btn-primary" onClick={handleCreateNote}>
            Create New Note
          </button>
        </div>
      </div>
      
      {selectedNotes.size > 0 && (
        <div className="selection-bar">
          <span className="selection-bar-text">
            {selectedNotes.size} {selectedNotes.size === 1 ? 'note' : 'notes'} selected
          </span>
          <button className="btn btn-secondary btn-small" onClick={handleSelectAll}>
            {selectedNotes.size === notes.length ? 'Deselect All' : 'Select All'}
          </button>
          <button className="btn btn-danger btn-small" onClick={handleBulkDelete}>
            Delete Selected
          </button>
        </div>
      )}

      {notes.length === 0 ? (
        <div className="empty-state">
          <p>No notes yet. Create your first note!</p>
        </div>
      ) : viewMode === 'tiles' ? (
        <div className="note-grid">
          {notes.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              onDelete={handleNoteDelete}
              isSelected={selectedNotes.has(note.id)}
              onSelect={() => handleSelectNote(note.id)}
            />
          ))}
        </div>
      ) : (
        <div className="note-list-view">
          {notes.map((note) => (
            <div
              key={note.id}
              className={`note-list-item ${selectedNotes.has(note.id) ? 'selected' : ''}`}
              onClick={(e) => handleNoteClick(note.id, e)}
            >
              <input
                type="checkbox"
                className="note-list-item-checkbox"
                checked={selectedNotes.has(note.id)}
                onChange={() => handleSelectNote(note.id)}
                onClick={(e) => e.stopPropagation()}
              />
              <span className="note-list-item-title">{note.title}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NoteList;

