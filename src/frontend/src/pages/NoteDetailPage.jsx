import { useParams, useNavigate } from 'react-router-dom';
import NoteForm from '../components/NoteForm';

const NoteDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isNew = id === 'new';

  const handleSave = () => {
    navigate('/notes');
  };

  const handleCancel = () => {
    navigate('/notes');
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

