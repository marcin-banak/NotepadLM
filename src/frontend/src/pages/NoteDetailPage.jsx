import { useParams, useNavigate, useLocation } from 'react-router-dom';
import NoteForm from '../components/NoteForm';
import NoteView from '../components/NoteView';

const NoteDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isNew = id === 'new';
  const isEdit = location.pathname.includes('/edit');

  const handleSave = () => {
    // After saving, navigate to view mode
    if (!isNew) {
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

  return (
    <div className="note-detail-page">
      <NoteView noteId={parseInt(id)} onDelete={handleDelete} />
    </div>
  );
};

export default NoteDetailPage;

