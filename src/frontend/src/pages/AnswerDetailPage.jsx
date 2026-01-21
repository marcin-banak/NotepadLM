import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { getAnswer, deleteAnswer, convertAnswerToNote } from '../services/answerService';
import CitationTooltip from '../components/CitationTooltip';

const AnswerDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnswer = async () => {
      setLoading(true);
      const result = await getAnswer(id);
      setLoading(false);

      if (result.success) {
        setAnswer(result.data);
      } else {
        setError(result.error || 'Failed to load answer');
      }
    };

    if (id) {
      fetchAnswer();
    }
  }, [id]);

  // Parse citations from answer text
  const parseAnswerWithCitations = (answerText, references) => {
    const citationPattern = /\[(\d+)\]/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = citationPattern.exec(answerText)) !== null) {
      // Add text before citation
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: answerText.substring(lastIndex, match.index)
        });
      }

      // Add citation
      const citationNum = match[1];
      const reference = references[citationNum];
      if (reference) {
        parts.push({
          type: 'citation',
          citationNumber: citationNum,
          chunkText: reference.chunk_text,
          noteId: reference.note_id
        });
      } else {
        // Reference not found, just show as text
        parts.push({
          type: 'text',
          content: match[0]
        });
      }

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < answerText.length) {
      parts.push({
        type: 'text',
        content: answerText.substring(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content: answerText }];
  };

  const handleCitationClick = (noteId) => {
    const returnTo = location.state?.returnTo || `/answer/${id}`;
    navigate(`/notes/${noteId}`, { state: { returnTo } });
  };

  const handleBack = () => {
    const returnTo = location.state?.returnTo;
    if (returnTo) {
      navigate(returnTo);
    } else {
      navigate('/ask');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this answer?')) {
      return;
    }

    const result = await deleteAnswer(id);
    if (result.success) {
      navigate('/ask');
    } else {
      alert(result.error || 'Failed to delete answer');
    }
  };

  const handleConvertToNote = async () => {const result = await convertAnswerToNote(id);
    if (result.success) {
      navigate(`/notes/${result.data.note_id}`);
    } else {
      alert(result.error || 'Failed to convert answer to note');
    }
  };

  if (loading) {
    return (
      <div className="answer-detail-page">
        <div className="loading">Loading answer...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="answer-detail-page">
        <div className="error-message">{error}</div>
        <button className="btn btn-primary" onClick={handleBack}>
          Back to Ask
        </button>
      </div>
    );
  }

  if (!answer) {
    return (
      <div className="answer-detail-page">
        <div className="error-message">Answer not found</div>
        <button className="btn btn-primary" onClick={handleBack}>
          Back to Ask
        </button>
      </div>
    );
  }

  const answerParts = parseAnswerWithCitations(answer.answer_text, answer.references);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="answer-detail-page">
      <div className="answer-detail-header">
        <h1>{answer.title}</h1>
        <div className="answer-detail-actions">
          <button className="btn btn-primary" onClick={handleConvertToNote}>
            Add to Notes
          </button>
          <button className="btn btn-danger" onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>

      <div className="answer-detail-meta">
        <p className="answer-question"><strong>Question:</strong> {answer.question}</p>
        <p className="answer-date">Answered on {formatDate(answer.created_at)}</p>
      </div>

      <div className="answer-detail-content">
        {answerParts.map((part, index) => {
          if (part.type === 'citation') {
            return (
              <CitationTooltip
                key={index}
                citationNumber={part.citationNumber}
                chunkText={part.chunkText}
                noteId={part.noteId}
                onNavigate={handleCitationClick}
              />
            );
          } else {
            return <span key={index}>{part.content}</span>;
          }
        })}
      </div>
    </div>
  );
};

export default AnswerDetailPage;

