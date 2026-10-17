'use client';
import { useRef, useEffect, useState } from 'react';

export default function VideoSection() {
  const videoRef = useRef(null);
  const [isMuted, setIsMuted] = useState(true);
  const [volume, setVolume] = useState(1);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            video.play().catch((err) => {
              console.log('Autoplay prevented:', err);
            });
          } else {
            video.pause();
          }
        });
      },
      { threshold: 0.35 }
    );

    observer.observe(video);

    return () => {
      observer.disconnect();
    };
  }, []);

  const toggleMute = () => {
    if (!videoRef.current) return;
    const nextMuted = !isMuted;
    videoRef.current.muted = nextMuted;
    setIsMuted(nextMuted);
    if (!nextMuted && videoRef.current.volume === 0) {
      videoRef.current.volume = 1;
      setVolume(1);
    }
  };

  const handleVolumeChange = (e) => {
    const newVol = parseFloat(e.target.value);
    setVolume(newVol);
    if (videoRef.current) {
      videoRef.current.volume = newVol;
      if (newVol === 0) {
        videoRef.current.muted = true;
        setIsMuted(true);
      } else {
        videoRef.current.muted = false;
        setIsMuted(false);
      }
    }
  };

  return (
    <section className="video-section" id="video-tour" style={{ position: 'relative', zIndex: 5 }}>
      <div className="wrap">
        <div className="sec-head center">
          <span className="kicker">Video Experience</span>
          <h2>पवित्र विधी व <em>आध्यात्मिक दर्शन</em></h2>
          <p>
            रुद्राक्ष शुद्धीकरण, प्राणप्रतिष्ठा विधी आणि गुरुजींचे विशेष मार्गदर्शन — प्रत्यक्ष व्हिडिओ अनुभव.
          </p>
        </div>

        <div
          className="video-player-container"
          style={{
            maxWidth: '960px',
            margin: '0 auto',
            borderRadius: '24px',
            overflow: 'hidden',
            border: '1px solid rgba(224, 176, 74, 0.35)',
            boxShadow: '0 30px 80px -20px rgba(0, 0, 0, 0.9), 0 0 35px -10px rgba(224, 176, 74, 0.25)',
            background: 'linear-gradient(160deg, rgba(38,15,21,0.95), rgba(10,5,8,0.98))',
            position: 'relative',
          }}
        >
          <video
            ref={videoRef}
            src="/videos/guruji-video.mp4"
            playsInline
            muted={isMuted}
            loop
            preload="auto"
            style={{
              width: '100%',
              maxHeight: '600px',
              display: 'block',
              margin: '0 auto',
              background: '#0a0508',
            }}
          />

          {/* Volume Control Only */}
          <div
            style={{
              position: 'absolute',
              bottom: '18px',
              right: '18px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: 'rgba(10, 5, 8, 0.8)',
              backdropFilter: 'blur(10px)',
              padding: '8px 14px',
              borderRadius: '99px',
              border: '1px solid rgba(224, 176, 74, 0.35)',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.6)',
              zIndex: 10,
            }}
          >
            <button
              onClick={toggleMute}
              aria-label={isMuted ? 'Unmute video' : 'Mute video'}
              style={{
                background: 'none',
                border: 'none',
                color: isMuted ? 'var(--muted)' : 'var(--gold)',
                display: 'grid',
                placeItems: 'center',
                cursor: 'pointer',
                padding: '2px',
                transition: 'color 0.25s',
              }}
            >
              {isMuted || volume === 0 ? (
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ width: '18px', height: '18px' }}
                >
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                  <line x1="23" y1="9" x2="17" y2="15" />
                  <line x1="17" y1="9" x2="23" y2="15" />
                </svg>
              ) : (
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ width: '18px', height: '18px' }}
                >
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                  <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
                  <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
                </svg>
              )}
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={isMuted ? 0 : volume}
              onChange={handleVolumeChange}
              aria-label="Volume slider"
              style={{
                width: '65px',
                height: '4px',
                accentColor: 'var(--gold)',
                cursor: 'pointer',
                opacity: 0.9,
              }}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
