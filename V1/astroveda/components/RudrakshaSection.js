'use client';
import { useState } from 'react';
import { RUDRAKSHA } from '@/lib/products';
import ProductCard from '@/components/ProductCard';

const FILTERS = [
  { label: 'All · सर्व', value: 'all' },
  { label: '1 Mukhi', value: 'm1' },
  { label: '2 Mukhi', value: 'm2' },
  { label: '3 Mukhi', value: 'm3' },
  { label: '4 Mukhi', value: 'm4' },
  { label: '5 Mukhi', value: 'm5' },
  { label: '6 Mukhi', value: 'm6' },
  { label: '7 Mukhi', value: 'm7' },
  { label: 'Mala', value: 'mala' },
  { label: 'Bracelet', value: 'bracelet' },
];

export default function RudrakshaSection({ products }) {
  const [active, setActive] = useState('all');
  const list = (products && products.length > 0) ? products : RUDRAKSHA;
  const filtered = active === 'all' ? list : list.filter(p => p.cat === active);

  return (
    <section id="rudraksha">
      <div className="wrap">
        <div className="sec-head reveal">
          <span className="kicker">Rudraksha</span>
          <h2>रुद्राक्ष <em>Collection</em></h2>
          <p>प्रत्येक रुद्राक्ष प्रमाणित स्रोतांकडून — मुखीनुसार, आकारानुसार आणि पारंपरिक महत्त्वानुसार.</p>
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
              या श्रेणीतील रुद्राक्ष लवकरच उपलब्ध होतील. (Products in this category will be available soon).
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
