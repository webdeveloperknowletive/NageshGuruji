'use client';
import { useStore } from '@/context/StoreContext';

export default function MobileDrawer() {
  const { drawerOpen, setDrawerOpen, openTracking, openContact } = useStore();

  const handleLinkClick = () => {
    setDrawerOpen(false);
  };

  const handleTrackClick = () => {
    setDrawerOpen(false);
    openTracking();
  };

  const handleContactClick = () => {
    setDrawerOpen(false);
    openContact();
  };

  return (
    <>
      <div
        className={`drawer-overlay${drawerOpen ? ' show' : ''}`}
        id="drawerOverlay"
        onClick={() => setDrawerOpen(false)}
      />
      <aside className={`mobile-drawer${drawerOpen ? ' open' : ''}`} id="mobileDrawer">
        <button
          className="drawer-close"
          id="drawerClose"
          aria-label="Close"
          onClick={() => setDrawerOpen(false)}
        >
          ✕
        </button>
        <ul>
          <li><a href="#top" onClick={handleLinkClick}>Home</a></li>
          <li><a href="#shop" onClick={handleLinkClick}>Shop</a></li>
          <li><a href="#puja" onClick={handleLinkClick}>Puja Services</a></li>
          <li><a href="#jyotish" onClick={handleLinkClick}>Jyotish</a></li>
          <li><a href="#rudraksha" onClick={handleLinkClick}>Rudraksha</a></li>
          <li><a href="#ratna" onClick={handleLinkClick}>Ratna</a></li>
          <li><a href="#yantra" onClick={handleLinkClick}>Yantra</a></li>
          <li><a href="#bracelets" onClick={handleLinkClick}>Bracelets</a></li>
          <li><a href="#about" onClick={handleLinkClick}>About Guruji</a></li>
          <li><a href="#blog" onClick={handleLinkClick}>Blog</a></li>
          <li>
            <button
              type="button"
              onClick={handleTrackClick}
              style={{ background: 'none', border: 'none', color: 'var(--gold-lt)', font: 'inherit', cursor: 'pointer', padding: 0, textAlign: 'left', width: '100%' }}
            >
              📦 Track Order
            </button>
          </li>
          <li>
            <button
              type="button"
              onClick={handleContactClick}
              style={{ background: 'none', border: 'none', color: 'inherit', font: 'inherit', cursor: 'pointer', padding: 0, textAlign: 'left', width: '100%' }}
            >
              Contact Seva
            </button>
          </li>
        </ul>
      </aside>
    </>
  );
}
