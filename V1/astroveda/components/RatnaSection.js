import { RATNA } from '@/lib/products';
import ProductCard from '@/components/ProductCard';

export default function RatnaSection({ products }) {
  const list = (products && products.length > 0) ? products : RATNA;

  return (
    <section id="ratna">
      <div className="wrap">
        <div className="sec-head reveal">
          <span className="kicker">Ratna</span>
          <h2>Choose Your <em>Gemstone</em> With Guidance</h2>
          <p>प्रत्येक रत्न IGI / GIA प्रमाणित. पण रत्न निवड ही वैयक्तिक बाब आहे — म्हणून आम्ही मार्गदर्शन देतो.</p>
        </div>
        <div className="prod-grid">
          {list.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
        <div style={{ marginTop: '40px', textAlign: 'center' }}>
          <a href="#jyotish" className="btn btn-gold" style={{ padding: '16px 34px' }}>
            Not sure which gemstone is right for you? · Get Gemstone Consultation →
          </a>
        </div>
      </div>
    </section>
  );
}
