import { useRef, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { gsap } from 'gsap'
import NetworkVisualization from './NetworkVisualization'
import { useAuth } from '../../context/AuthContext'

export default function HeroSection() {
  const { isAuthenticated } = useAuth()
  const sectionRef = useRef<HTMLElement>(null)
  const titleRef = useRef<HTMLHeadingElement>(null)
  const textRef = useRef<HTMLParagraphElement>(null)
  const ctaRef = useRef<HTMLDivElement>(null)
  const visRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

      tl.fromTo(
        titleRef.current,
        { y: 50, opacity: 0 },
        { y: 0, opacity: 1, duration: 1.1, delay: 0.3 }
      )
        .fromTo(
          textRef.current,
          { y: 30, opacity: 0 },
          { y: 0, opacity: 0.85, duration: 0.8 },
          '-=0.7'
        )
        .fromTo(
          ctaRef.current,
          { y: 20, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.7 },
          '-=0.5'
        )
        .fromTo(
          visRef.current,
          { opacity: 0, scale: 0.96 },
          { opacity: 1, scale: 1, duration: 1.2, ease: 'power2.out' },
          '-=0.9'
        )
    }, sectionRef)

    return () => ctx.revert()
  }, [])

  const scrollToResearch = () => {
    const el = document.getElementById('features')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <section
      ref={sectionRef}
      style={{
        position: 'relative',
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        paddingTop: '6rem',
        paddingBottom: '3rem',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '1380px',
          margin: '0 auto',
          padding: '0 2rem',
          display: 'grid',
          gridTemplateColumns: '45% 55%',
          alignItems: 'center',
          gap: '2rem',
        }}
        className="hero-grid"
      >
        {/* LEFT COLUMN: EDITORIAL CONTENT */}
        <div style={{ zIndex: 2, paddingRight: '1rem' }}>
          <h1
            ref={titleRef}
            className="font-serif"
            style={{
              fontSize: 'clamp(3rem, 5.5vw, 5.25rem)',
              fontWeight: 400,
              lineHeight: 1.05,
              color: '#111111',
              letterSpacing: '-0.02em',
              marginBottom: '2rem',
              opacity: 0,
            }}
          >
            Agronomic intelligence that runs itself.
          </h1>

          <p
            ref={textRef}
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: 'clamp(1rem, 1.35vw, 1.25rem)',
              fontWeight: 400,
              lineHeight: 1.5,
              color: '#444444',
              maxWidth: '520px',
              marginBottom: '2.75rem',
              opacity: 0,
            }}
          >
            Fieldwise is the autonomous decision system for precision agriculture.
            Continuously understanding soil telemetry, optimizing NPK nutrient ratios, and improving crop yield.
          </p>

          {/* ACTION BUTTONS */}
          <div
            ref={ctaRef}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1.25rem',
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

            <button onClick={scrollToResearch} className="editorial-btn-secondary">
              <span className="editorial-corner-tl" />
              <span className="editorial-corner-tr" />
              <span className="editorial-corner-bl" />
              <span className="editorial-corner-br" />
              Explore the research
            </button>
          </div>
        </div>

        {/* RIGHT COLUMN: INTERACTIVE NETWORK VISUALIZATION */}
        <div
          ref={visRef}
          style={{
            position: 'relative',
            height: 'clamp(480px, 68vh, 720px)',
            width: '100%',
            opacity: 0,
          }}
        >
          <NetworkVisualization />
        </div>
      </div>

      <style>{`
        @media (max-width: 1024px) {
          .hero-grid {
            grid-template-columns: 1fr !important;
            padding-top: 2rem !important;
          }
        }
      `}</style>
    </section>
  )
}
