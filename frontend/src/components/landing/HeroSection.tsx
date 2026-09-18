import { useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { gsap } from 'gsap'
import NetworkVisualization from './NetworkVisualization'
import { useAuth } from '../../context/AuthContext'

export default function HeroSection() {
  const { isAuthenticated } = useAuth()
  const sectionRef = useRef<HTMLElement>(null)
  const badgeRef = useRef<HTMLDivElement>(null)
  const titleRef = useRef<HTMLHeadingElement>(null)
  const textRef = useRef<HTMLParagraphElement>(null)
  const ctaRef = useRef<HTMLDivElement>(null)
  const visRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

      tl.fromTo(
        badgeRef.current,
        { y: -15, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, delay: 0.15 }
      )
        .fromTo(
          titleRef.current,
          { y: 35, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.95 },
          '-=0.35'
        )
        .fromTo(
          textRef.current,
          { y: 25, opacity: 0 },
          { y: 0, opacity: 0.9, duration: 0.75 },
          '-=0.6'
        )
        .fromTo(
          ctaRef.current,
          { y: 20, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.65 },
          '-=0.45'
        )
        .fromTo(
          visRef.current,
          { opacity: 0, scale: 0.95 },
          { opacity: 1, scale: 1, duration: 1.1, ease: 'power2.out' },
          '-=0.85'
        )
    }, sectionRef)

    return () => ctx.revert()
  }, [])

  const scrollToProduct = () => {
    const el = document.getElementById('features') || document.getElementById('product')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <section ref={sectionRef} className="hero-section">
      <div className="hero-grid">
        {/* LEFT COLUMN: EDITORIAL CONTENT */}
        <div style={{ zIndex: 2, paddingRight: '0.5rem' }}>
          {/* MICRO LABEL */}
          <div
            ref={badgeRef}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.25rem 0.75rem',
              borderRadius: '9999px',
              border: '1px solid rgba(17, 17, 17, 0.12)',
              background: 'rgba(255, 255, 255, 0.5)',
              fontFamily: 'var(--font-body)',
              fontSize: '0.6875rem',
              fontWeight: 600,
              color: '#333333',
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              marginBottom: '1.25rem',
              opacity: 0,
            }}
          >
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#FF6B00' }} />
            Autonomous Agronomic Telemetry
          </div>

          {/* HEADLINE */}
          <h1
            ref={titleRef}
            className="font-serif"
            style={{
              fontSize: 'clamp(2.35rem, 4.1vw, 3.85rem)',
              fontWeight: 400,
              lineHeight: 1.08,
              color: '#111111',
              letterSpacing: '-0.025em',
              marginBottom: '1.25rem',
              maxWidth: '540px',
              opacity: 0,
            }}
          >
            Turn complex soil telemetry into clear decisions.
          </h1>

          {/* DESCRIPTION */}
          <p
            ref={textRef}
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: 'clamp(0.9375rem, 1.15vw, 1.125rem)',
              fontWeight: 400,
              lineHeight: 1.55,
              color: '#555555',
              maxWidth: '510px',
              marginBottom: '2.25rem',
              opacity: 0,
            }}
          >
            Fieldwise deploys ensemble machine learning to analyze NPK telemetry, soil pH, and environmental variables—delivering real-time fertilizer recommendations with agronomic precision.
          </p>

          {/* ACTION BUTTONS */}
          <div
            ref={ctaRef}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              flexWrap: 'wrap',
              opacity: 0,
            }}
          >
            {isAuthenticated ? (
              <Link to="/overview" className="editorial-btn-primary">
                Open Dashboard
                <span className="material-symbols-outlined" style={{ fontSize: '18px', marginLeft: '6px' }}>
                  arrow_forward
                </span>
              </Link>
            ) : (
              <Link to="/register" className="editorial-btn-primary">
                Get Started
                <span className="material-symbols-outlined" style={{ fontSize: '18px', marginLeft: '6px' }}>
                  arrow_forward
                </span>
              </Link>
            )}

            <button onClick={scrollToProduct} className="editorial-btn-secondary">
              Explore
            </button>
          </div>
        </div>

        {/* RIGHT COLUMN: INTERACTIVE NETWORK VISUALIZATION */}
        <div
          ref={visRef}
          style={{
            position: 'relative',
            height: 'clamp(340px, 52vh, 540px)',
            width: '100%',
            opacity: 0,
          }}
        >
          <NetworkVisualization />
        </div>
      </div>
    </section>
  )
}
