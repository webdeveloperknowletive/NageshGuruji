const reasons = [
  { num: '01', title: 'परंपरेचा अनुभव', desc: 'पूजा व ज्योतिष परंपरेशी जोडलेले मार्गदर्शन — तीन पिढ्यांचा अनुभव आणि शास्त्राधारित पद्धती.' },
  { num: '02', title: 'Personalised Guidance', desc: 'प्रत्येक व्यक्तीच्या गरजेनुसार सल्ला — जन्मकुंडलीचा अभ्यास करून वैयक्तिक शिफारस.' },
  { num: '03', title: 'Authentic Information', desc: 'प्रत्येक product सोबत स्पष्ट माहिती, प्रमाणपत्रे, मुख-आकार-महत्त्व आणि धारण पद्धत.' },
  { num: '04', title: 'Complete Spiritual Services', desc: 'पूजा, ज्योतिष, रत्न, रुद्राक्ष, यंत्र आणि Bracelets — सर्व एकाच ठिकाणी, एकाच विश्वासाने.' },
  { num: '05', title: 'After-Purchase Guidance', desc: 'Product घेतल्यानंतर वापर, धारण, पूजन आणि care instructions बद्दल संपूर्ण मार्गदर्शन.' },
  { num: '06', title: '10,000+ संतुष्ट ग्राहक', desc: 'महाराष्ट्र, गुजरात, कर्नाटक आणि परदेशातील हजारो कुटुंबांचा विश्वास.' },
];

export default function WhySection() {
  return (
    <section className="why-section">
      <div className="wrap">
        <div className="sec-head center reveal">
          <span className="kicker">Why Choose Us</span>
          <h2>आमची <em>वचनबद्धता</em></h2>
          <p>25 वर्षांहून अधिक अनुभव — परंपरा, प्रामाणिकपणा आणि वैयक्तिक मार्गदर्शन.</p>
        </div>
        <div className="why-grid">
          {reasons.map((r) => (
            <div key={r.num} className="why-card reveal">
              <div className="why-num">{r.num}</div>
              <h4>{r.title}</h4>
              <p>{r.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
