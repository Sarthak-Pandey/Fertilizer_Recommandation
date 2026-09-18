import { useRef, useEffect } from 'react'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const workflowSteps = [
  {
    num: '01',
    title: 'Ingest Telemetry',
    subtitle: 'Real-time Soil & Climate Signals',
    desc: 'Continuously streams multi-variable parameters including Nitrogen (N), Phosphorus (P), Potassium (K), soil pH, humidity, and rainfall readings.',
    badge: 'TELEMETRY STREAM',
  },
  {
    num: '02',
    title: 'Multi-Model Inference',
    subtitle: 'XGBoost & Forest Ensembles',
    desc: 'Processes soil vector metrics through trained multi-class ensemble models to classify non-linear agronomic dependencies instantly.',
    badge: 'ENSEMBLE ENGINE',
  },
  {
    num: '03',
    title: 'Precision Recommendation',
    subtitle: 'Optimized Fertilizer Ratios',
    desc: 'Prescribes optimal fertilizer types (Urea, DAP, 14-35-14, 28-28-0, etc.) with exact application rates to preserve long-term soil health.',
    badge: 'AGRONOMIC PRESCRIPTION',
  },
  {
    num: '04',
    title: 'Audit & Provenance',
    subtitle: 'Model Governance & Telemetry History',
    desc: 'Records complete inference logs, feature importance values, and confidence metrics in an auditable telemetry ledger.',
    badge: 'MODEL AUDIT',
  },
]

const systemMetrics = [
  { value: '98.4%', label: 'Classification Accuracy' },
  { value: '< 12ms', label: 'Inference Latency' },
  { value: '7+', label: 'Soil Parameters' },
  { value: '100%', label: 'Auditable Provenance' },
]

export default function ProductOverview() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Step blocks animation
      gsap.from('.workflow-block', {
        scrollTrigger: {
          trigger: containerRef.current,
          start: 'top 75%',
        },
        y: 35,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out',
      })

      // Metrics animation
      gsap.from('.metric-block', {
        scrollTrigger: {
          trigger: '.metrics-container',
          start: 'top 85%',
        },
        y: 25,
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
            border: '1px solid rgba(17, 17, 17, 0.15)',
            background: 'rgba(255, 255, 255, 0.6)',
            fontFamily: 'var(--font-body)',
            fontSize: '0.6875rem',
            fontWeight: 600,
            color: '#111111',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            marginBottom: '1.25rem',
          }}
        >
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#FF6B00' }} />
          Product Architecture
        </div>
        <h2
          className="font-serif"
          style={{
            fontSize: 'clamp(2.15rem, 3.8vw, 3.25rem)',
            fontWeight: 400,
            color: '#111111',
            letterSpacing: '-0.02em',
            maxWidth: '680px',
            lineHeight: 1.15,
          }}
        >
          Autonomous decision lifecycle for precision agriculture.
        </h2>
      </div>

      {/* EDITORIAL WORKFLOW BLOCKS */}
      <div
        id="product"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '1.5rem',
          marginBottom: '5rem',
        }}
      >
        {workflowSteps.map((step) => (
          <div
            key={step.num}
            className="workflow-block"
            style={{
              background: 'rgba(255, 255, 255, 0.7)',
              backdropFilter: 'blur(12px)',
              borderRadius: '1.25rem',
              padding: '2.25rem 1.75rem',
              border: '1px solid rgba(17, 17, 17, 0.08)',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.02)',
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
                  {step.num}
                </span>
                <span
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.625rem',
                    fontWeight: 600,
                    color: '#111111',
                    background: 'rgba(0, 0, 0, 0.05)',
                    padding: '0.2rem 0.55rem',
                    borderRadius: '4px',
                    letterSpacing: '0.06em',
                    textTransform: 'uppercase',
                  }}
                >
                  {step.badge}
                </span>
              </div>
              <h3
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '1.25rem',
                  fontWeight: 600,
                  color: '#111111',
                  marginBottom: '0.35rem',
                  letterSpacing: '-0.015em',
                }}
              >
                {step.title}
              </h3>
              <div
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.75rem',
                  fontWeight: 500,
                  color: '#888888',
                  marginBottom: '1rem',
                  letterSpacing: '0.02em',
                }}
              >
                {step.subtitle}
              </div>
              <p
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.90625rem',
                  color: '#555555',
                  lineHeight: 1.6,
                }}
              >
                {step.desc}
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
        {systemMetrics.map((m, idx) => (
          <div key={idx} className="metric-block">
            <div
              className="font-serif"
              style={{
                fontSize: 'clamp(2.35rem, 4vw, 3.5rem)',
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
