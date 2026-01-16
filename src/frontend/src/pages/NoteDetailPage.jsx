import { useParams, useNavigate, useLocation } from 'react-router-dom';
import NoteForm from '../components/NoteForm';

const NoteDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isNew = id === 'new';

  const handleSave = () => {
    const returnTo = location.state?.returnTo;
    if (returnTo) {
      navigate(returnTo);
    } else {
      navigate('/notes');
    }
  };

  const handleCancel = () => {
    const returnTo = location.state?.returnTo;
    if (returnTo) {
      navigate(returnTo);
    } else {
      navigate('/notes');
    }
  };

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
};

export default NoteDetailPage;

