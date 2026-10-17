export default function Hero({ banner, bgImage }) {
  const title = banner?.title;
  const subtitle = banner?.subtitle || 'Authentic Rudraksha · Certified Gemstones · Sacred Yantra · Jyotish Consultation';
  const btnText = banner?.button_text || 'Explore Collection →';
  const btnLink = banner?.link_url || '#shop';
  const bg = bgImage || banner?.image_url;

  return (
    <section 
      className="hero"
      style={bg ? {
        backgroundImage: `radial-gradient(circle at 75% 40%, rgba(224, 176, 74, 0.15) 0%, transparent 60%), linear-gradient(to bottom, rgba(16,12,8,0.76), rgba(16,12,8,0.92)), url(${bg})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      } : undefined}
    >
      <div className="hero-halo" />
      <div className="hero-inner">
        <div className="hero-copy">
          <p className="eyebrow">AstroVeda — Sacred Wisdom</p>
          <h1>
            {title && title !== 'परंपरेतून मार्गदर्शन • श्रद्धेतून समाधान' ? (
              title
            ) : (
              <>
                परंपरेतून <em>मार्गदर्शन</em><br />
                श्रद्धेतून <em>समाधान</em>
              </>
            )}
          </h1>
          <p className="sub">{subtitle}</p>
          <div className="hero-pills">
            <span>✓ IGI / GIA Certified</span>
            <span>✓ Energised Products</span>
            <span>✓ 25+ Years Experience</span>
            <span>✓ 10,000+ Satisfied Clients</span>
          </div>
          <div className="hero-actions">
            <a href={btnLink} className="btn btn-gold">{btnText}</a>
            <a href="#jyotish" className="btn btn-ghost">Book Consultation</a>
          </div>
        </div>

        <div className="hero-visual">
          <svg className="mandala" viewBox="0 0 400 400" aria-hidden="true">
            <defs>
              <radialGradient id="auraGold" cx="50%" cy="50%" r="60%">
                <stop offset="0" stopColor="#e0b04a" stopOpacity=".35"/>
                <stop offset="1" stopColor="#e0b04a" stopOpacity="0"/>
              </radialGradient>
            </defs>
            <circle cx="200" cy="200" r="192" fill="none" stroke="rgba(224,176,74,.22)" strokeWidth=".8" strokeDasharray="4 8"/>
            <circle cx="200" cy="200" r="160" fill="none" stroke="rgba(224,176,74,.16)" strokeWidth=".8" strokeDasharray="3 6"/>
            <g id="petals">
              {Array.from({ length: 24 }).map((_, i) => {
                const angle = (i / 24) * 360;
                return (
                  <ellipse
                    key={i}
                    cx={200}
                    cy={67}
                    rx={15}
                    ry={33}
                    transform={`rotate(${angle} 200 200)`}
                    fill="none"
                    stroke="rgba(224,176,74,.28)"
                    strokeWidth=".7"
                  />
                );
              })}
            </g>
          </svg>
          <svg className="mandala-rev" viewBox="0 0 400 400" aria-hidden="true">
            <circle cx="200" cy="200" r="118" fill="none" stroke="rgba(255,140,43,.26)" strokeWidth=".7" strokeDasharray="3 6"/>
            <circle cx="200" cy="200" r="88" fill="none" stroke="rgba(255,140,43,.18)" strokeWidth=".7" strokeDasharray="2 5"/>
          </svg>
          <div className="center-om">ॐ</div>
          <div className="hero-floating-chips">
            <span className="hero-chip c1">📿 5 Mukhi Rudraksha</span>
            <span className="hero-chip c2">💎 IGI Certified Gems</span>
            <span className="hero-chip c3">🪔 अभिमंत्रित यंत्र</span>
          </div>
        </div>
      </div>
    </section>
  );
}
