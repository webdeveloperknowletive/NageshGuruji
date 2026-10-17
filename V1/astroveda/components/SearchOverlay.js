'use client';
import { useState, useRef, useEffect } from 'react';
import { useStore } from '@/context/StoreContext';
import { getAllProducts, adaptApiProduct } from '@/lib/products';
import { getProducts } from '@/lib/api';

const POPULAR_SEARCHES = [
  '5 Mukhi Rudraksha',
  'Emerald · Panna',
  'Shri Yantra',
  'Blue Sapphire',
  'Rudraksha Mala',
  'Navagraha Bracelet',
  'Yellow Sapphire',
  'Kuber Yantra',
];

export default function SearchOverlay() {
  const { searchOpen, setSearchOpen, openProductModal } = useStore();
  const [query, setQuery] = useState('');
  const [liveProducts, setLiveProducts] = useState([]);
  const inputRef = useRef(null);

  useEffect(() => {
    if (searchOpen) {
      if (inputRef.current) {
        setTimeout(() => inputRef.current?.focus(), 150);
      }
      getProducts()
        .then(res => {
          if (res?.products && res.products.length > 0) {
            setLiveProducts(res.products.map(adaptApiProduct).filter(Boolean));
          }
        })
        .catch(() => {});
    } else {
      setQuery('');
    }
  }, [searchOpen]);

  const allProducts = liveProducts.length > 0 ? liveProducts : getAllProducts();
  const q = query.trim().toLowerCase();
  const matches = q
    ? allProducts
        .filter(
          p =>
            p.title.toLowerCase().includes(q) ||
            p.desc.toLowerCase().includes(q) ||
            (p.catLabel && p.catLabel.toLowerCase().includes(q))
        )
        .slice(0, 8)
    : [];

  const handlePick = (prod) => {
    setSearchOpen(false);
    openProductModal(prod);
  };

  return (
    <div className={`search-overlay${searchOpen ? ' open' : ''}`} aria-hidden={!searchOpen}>
      <button
        className="search-close"
        onClick={() => setSearchOpen(false)}
        aria-label="Close search"
      >
        ✕
      </button>

      <div className="search-inner">
        <p className="search-title">Search AstroVeda</p>
        <div className="search-box">
          <svg className="search-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <circle cx="11" cy="11" r="7"/>
            <path d="M21 21l-4.3-4.3"/>
          </svg>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Rudraksha, Emerald, Shri Yantra, Bracelet..."
            autoComplete="off"
          />
          <button className="go" aria-label="Search">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round">
              <path d="M5 12h14M13 6l6 6-6 6"/>
            </svg>
          </button>
        </div>

        <p className="search-suggest-label">Popular Searches</p>
        <div className="search-chips">
          {POPULAR_SEARCHES.map(term => (
            <button
              key={term}
              className="search-chip"
              onClick={() => setQuery(term)}
            >
              {term}
            </button>
          ))}
        </div>

        <div className="search-results">
          {q && matches.length === 0 && (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '30px', color: 'var(--muted)', fontSize: '13px' }}>
              No products found for &quot;{query}&quot;
            </div>
          )}
          {matches.map(p => (
            <div
              key={p.id || p.title}
              className="search-result-item"
              onClick={() => handlePick(p)}
              style={{ cursor: 'pointer' }}
            >
              <div
                className="sr-thumb"
                dangerouslySetInnerHTML={{ __html: p.img || '' }}
              />
              <div className="sr-info">
                <h4>{p.title}</h4>
                <span>{p.price}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
