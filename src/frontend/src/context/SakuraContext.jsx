import { createContext, useContext, useState, useEffect } from 'react';

const SakuraContext = createContext();

export const useSakura = () => {
  const context = useContext(SakuraContext);
  if (!context) {
    throw new Error('useSakura must be used within a SakuraProvider');
  }
  return context;
};

export const SakuraProvider = ({ children }) => {
  const [isEnabled, setIsEnabled] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('sakura-enabled');
      return saved === 'true';
    }
    return false;
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('sakura-enabled', isEnabled.toString());
    }
  }, [isEnabled]);

  const toggleSakura = () => {
    setIsEnabled(prev => !prev);
  };

  return (
    <SakuraContext.Provider value={{ isEnabled, toggleSakura }}>
      {children}
    </SakuraContext.Provider>
  );
};
