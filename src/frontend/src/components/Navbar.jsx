import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getUserAnswers } from '../services/answerService';
import AnswerCard from './AnswerCard';

const Navbar = () => {
  const { isAuthenticated, logout, user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [answers, setAnswers] = useState([]);
  const [loadingAnswers, setLoadingAnswers] = useState(false);
  const isAskPage = location.pathname === '/ask';
  const isAnswerPage = location.pathname.startsWith('/answer/');

  useEffect(() => {
    if (isAuthenticated && (isAskPage || isAnswerPage)) {
      const fetchAnswers = async () => {
        setLoadingAnswers(true);
        const result = await getUserAnswers();
        setLoadingAnswers(false);
        if (result.success) {
          setAnswers(result.data);
        }
      };
      fetchAnswers();
    }
  }, [isAuthenticated, isAskPage, isAnswerPage]);

  const handleLogout = () => {
    logout();
  };

  const handleAnswerSelect = (answer) => {
    navigate(`/answer/${answer.id}`);
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-inner">
        <Link to="/" className="sidebar-brand">
          NotepadLM
        </Link>

        <nav className="sidebar-nav" aria-label="Primary navigation">
          {isAuthenticated ? (
            <>
              <Link to="/notes" className="sidebar-link">
                Notes
              </Link>
              <Link to="/groups" className="sidebar-link">
                Groups
              </Link>
              <Link to="/search" className="sidebar-link">
                Search
              </Link>
              <Link to="/ask" className="sidebar-link">
                Ask
              </Link>
            </>
          ) : (
            <>
              <Link to="/login" className="sidebar-link">
                Login
              </Link>
              <Link to="/register" className="sidebar-link sidebar-link-accent">
                Register
              </Link>
            </>
          )}
        </nav>

        {isAuthenticated && (isAskPage || isAnswerPage) && (
          <>
            <div className="sidebar-divider"></div>
            <div className="sidebar-answers">
              {loadingAnswers ? (
                <p className="sidebar-answers-empty">Loading...</p>
              ) : answers.length === 0 ? (
                <p className="sidebar-answers-empty">No answers yet.</p>
              ) : (
                <div className="sidebar-answers-list">
                  {answers.map((answer) => {
                    const currentAnswerId = location.pathname.startsWith('/answer/') 
                      ? location.pathname.split('/answer/')[1] 
                      : null;
                    return (
                      <AnswerCard
                        key={answer.id}
                        answer={{
                          id: answer.id,
                          title: answer.title,
                          question: answer.question,
                          created_at: answer.created_at
                        }}
                        onSelect={handleAnswerSelect}
                        compact={true}
                        isActive={currentAnswerId === String(answer.id)}
                      />
                    );
                  })}
                </div>
              )}
            </div>
          </>
        )}

        <div className="sidebar-footer">
          {isAuthenticated ? (
            <>
              {user && <div className="sidebar-user">Hello, {user.name}</div>}
              <button onClick={handleLogout} className="btn btn-secondary btn-small">
                Logout
              </button>
            </>
          ) : (
            <div className="sidebar-hint">Sign in to access your notes.</div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Navbar;

