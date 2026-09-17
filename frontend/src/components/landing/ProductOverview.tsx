import { useRef, useEffect } from 'react'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const features = [
  {
    num: '01',
    title: 'Soil Telemetry Stream',
    desc: 'Ingests real-time soil nutrient parameters: Nitrogen (N), Phosphorus (P), Potassium (K), pH, temperature, and moisture levels.',
    badge: 'TELEMETRY',
  },
  {
    num: '02',
    title: 'Ensemble Machine Intelligence',
    desc: 'Powered by XGBoost and Random Forest multi-class classification models to analyze non-linear crop-nutrient dependencies.',
    badge: 'MODEL ENGINE',
  },
  {
    num: '03',
    title: 'Precision Fertilizer Prescription',
    desc: 'Generates targeted recommendations (Urea, DAP, 14-35-14, 28-28-0, etc.) with exact application ratios to prevent soil degradation.',
    badge: 'OPTIMIZATION',
  },
  {
    num: '04',
    title: 'Audit & Yield Governance',
    desc: 'Tracks historical prediction records, model confidence metrics, and feature importance matrices for complete transparency.',
    badge: 'AUDIT TRAIL',
  },
]

const metrics = [
  { value: '98.4%', label: 'Ensemble Model Accuracy' },
  { value: '< 12ms', label: 'Inference Latency' },
  { value: '10+', label: 'Soil & Crop Profiles' },
  { value: '100%', label: 'Audit Trail Provenance' },
]

export default function ProductOverview() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Feature cards animation
      gsap.from('.product-feature-card', {
        scrollTrigger: {
          trigger: containerRef.current,
          start: 'top 75%',
        },
        y: 40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out',
      })

      // Metrics animation
      gsap.from('.metric-item', {
        scrollTrigger: {
          trigger: '.metrics-container',
          start: 'top 85%',
        },
        y: 30,
        opacity: 0,
        duration: 0.7,
        stagger: 0.1,
        ease: 'power2.out',
      })
    }, containerRef)

    return () => ctx.revert()
  }, [])

  return (
    <div ref={containerRef} style={{ padding: '6rem 2rem 4rem', maxWidth: '1380px', margin: '0 auto' }}>
      {/* SECTION HEADER */}
      <div id="features" style={{ marginBottom: '4rem' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.25rem 0.75rem',
            borderRadius: '9999px',
            border: '1px solid rgba(17, 17, 17, 0.2)',
            fontFamily: 'var(--font-body)',
            fontSize: '0.75rem',
            fontWeight: 600,
            color: '#111111',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            marginBottom: '1.25rem',
          }}
        >
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#FF6B00' }} />
          System Architecture
        </div>
        <h2
          className="font-serif"
          style={{
            fontSize: 'clamp(2.25rem, 4vw, 3.5rem)',
            fontWeight: 400,
            color: '#111111',
            letterSpacing: '-0.02em',
            maxWidth: '680px',
            lineHeight: 1.15,
          }}
        >
          Built for autonomous soil nutrient optimization.
        </h2>
      </div>

      {/* FEATURE GRID */}
      <div
        id="architecture"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '1.5rem',
          marginBottom: '6rem',
        }}
      >
        {features.map((item) => (
          <div
            key={item.num}
            className="product-feature-card"
            style={{
              background: 'rgba(255, 255, 255, 0.65)',
              backdropFilter: 'blur(12px)',
              borderRadius: '1.25rem',
              padding: '2.25rem 1.75rem',
              border: '1px solid rgba(255, 255, 255, 0.8)',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.03)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              transition: 'all 0.3s ease',
            }}
          >
            <div>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '1.5rem',
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: '#888888',
                  }}
                >
                  {item.num}
                </span>
                <span
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.6875rem',
                    fontWeight: 600,
                    color: '#111111',
                    background: 'rgba(0, 0, 0, 0.05)',
                    padding: '0.2rem 0.6rem',
                    borderRadius: '4px',
                    letterSpacing: '0.05em',
                  }}
                >
                  {item.badge}
                </span>
              </div>
              <h3
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '1.25rem',
                  fontWeight: 600,
                  color: '#111111',
                  marginBottom: '0.875rem',
                  letterSpacing: '-0.01em',
                }}
              >
                {item.title}
              </h3>
              <p
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.9375rem',
                  color: '#555555',
                  lineHeight: 1.6,
                }}
              >
                {item.desc}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* METRICS SHOWCASE */}
      <div
        id="research"
        className="metrics-container"
        style={{
          background: '#111111',
          color: '#FFFFFF',
          borderRadius: '1.75rem',
          padding: '3.5rem 2.5rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '2.5rem',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
        }}
      >
        {metrics.map((m, idx) => (
          <div key={idx} className="metric-item">
            <div
              className="font-serif"
              style={{
                fontSize: 'clamp(2.5rem, 4vw, 3.75rem)',
                fontWeight: 400,
                color: '#FFFFFF',
                lineHeight: 1,
                marginBottom: '0.75rem',
              }}
            >
              {m.value}
            </div>
            <div
              style={{
                fontFamily: 'var(--font-body)',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: '#999999',
                letterSpacing: '0.02em',
              }}
            >
              {m.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
