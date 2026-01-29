import { useEffect, useRef } from 'react';
import Navbar from './Navbar';
import { useSakura } from '../context/SakuraContext';

const Layout = ({ children }) => {
  const { isEnabled } = useSakura();
  const sakuraInstanceRef = useRef(null);

  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;

    let isMounted = true;
    let SakuraClass = null;

    const loadSakura = () => {
      if (SakuraClass) return Promise.resolve(SakuraClass);

      return new Promise((resolve, reject) => {
        // Check if window.Sakura is available (loaded via script tag in index.html)
        if (typeof window !== 'undefined' && window.Sakura && typeof window.Sakura === 'function') {
          console.log('Using window.Sakura from script tag');
          SakuraClass = window.Sakura;
          resolve(SakuraClass);
          return;
        }

        // Wait for script to load (script tag in index.html loads before React)
        let attempts = 0;
        const maxAttempts = 100; // 10 seconds max wait (100 * 100ms)
        
        const checkSakura = () => {
          attempts++;
          
          if (typeof window !== 'undefined' && window.Sakura && typeof window.Sakura === 'function') {
            console.log('Sakura loaded from window:', window.Sakura);
            SakuraClass = window.Sakura;
            resolve(SakuraClass);
            return;
          }
          
          if (attempts >= maxAttempts) {
            reject(new Error('Sakura not found in window object. Make sure sakura.min.js is loaded in index.html'));
            return;
          }
          
          // Check again after a short delay
          setTimeout(checkSakura, 100);
        };
        
        // Start checking
        checkSakura();
      });
    };

    const initSakura = async () => {
      console.log('initSakura called, isEnabled:', isEnabled);
      
      if (!isEnabled) {
        // Stop sakura-js if disabled
        if (sakuraInstanceRef.current && sakuraInstanceRef.current.stop) {
          console.log('Stopping sakura');
          sakuraInstanceRef.current.stop(false);
          sakuraInstanceRef.current = null;
        }
        return;
      }

      // Wait for sakura-background container to be available in DOM
      const checkAndInit = () => {
        if (!isMounted) return;

        const sakuraContainer = document.getElementById('sakura-background');
        console.log('Checking for #sakura-background element:', sakuraContainer);
        
        if (!sakuraContainer) {
          // Retry on next frame
          requestAnimationFrame(checkAndInit);
          return;
        }

        // Element exists, proceed with initialization
        loadSakura().then((Sakura) => {
          if (!isMounted || !Sakura) {
            console.error('Sakura class not available or component unmounted');
            return;
          }

          // Initialize or restart sakura-js
          if (!sakuraInstanceRef.current) {
            try {
              console.log('Initializing sakura with selector #sakura-background');
              sakuraInstanceRef.current = new Sakura('#sakura-background', {
                colors: [
                  {
                    gradientColorStart: '#B45309',
                    gradientColorEnd:   '#78350F',
                    gradientColorDegree: 120,
                  },
                  {
                    gradientColorStart: '#B45309',
                    gradientColorEnd:   '#78350F',
                    gradientColorDegree: 120,
                  },
                  {
                    gradientColorStart: '#9A3412',
                    gradientColorEnd:   '#D97706',
                    gradientColorDegree: 120,
                  }
                ],
                delay: 50,
                fallSpeed: 1,
                minSize: 10,
                maxSize: 20,
              });
              console.log('Sakura instance created:', sakuraInstanceRef.current);
            } catch (error) {
              console.error('Error creating sakura instance:', error);
              console.error('Error details:', {
                message: error.message,
                stack: error.stack,
                Sakura: Sakura,
                selector: '#sakura-background'
              });
            }
          } else if (sakuraInstanceRef.current && sakuraInstanceRef.current.start) {
            // Restart if instance exists
            console.log('Restarting sakura');
            sakuraInstanceRef.current.start();
          }
        }).catch((error) => {
          console.error('Failed to load sakura:', error);
        });
      };

      // Start checking on next frame to ensure DOM is ready
      requestAnimationFrame(checkAndInit);
    };

    initSakura();

    // Cleanup on unmount
    return () => {
      isMounted = false;
      if (sakuraInstanceRef.current && sakuraInstanceRef.current.stop) {
        sakuraInstanceRef.current.stop(false);
        sakuraInstanceRef.current = null;
      }
    };
  }, [isEnabled]);

  return (
    <>
      {/* Fixed background container for sakura petals - always viewport size */}
      <div id="sakura-background"></div>
      <div className="layout app-shell">
        <Navbar />
        <main className="app-content">
          <div className="content-inner">{children}</div>
        </main>
      </div>
    </>
  );
};

export default Layout;

