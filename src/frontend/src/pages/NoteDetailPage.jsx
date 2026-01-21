import { useParams, useNavigate, useLocation } from 'react-router-dom';
import NoteForm from '../components/NoteForm';
import NoteView from '../components/NoteView';

const NoteDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  // Check pathname first to handle routing edge cases
  const isNew = location.pathname === '/notes/new' || id === 'new';
  const isEdit = location.pathname.includes('/edit');
  
  // Debug logging
  console.log('NoteDetailPage render:', { id, pathname: location.pathname, isNew, isEdit });

  const handleSave = (noteData) => {
    console.log('NoteDetailPage handleSave called with:', noteData, 'isNew:', isNew);
    // After saving, navigate to view mode
    if (!isNew) {
      // Editing existing note - go back to view mode
      console.log('Editing note, navigating to:', `/notes/${id}`);
      navigate(`/notes/${id}`, { replace: true });
    } else {
      // For new notes, navigate to the created note's detail page
      console.log('Creating new note, noteData:', noteData);
      if (noteData && noteData.id !== undefined && noteData.id !== null) {
        const noteId = typeof noteData.id === 'number' ? noteData.id : parseInt(noteData.id);
        console.log('Parsed noteId:', noteId);
        if (!isNaN(noteId) && noteId > 0) {
          // Use replace to avoid back button issues
          console.log('Navigating to:', `/notes/${noteId}`);
          navigate(`/notes/${noteId}`, { replace: true });
        } else {
          console.error('Invalid noteId:', noteId);
          // Invalid ID - go to notes list
          navigate('/notes', { replace: true });
        }
      } else {
        console.error('No ID in noteData:', noteData);
        // No ID - go to notes list
        const returnTo = location.state?.returnTo;
        if (returnTo) {
          navigate(returnTo, { replace: true });
        } else {
          navigate('/notes', { replace: true });
        }
      }
    }
  };

  const handleCancel = () => {
    if (!isNew) {
      // If editing, go back to view mode
      navigate(`/notes/${id}`);
    } else {
      const returnTo = location.state?.returnTo;
      if (returnTo) {
        navigate(returnTo);
      } else {
        navigate('/notes');
      }
    }
  };

  const handleDelete = () => {
    navigate('/notes');
  };

  // First check if we're creating or editing - this must come first!
  if (isNew || isEdit) {
    return (
      <div className="note-detail-page">
        <h1>{isNew ? 'Create New Note' : 'Edit Note'}</h1>
        <NoteForm
          noteId={isNew ? null : parseInt(id)}
          onSave={handleSave}
          onCancel={handleCancel}
        />
      </div>
    );
  }

  // If we get here, we should have a valid numeric id for viewing
  if (!id) {
    return (
      <div className="note-detail-page">
        <div className="error-message">Invalid note ID</div>
        <button className="btn btn-primary" onClick={() => navigate('/notes')}>
          Back to Notes
        </button>
      </div>
    );
  }

  const noteId = parseInt(id);
  
  if (isNaN(noteId) || noteId <= 0) {
    return (
      <div className="note-detail-page">
        <div className="error-message">Invalid note ID</div>
        <button className="btn btn-primary" onClick={() => navigate('/notes')}>
          Back to Notes
        </button>
      </div>
    );
  }

  return (
    <div className="note-detail-page">
      <NoteView noteId={noteId} onDelete={handleDelete} />
    </div>
  );
};

export default NoteDetailPage;

