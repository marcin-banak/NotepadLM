import { useState, useEffect } from 'react';
import * as noteService from '../services/noteService';

const NoteForm = ({ noteId, onSave, onCancel }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingNote, setLoadingNote] = useState(!!noteId);

  useEffect(() => {
    if (noteId) {
      const fetchNote = async () => {
        setLoadingNote(true);
        const result = await noteService.getNote(noteId);
        setLoadingNote(false);

        if (result.success) {
          setTitle(result.data.title);
          setContent(result.data.content);
        } else {
          setError(result.error || 'Failed to load note');
        }
      };
      fetchNote();
    }
  }, [noteId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const noteData = {
      title,
      content,
    };

    const result = noteId
      ? await noteService.updateNote(noteId, noteData)
      : await noteService.createNote(noteData);

    setLoading(false);

    if (result.success) {
      onSave(result.data);
    } else {
      setError(result.error || 'Failed to save note');
    }
  };

  if (loadingNote) {
    return <div className="loading">Loading note...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="note-form">
      {error && <div className="error-message">{error}</div>}
      <div className="form-group">
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          disabled={loading}
          className="form-input"
        />
      </div>
      <div className="form-group">
        <label htmlFor="content">Content</label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          disabled={loading}
          rows={15}
          className="form-textarea"
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : noteId ? 'Update Note' : 'Create Note'}
        </button>
        {onCancel && (
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default NoteForm;

