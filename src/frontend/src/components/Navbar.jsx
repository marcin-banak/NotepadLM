import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { isAuthenticated, logout, user } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          NotepadLM
        </Link>
        <div className="navbar-menu">
          {isAuthenticated ? (
            <>
              <Link to="/notes" className="navbar-link">
                Notes
              </Link>
              <Link to="/groups" className="navbar-link">
                Groups
              </Link>
              <Link to="/search" className="navbar-link">
                Search
              </Link>
              {user && <span className="navbar-user">Hello, {user.name}</span>}
              <button onClick={handleLogout} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Login
              </Link>
              <Link to="/register" className="btn btn-primary">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

