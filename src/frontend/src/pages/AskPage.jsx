import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { askQuestion, getUserAnswers, getAnswer } from '../services/answerService';
import AnswerCard from '../components/AnswerCard';
import CitationTooltip from '../components/CitationTooltip';

const AskPage = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentAnswer, setCurrentAnswer] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [loadingAnswers, setLoadingAnswers] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnswers = async () => {
      setLoadingAnswers(true);
      const result = await getUserAnswers();
      setLoadingAnswers(false);
      if (result.success) {
        setAnswers(result.data);
      }
    };
    fetchAnswers();
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);

    const result = await askQuestion(query.trim());
    
    setLoading(false);

    if (result.success) {
      const answer = result.data;
      // Fetch full answer details
      const fullAnswerResult = await getAnswer(answer.answer_id);
      if (fullAnswerResult.success) {
        setCurrentAnswer(fullAnswerResult.data);
        // Refresh answers list
        const answersResult = await getUserAnswers();
        if (answersResult.success) {
          setAnswers(answersResult.data);
        }
      }
      setQuery(''); // Clear query after successful answer
    } else {
      setError(result.error || 'Failed to get answer');
    }
  };

  const handleCitationClick = (noteId) => {
    if (currentAnswer) {
      navigate(`/notes/${noteId}`, { state: { returnTo: `/answer/${currentAnswer.id}` } });
    } else {
      navigate(`/notes/${noteId}`);
    }
  };

  const handleAnswerSelect = async (answer) => {
    // Fetch full answer details
    const result = await getAnswer(answer.id);
    if (result.success) {
      setCurrentAnswer(result.data);
    }
  };

  const answerParts = currentAnswer
    ? parseAnswerWithCitations(currentAnswer.answer_text, currentAnswer.references)
    : [];

  return (
    <div className="ask-page">
      <div className="ask-page-container">
        {/* Left sidebar with answer list */}
        <div className="ask-page-sidebar">
          <h2>Your Answers</h2>
          {loadingAnswers ? (
            <p className="empty-state-text">Loading...</p>
          ) : answers.length === 0 ? (
            <p className="empty-state-text">No answers yet. Ask a question to get started!</p>
          ) : (
            <div className="answer-list">
              {answers.map((answer) => (
                <AnswerCard
                  key={answer.id}
                  answer={{
                    id: answer.id,
                    title: answer.title,
                    question: answer.question,
                    created_at: answer.created_at
                  }}
                  onSelect={handleAnswerSelect}
                />
              ))}
            </div>
          )}
        </div>

        {/* Main content area */}
        <div className="ask-page-main">
          <div className="ask-page-main-content">
            <div className="ask-page-header">
              <h1>Ask a Question</h1>
              <p className="ask-page-subtitle">
                Ask questions about your notes and get AI-powered answers with citations
              </p>
            </div>

            {/* Query form - only show if no current answer */}
            {!currentAnswer && (
              <form onSubmit={handleSubmit} className="ask-form">
                <div className="form-group">
                  <label htmlFor="query">Your Question</label>
                  <textarea
                    id="query"
                    className="form-input form-textarea"
                    placeholder="Enter your question here..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={loading}
                    rows={4}
                  />
                </div>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading || !query.trim()}
                >
                  {loading ? 'Generating Answer...' : 'Ask Question'}
                </button>
              </form>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {loading && (
              <div className="loading">
                Generating answer...
              </div>
            )}

            {/* Display current answer */}
            {currentAnswer && (
              <div className="answer-display">
                <div className="answer-header">
                  <h2>{currentAnswer.title}</h2>
                  <button
                    className="btn btn-secondary"
                    onClick={() => {
                      setCurrentAnswer(null);
                      setQuery('');
                    }}
                  >
                    Ask New Question
                  </button>
                </div>
                <div className="answer-meta">
                  <p className="answer-question"><strong>Question:</strong> {currentAnswer.question}</p>
                </div>
                <div className="answer-content">
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
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AskPage;

