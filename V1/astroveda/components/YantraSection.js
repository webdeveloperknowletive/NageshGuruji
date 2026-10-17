import { YANTRA } from '@/lib/products';
import ProductCard from '@/components/ProductCard';

export default function YantraSection({ products }) {
  const list = (products && products.length > 0) ? products : YANTRA;

  return (
    <section id="yantra">
      <div className="wrap">
        <div className="sec-head reveal">
          <span className="kicker">Yantra</span>
          <h2>Sacred <em>Yantra</em> Collection</h2>
          <p>तांब्यात हस्तनिर्मित यंत्र — अभिमंत्रण, प्राणप्रतिष्ठा व स्थापना मार्गदर्शनासह.</p>
        </div>
        <div className="prod-grid">
          {list.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}
