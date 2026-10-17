import { FEATURED } from '@/lib/products';
import ProductCard from '@/components/ProductCard';

export default function FeaturedSection({ products }) {
  const list = (products && products.length > 0) ? products : FEATURED;

  return (
    <section>
      <div className="wrap">
        <div className="sec-head reveal">
          <span className="kicker">Featured</span>
          <h2>Our <em>Sacred</em> Collection</h2>
          <p>सर्वाधिक मागणी असलेली उत्पादने — प्रमाणित, अभिमंत्रित आणि पूर्ण मार्गदर्शनासह.</p>
        </div>
        <div className="prod-grid">
          {list.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}
