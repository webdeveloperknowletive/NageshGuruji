'use client';
import { useState } from 'react';
import { BRACELETS } from '@/lib/products';
import ProductCard from '@/components/ProductCard';

const FILTERS = [
  { label: 'All', value: 'all' },
  { label: 'Rudraksha Bracelets', value: 'rud' },
  { label: 'Gemstone Bracelets', value: 'gem' },
  { label: 'Spiritual Bracelets', value: 'spi' },
  { label: 'Combination Bracelets', value: 'combo' },
];

export default function BraceletsSection({ products }) {
  const [active, setActive] = useState('all');
  const list = (products && products.length > 0) ? products : BRACELETS;
  const filtered = active === 'all' ? list : list.filter(p => p.cat === active);

  return (
    <section id="bracelets">
      <div className="wrap">
        <div className="sec-head reveal">
          <span className="kicker">Bracelets</span>
          <h2>Spiritual <em>Bracelets</em></h2>
          <p>रुद्राक्ष, रत्न आणि संयोजन ब्रेसलेट — प्रत्येकासाठी धारण मार्गदर्शनासह.</p>
        </div>
        <div className="filter-bar">
          {FILTERS.map(f => (
            <button
              key={f.value}
              className={`filter-chip${active === f.value ? ' active' : ''}`}
              onClick={() => setActive(f.value)}
            >
              {f.label}
            </button>
          ))}
        </div>
        <div className="prod-grid">
          {filtered.length > 0 ? (
            filtered.map(product => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '40px', color: 'var(--muted)', fontSize: '13px' }}>
              या श्रेणीतील ब्रेसलेट्स लवकरच उपलब्ध होतील. (Products in this category will be available soon).
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
