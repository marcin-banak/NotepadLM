import { useNavigate } from 'react-router-dom';

const AnswerCard = ({ answer, onSelect, compact = false, isActive = false }) => {
  const navigate = useNavigate();

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleClick = () => {
    if (onSelect) {
      onSelect(answer);
    } else {
      navigate(`/answer/${answer.id}`);
    }
  };

  if (compact) {
    return (
      <div className={`answer-card answer-card-compact ${isActive ? 'active' : ''}`} onClick={handleClick}>
        <div className="answer-card-title-compact">{answer.title}</div>
      </div>
    );
  }

  return (
    <div className="answer-card" onClick={handleClick}>
      <div className="answer-card-header">
        <h3 className="answer-card-title">{answer.title}</h3>
      </div>
      <p className="answer-card-question">{answer.question}</p>
      <div className="answer-card-footer">
        <span className="answer-card-date">
          {formatDate(answer.created_at)}
        </span>
      </div>
    </div>
  );
};

export default AnswerCard;

