'use client';
import { useStore } from '@/context/StoreContext';

export default function Navbar({ logo }) {
  const { cartCount, wishlist, setCartOpen, setWishOpen, setSearchOpen, setDrawerOpen, openTracking, openContact } = useStore();
  const logoSrc = logo || '/swami-guruji-logo-cropped.jpg';

  const openCart = () => { setCartOpen(true); setWishOpen(false); setSearchOpen(false); setDrawerOpen(false); };
  const openWish = () => { setWishOpen(true); setCartOpen(false); setSearchOpen(false); setDrawerOpen(false); };
  const openSearch = () => { setSearchOpen(true); setCartOpen(false); setWishOpen(false); setDrawerOpen(false); };

  return (
    <nav className="nav" id="top">
      <a href="#top" className="brand" aria-label="Swami Guruji">
        <img
          src={logoSrc}
          alt="Swami Guruji"
          className="brand-logo-img"
          onError={(e) => { e.currentTarget.onerror = null; e.currentTarget.src = '/swami-guruji-logo-cropped.jpg'; }}
        />
      </a>

      <ul className="nav-links">
        <li><a href="#shop">Shop</a></li>
        <li><a href="#puja">Puja Services</a></li>
        <li><a href="#jyotish">Jyotish</a></li>
        <li><a href="#rudraksha">Rudraksha</a></li>
        <li><a href="#ratna">Ratna</a></li>
        <li><a href="#yantra">Yantra</a></li>
        <li><a href="#bracelets">Bracelets</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#blog">Blog</a></li>
        <li>
          <button
            type="button"
            onClick={openContact}
            style={{ background: 'none', border: 'none', color: 'inherit', font: 'inherit', cursor: 'pointer', padding: 0 }}
          >
            Contact
          </button>
        </li>
      </ul>

      <div className="nav-actions">
        <button
          type="button"
          onClick={() => openTracking()}
          style={{
            background: 'none',
            border: '1px solid rgba(224, 176, 74, 0.35)',
            borderRadius: '20px',
            color: 'var(--gold-lt)',
            fontSize: '11px',
            padding: '5px 12px',
            cursor: 'pointer',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}
          title="Track an order by Order Number"
        >
          <span>📦</span> Track Order
        </button>
        <button className="icon-btn" id="searchBtn" aria-label="Search" onClick={openSearch}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>
          </svg>
        </button>
        <button className="icon-btn" id="wishBtn" aria-label="Wishlist" onClick={openWish}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 000-7.8z"/>
          </svg>
          {wishlist.length > 0 && <span className="badge" id="wishCount">{wishlist.length}</span>}
        </button>
        <button className="icon-btn" id="cartBtn" aria-label="Cart" onClick={openCart}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 01-8 0"/>
          </svg>
          {cartCount > 0 && <span className="badge" id="cartCount">{cartCount}</span>}
        </button>
        <a href="#jyotish" className="btn-book">Book Consultation</a>
        <button
          className="icon-btn hamburger"
          id="hamburger"
          aria-label="Menu"
          onClick={() => setDrawerOpen(prev => !prev)}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>
    </nav>
  );
}
