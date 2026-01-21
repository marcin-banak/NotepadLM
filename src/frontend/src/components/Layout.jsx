import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="layout app-shell">
      <Navbar />
      <main className="app-content">
        <div className="content-inner">{children}</div>
      </main>
    </div>
  );
};

export default Layout;

