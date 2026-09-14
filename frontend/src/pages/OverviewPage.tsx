import { useEffect, useRef, useState } from 'react'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

// ---- Data ----
const recommendations = [
  { id: '#FW-9402', formula: 'Urea 46-0-0', conf: 99.1, time: 'Today 09:42', latency: '28ms', status: 'Deployed', statusColor: 'primary' },
  { id: '#FW-9401', formula: 'DAP (18-46-0)', conf: 97.8, time: 'Today 08:15', latency: '32ms', status: 'Deployed', statusColor: 'primary' },
  { id: '#FW-9399', formula: 'Potash MOP', conf: 98.4, time: 'Yesterday', latency: '24ms', status: 'In Review', statusColor: 'amber' },
  { id: '#FW-9395', formula: 'Ammonium Nitrate', conf: 96.9, time: 'Yesterday', latency: '35ms', status: 'Deployed', statusColor: 'primary' },
  { id: '#FW-9390', formula: 'NPK 16-16-16', conf: 95.2, time: '2 days ago', latency: '29ms', status: 'Deployed', statusColor: 'primary' },
]

const healthMetrics = [
  { icon: 'speed', label: 'FastAPI Latency', value: '28ms avg' },
  { icon: 'memory', label: 'Redis Cache Hit', value: '99.4%' },
  { icon: 'hub', label: 'XGBoost Node', value: 'Healthy ✓' },
  { icon: 'verified_user', label: 'System Uptime', value: '99.98%' },
]

const growthStages = ['Sowing', 'Vegetative V4', 'Reproductive R1', 'Grain Fill']

// ---- Animated Counter ----
function AnimatedCounter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obj = { val: 0 }
    gsap.to(obj, {
      val: target,
      duration: 2,
      delay: 0.5,
      ease: 'power2.out',
      onUpdate: () => {
        el.textContent = `${target % 1 !== 0 ? obj.val.toFixed(1) : Math.round(obj.val)}${suffix}`
      },
    })
  }, [target, suffix])
  return <span ref={ref}>0{suffix}</span>
}

// ---- Confidence Ring ----
function ConfidenceRing({ value }: { value: number }) {
  const circleRef = useRef<SVGCircleElement>(null)
  const r = 42
  const circ = 2 * Math.PI * r

  useEffect(() => {
    if (!circleRef.current) return
    const dashoffset = circ * (1 - value / 100)
    gsap.fromTo(
      circleRef.current,
      { strokeDashoffset: circ },
      { strokeDashoffset: dashoffset, duration: 2, delay: 0.8, ease: 'power3.out' }
    )
  }, [value, circ])

  return (
    <div style={{ position: 'relative', width: '120px', height: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg viewBox="0 0 100 100" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
        <circle cx="50" cy="50" r={r} fill="transparent" stroke="#E6E6E2" strokeWidth="6" />
        <circle
          ref={circleRef}
          cx="50" cy="50" r={r}
          fill="transparent"
          stroke="#111111"
          strokeWidth="6"
          strokeDasharray={circ}
          strokeDashoffset={circ}
          strokeLinecap="round"
        />
      </svg>
      <div style={{
        position: 'absolute',
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
      }}>
        <span style={{
          fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 700,
          color: '#111111', lineHeight: 1,
        }}>{value}%</span>
        <span style={{
          fontFamily: 'var(--font-body)', fontSize: '0.5625rem', fontWeight: 600,
          color: '#666666', textTransform: 'uppercase', letterSpacing: '0.04em', marginTop: '3px',
        }}>Confidence</span>
      </div>
    </div>
  )
}

// ---- Main Page ----
export default function OverviewPage() {
  const heroRef = useRef<HTMLDivElement>(null)
  const statsRef = useRef<HTMLDivElement>(null)
  const formRef = useRef<HTMLDivElement>(null)
  const resultRef = useRef<HTMLDivElement>(null)
  const tableRef = useRef<HTMLDivElement>(null)
  const healthRef = useRef<HTMLDivElement>(null)
  const rowsRef = useRef<HTMLDivElement[]>([])

  const [ph, setPh] = useState(6.4)
  const [nitrogen, setNitrogen] = useState(140)
  const [phosphorus, setPhosphorus] = useState(45)
  const [potassium, setPotassium] = useState(120)
  const [stage, setStage] = useState('Vegetative V4')
  const [computing, setComputing] = useState(false)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Hero stagger entrance
      gsap.fromTo(
        heroRef.current,
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 1, ease: 'power3.out', delay: 0.2 }
      )

      // Stats cards
      gsap.fromTo(
        statsRef.current!.children,
        { opacity: 0, y: 20, scale: 0.97 },
        {
          opacity: 1, y: 0, scale: 1,
          duration: 0.6, stagger: 0.1, ease: 'power2.out',
          delay: 0.4,
        }
      )

      // Form panel – scroll trigger
      gsap.fromTo(formRef.current, { opacity: 0, x: -30 }, {
        opacity: 1, x: 0, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: formRef.current, start: 'top 85%' },
      })

      // Result panel – scroll trigger
      gsap.fromTo(resultRef.current, { opacity: 0, x: 30 }, {
        opacity: 1, x: 0, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: resultRef.current, start: 'top 85%' },
      })

      // Table rows stagger
      gsap.fromTo(rowsRef.current, { opacity: 0, y: 15 }, {
        opacity: 1, y: 0, duration: 0.5, stagger: 0.08, ease: 'power2.out',
        scrollTrigger: { trigger: tableRef.current, start: 'top 80%' },
      })

      // Health bar
      gsap.fromTo(healthRef.current!.children, { opacity: 0, y: 15 }, {
        opacity: 1, y: 0, duration: 0.5, stagger: 0.08, ease: 'power2.out',
        scrollTrigger: { trigger: healthRef.current, start: 'top 90%' },
      })
    })

    return () => ctx.revert()
  }, [])

  const handleCompute = () => {
    setComputing(true)
    gsap.to('.compute-btn', { scale: 0.98, duration: 0.1, yoyo: true, repeat: 1 })
    setTimeout(() => setComputing(false), 1800)
  }

  const filtered = filter === 'all'
    ? recommendations
    : recommendations.filter(r => r.status === 'Deployed')

  return (
    <main style={{ minHeight: 'calc(100vh - 60px)', paddingBottom: '3rem' }}>
      <div className="container" style={{ paddingTop: '2.5rem' }}>

        {/* ===== HERO ===== */}
        <section ref={heroRef} style={{ marginBottom: '2rem', opacity: 0 }}>
          <div className="glass" style={{
            borderRadius: 'var(--radius-xl)',
            padding: '2rem',
            position: 'relative', overflow: 'hidden',
          }}>
            <div style={{ position: 'relative', zIndex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
                <span className="badge badge-primary">
                  <span className="material-symbols-outlined" style={{ fontSize: '13px' }}>science</span>
                  Autonomous Agronomic Dispatch
                </span>
                <span style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.75rem',
                  color: '#666666',
                }}>Tuesday, 14 June 2025 · North Block</span>
              </div>

              <h1 style={{
                fontFamily: 'var(--font-display)',
                fontSize: 'clamp(1.75rem, 4.5vw, 2.75rem)',
                fontWeight: 600, letterSpacing: '-0.03em',
                marginBottom: '0.75rem', color: '#111111',
              }}>
                Make the next <span className="text-gradient">application count.</span>
              </h1>
              <p style={{
                fontFamily: 'var(--font-body)',
                fontSize: '1rem', color: '#555555',
                maxWidth: '600px', lineHeight: 1.6,
              }}>
                Precision nutrient optimization driven by multi-spectral soil telemetry and predictive agronomic models.
              </p>
            </div>

            {/* Stat cards strip */}
            <div ref={statsRef} style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '1rem',
              marginTop: '2rem',
              paddingTop: '1.5rem',
              borderTop: '1px solid #E2E2DF',
            }} className="stats-grid">
              {[
                { label: 'Predictions Logged', value: 156, suffix: '', delta: '+12% this cycle', icon: 'monitoring' },
                { label: 'Average Confidence', value: 98.6, suffix: '%', delta: 'Model v2.4 Active', icon: 'verified' },
                { label: 'Frequent Recommendation', value: null, text: 'Urea', delta: '41.2% distribution', icon: 'water_drop' },
              ].map((stat, i) => (
                <div key={i} style={{
                  background: '#FAFAF8',
                  borderRadius: 'var(--radius-lg)',
                  padding: '1rem 1.25rem',
                  border: '1px solid #E2E2DF',
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                }}>
                  <div>
                    <p style={{
                      fontFamily: 'var(--font-body)', fontSize: '0.6875rem',
                      fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase',
                      color: '#777777', marginBottom: '0.25rem',
                    }}>{stat.label}</p>
                    <p className="stat-ticker" style={{
                      fontSize: '1.5rem',
                      color: '#111111',
                    }}>
                      {stat.value !== null
                        ? <AnimatedCounter target={stat.value} suffix={stat.suffix} />
                        : stat.text}
                    </p>
                    <p style={{
                      fontFamily: 'var(--font-body)', fontSize: '0.6875rem',
                      color: '#666666', marginTop: '3px',
                    }}>{stat.delta}</p>
                  </div>
                  <div style={{
                    width: '42px', height: '42px', borderRadius: 'var(--radius-md)',
                    background: '#F0F0EC', border: '1px solid #E2E2DF',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexShrink: 0,
                  }}>
                    <span className="material-symbols-outlined" style={{
                      color: '#111111', fontSize: '22px',
                      fontVariationSettings: "'FILL' 1",
                    }}>{stat.icon}</span>
                  </div>
                </div>
              ))}
            </div>

            <style>{`
              @media (max-width: 640px) {
                .stats-grid { grid-template-columns: 1fr !important; }
              }
            `}</style>
          </div>
        </section>

        {/* ===== SOIL ANALYSIS + RECOMMENDATION ===== */}
        <section style={{
          marginBottom: '2rem',
        }} id="analysis">
          <div style={{ display: 'grid', gridTemplateColumns: '7fr 5fr', gap: '1.25rem' }} className="analysis-grid">

            {/* FORM PANEL */}
            <div ref={formRef} className="glass" style={{
              borderRadius: 'var(--radius-xl)',
              padding: '1.75rem',
              opacity: 0,
            }}>
              <div style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                marginBottom: '1.5rem', paddingBottom: '1rem',
                borderBottom: '1px solid #E2E2DF',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className="material-symbols-outlined" style={{ color: '#111111' }}>tune</span>
                  <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 600, color: '#111111' }}>
                    Soil Chemistry Telemetry
                  </h2>
                </div>
                <span style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.625rem', fontWeight: 600,
                  letterSpacing: '0.06em', textTransform: 'uppercase',
                  color: '#111111', background: '#F0F0EC',
                  border: '1px solid #E2E2DF',
                  padding: '0.25rem 0.625rem', borderRadius: 'var(--radius-sm)',
                }}>NODE #US-C1-S8</span>
              </div>

              {/* pH Slider */}
              <div style={{
                background: '#FAFAF8', borderRadius: 'var(--radius-lg)',
                padding: '1.25rem', border: '1px solid #E2E2DF',
                marginBottom: '1.25rem',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.875rem' }}>
                  <label style={{
                    fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 500,
                    color: '#111111',
                    display: 'flex', alignItems: 'center', gap: '0.375rem',
                  }}>
                    <span className="material-symbols-outlined" style={{ fontSize: '18px', color: '#111111' }}>opacity</span>
                    Soil pH Reaction
                  </label>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{
                      fontFamily: 'var(--font-display)', fontSize: '1.5rem', fontWeight: 700,
                      color: '#111111',
                    }}>{ph.toFixed(1)}</span>
                    <span className="badge badge-primary" style={{ padding: '0.125rem 0.5rem', fontSize: '0.625rem' }}>
                      {ph < 5 ? 'Acidic' : ph < 7 ? 'Optimal' : 'Alkaline'}
                    </span>
                  </div>
                </div>
                <input type="range" min={4.5} max={8.5} step={0.1} value={ph}
                  onChange={e => setPh(parseFloat(e.target.value))} />
                <div style={{
                  display: 'flex', justifyContent: 'space-between',
                  fontFamily: 'var(--font-body)', fontSize: '0.625rem',
                  color: '#777777', marginTop: '0.5rem',
                }}>
                  <span>4.5 Acidic</span><span>6.5 Neutral</span><span>8.5 Alkaline</span>
                </div>
              </div>

              {/* NPK Inputs */}
              <div style={{ marginBottom: '1.25rem' }}>
                <div style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  marginBottom: '0.75rem',
                }}>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 500, color: '#111111' }}>
                    Elemental Nutrients
                  </span>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.6875rem', color: '#777777' }}>
                    Unit: kg/ha
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.75rem' }}>
                  {[
                    { label: 'N', name: 'Nitrogen', val: nitrogen, set: setNitrogen, fill: 70 },
                    { label: 'P', name: 'Phosphorus', val: phosphorus, set: setPhosphorus, fill: 45 },
                    { label: 'K', name: 'Potassium', val: potassium, set: setPotassium, fill: 60 },
                  ].map(n => (
                    <div key={n.label} style={{
                      background: '#FAFAF8',
                      borderRadius: 'var(--radius-lg)', padding: '0.75rem',
                      border: '1px solid #E2E2DF',
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.375rem' }}>
                        <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 700, color: '#111111' }}>{n.label}</span>
                        <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', color: '#777777' }}>{n.name}</span>
                      </div>
                      <input type="number" value={n.val}
                        onChange={e => n.set(parseInt(e.target.value) || 0)}
                        className="input" style={{ textAlign: 'center', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '1.125rem', padding: '0.375rem' }} />
                      <div className="progress-bar" style={{ marginTop: '0.625rem' }}>
                        <div className="progress-fill" style={{ width: `${n.fill}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Moisture & Organic Matter */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1.25rem' }}>
                {[
                  { icon: 'humidity_mid', label: 'Volumetric Moisture', value: '24.2%' },
                  { icon: 'compost', label: 'Organic Matter', value: '3.8% SOM' },
                ].map(m => (
                  <div key={m.label} style={{
                    background: '#FAFAF8', borderRadius: 'var(--radius-lg)',
                    padding: '0.75rem 1rem', border: '1px solid #E2E2DF',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  }}>
                    <div>
                      <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', color: '#777777', display: 'block', marginBottom: '2px' }}>{m.label}</span>
                      <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.0625rem', fontWeight: 600, color: '#111111' }}>{m.value}</span>
                    </div>
                    <span className="material-symbols-outlined" style={{ color: '#111111', fontVariationSettings: "'FILL' 1" }}>{m.icon}</span>
                  </div>
                ))}
              </div>

              {/* Growth Stage */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 500, color: '#111111', display: 'block', marginBottom: '0.5rem' }}>
                  Phenological Growth Stage
                </label>
                <div style={{
                  display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.375rem',
                  background: '#F0F0EC', padding: '0.375rem',
                  borderRadius: 'var(--radius-full)', border: '1px solid #E2E2DF',
                }}>
                  {growthStages.map(s => (
                    <button key={s} onClick={() => setStage(s)} style={{
                      padding: '0.5rem 0.375rem', borderRadius: 'var(--radius-full)',
                      fontFamily: 'var(--font-body)', fontSize: '0.6875rem', fontWeight: stage === s ? 600 : 500,
                      cursor: 'pointer', transition: 'all 0.2s ease', border: 'none',
                      background: stage === s ? '#111111' : 'transparent',
                      color: stage === s ? '#FFFFFF' : '#555555',
                      boxShadow: stage === s ? '0 1px 4px rgba(0,0,0,0.12)' : 'none',
                    }}>{s}</button>
                  ))}
                </div>
              </div>

              {/* CTA */}
              <button
                className="btn-primary compute-btn"
                style={{ width: '100%', padding: '0.875rem', fontSize: '0.875rem', gap: '0.5rem' }}
                onClick={handleCompute}
                disabled={computing}
              >
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>
                  {computing ? 'hourglass_top' : 'bolt'}
                </span>
                <span>{computing ? 'Computing Analysis...' : 'Compute Recommendation'}</span>
                {!computing && <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>arrow_forward</span>}
              </button>
            </div>

            {/* RESULT PANEL */}
            <div ref={resultRef} className="glass" style={{
              borderRadius: 'var(--radius-xl)',
              padding: '1.75rem',
              opacity: 0, position: 'relative', overflow: 'hidden',
            }}>
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
                marginBottom: '1.5rem', paddingBottom: '1rem',
                borderBottom: '1px solid #E2E2DF', position: 'relative', zIndex: 1,
              }}>
                <div>
                  <span style={{
                    fontFamily: 'var(--font-body)', fontSize: '0.625rem', fontWeight: 600,
                    letterSpacing: '0.06em', textTransform: 'uppercase',
                    color: '#666666', display: 'block', marginBottom: '4px',
                  }}>Targeted Formulation</span>
                  <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 600, color: '#111111' }}>
                    Optimal Formulation Output
                  </h3>
                </div>
                <span className="material-symbols-outlined" style={{
                  color: '#111111', fontSize: '24px',
                  fontVariationSettings: "'FILL' 1",
                  animation: 'float 3s ease-in-out infinite',
                }}>psychology</span>
              </div>

              {/* Confidence Ring + Badge */}
              <div style={{
                background: '#FAFAF8', borderRadius: 'var(--radius-xl)',
                padding: '1.5rem', border: '1px solid #E2E2DF',
                display: 'flex', flexDirection: 'column', alignItems: 'center',
                gap: '1rem', marginBottom: '1.25rem', position: 'relative', zIndex: 1,
              }}>
                <ConfidenceRing value={99.1} />
                <div style={{
                  width: '100%', padding: '0.875rem 1rem',
                  borderRadius: 'var(--radius-lg)', background: '#FFFFFF',
                  border: '1px solid #E2E2DF',
                  textAlign: 'center',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.03)',
                }}>
                  <div style={{
                    fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 700,
                    color: '#111111', letterSpacing: '-0.02em',
                  }}>Urea (46-0-0) + Zinc Chelate</div>
                  <p style={{
                    fontFamily: 'var(--font-body)', fontSize: '0.75rem',
                    color: '#555555', marginTop: '4px',
                  }}>High nitrogen mobilization with micro-zinc chelation matrix</p>
                </div>
              </div>

              {/* Parameters Grid */}
              <div style={{ position: 'relative', zIndex: 1 }}>
                <span style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.625rem', fontWeight: 600,
                  color: '#777777', textTransform: 'uppercase', letterSpacing: '0.06em',
                  display: 'block', marginBottom: '0.75rem',
                }}>Telemetry Execution Matrix</span>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  {[
                    { label: 'Dosage Volume', value: '125 kg/ha', sub: 'Variable rate applied' },
                    { label: 'Application Window', value: 'Pre-irrigation', sub: '< 14h window' },
                  ].map(p => (
                    <div key={p.label} style={{
                      background: '#FAFAF8', padding: '0.75rem',
                      borderRadius: 'var(--radius-lg)', border: '1px solid #E2E2DF',
                    }}>
                      <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', color: '#777777', display: 'block' }}>{p.label}</span>
                      <span style={{ fontFamily: 'var(--font-display)', fontSize: '1rem', fontWeight: 600, color: '#111111', display: 'block', margin: '2px 0' }}>{p.value}</span>
                      <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', color: '#555555', display: 'block' }}>{p.sub}</span>
                    </div>
                  ))}
                </div>
                <div style={{
                  background: '#FAFAF8', padding: '0.875rem 1rem',
                  borderRadius: 'var(--radius-lg)', border: '1px solid #E2E2DF',
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  marginBottom: '1.25rem',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span className="material-symbols-outlined" style={{ color: '#111111', fontVariationSettings: "'FILL' 1" }}>grain</span>
                    <div>
                      <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.6875rem', color: '#666666', display: 'block' }}>Projected Yield Delta</span>
                      <span style={{ fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 700, color: '#111111' }}>+14.8 bu/acre</span>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', color: '#777777', display: 'block' }}>Net Margin Impact</span>
                    <span style={{ fontFamily: 'var(--font-display)', fontSize: '0.875rem', fontWeight: 600, color: '#111111' }}>+$42.20/ha</span>
                  </div>
                </div>

                {/* Status Pill */}
                <div style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  paddingTop: '0.875rem', borderTop: '1px solid #E2E2DF',
                }}>
                  <div className="badge badge-primary">
                    <span className="pulse-dot" />
                    VALIDATED & READY
                  </div>
                  <button className="btn-secondary" style={{ padding: '0.3rem 0.75rem', fontSize: '0.6875rem' }}>
                    Telemetry Audit
                    <span className="material-symbols-outlined" style={{ fontSize: '14px' }}>chevron_right</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <style>{`
            @media (max-width: 900px) {
              .analysis-grid { grid-template-columns: 1fr !important; }
            }
          `}</style>
        </section>

        {/* ===== RECENT RECOMMENDATIONS ===== */}
        <section ref={tableRef} className="glass" style={{
          borderRadius: 'var(--radius-xl)',
          padding: '1.75rem',
          marginBottom: '2rem',
        }}>
          <div style={{
            display: 'flex', flexWrap: 'wrap', alignItems: 'center',
            justifyContent: 'space-between', gap: '0.75rem',
            marginBottom: '1.5rem', paddingBottom: '1rem',
            borderBottom: '1px solid #E2E2DF',
          }}>
            <div>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.125rem', fontWeight: 600, color: '#111111' }}>
                Recent Recommendations
              </h2>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#666666', marginTop: '2px' }}>
                Total: {recommendations.length} inference logs across edge clusters
              </p>
            </div>
            {/* Filters */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
              <div style={{ position: 'relative' }}>
                <span className="material-symbols-outlined" style={{
                  position: 'absolute', left: '0.625rem', top: '50%', transform: 'translateY(-50%)',
                  color: '#777777', fontSize: '16px',
                }}>search</span>
                <input className="input" placeholder="Filter formula..." style={{
                  paddingLeft: '2rem', width: '170px', borderRadius: 'var(--radius-full)',
                  fontSize: '0.75rem', background: '#FAFAF8',
                }} />
              </div>
              {['all', 'Deployed'].map(f => (
                <button key={f} onClick={() => setFilter(f)} style={{
                  padding: '0.375rem 0.875rem', borderRadius: 'var(--radius-full)',
                  fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: filter === f ? 600 : 500,
                  cursor: 'pointer', border: 'none', transition: 'all 0.2s',
                  background: filter === f ? '#111111' : '#F0F0EC',
                  color: filter === f ? '#FFFFFF' : '#555555',
                  boxShadow: filter === f ? '0 1px 4px rgba(0,0,0,0.12)' : 'none',
                }}>{f === 'all' ? 'All Logs' : 'Deployed Only'}</button>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
            {filtered.map((rec, i) => (
              <div key={rec.id}
                ref={el => { if (el) rowsRef.current[i] = el }}
                className="data-row"
                style={{
                  padding: '1rem 1.25rem',
                  display: 'flex', flexWrap: 'wrap',
                  alignItems: 'center', justifyContent: 'space-between',
                  gap: '0.875rem',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
                  <div style={{
                    width: '36px', height: '36px', borderRadius: 'var(--radius-md)',
                    background: '#F0F0EC',
                    border: '1px solid #E2E2DF',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                  }}>
                    <span className="material-symbols-outlined" style={{
                      color: '#111111',
                      fontSize: '18px', fontVariationSettings: "'FILL' 1",
                    }}>{rec.status === 'Deployed' ? 'check_circle' : 'pending'}</span>
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', flexWrap: 'wrap' }}>
                      <span style={{
                        fontFamily: 'monospace', fontSize: '0.75rem',
                        color: '#777777', fontWeight: 500,
                      }}>{rec.id}</span>
                      <span style={{
                        fontFamily: 'var(--font-body)', fontSize: '0.875rem', fontWeight: 600,
                        color: '#111111',
                      }}>{rec.formula}</span>
                      <span style={{
                        fontFamily: 'var(--font-body)', fontSize: '0.6875rem', fontWeight: 600,
                        background: '#F0F0EC', color: '#111111',
                        border: '1px solid #E2E2DF',
                        padding: '0.125rem 0.5rem', borderRadius: 'var(--radius-full)',
                      }}>{rec.conf}% conf</span>
                    </div>
                    <p style={{
                      fontFamily: 'var(--font-body)', fontSize: '0.6875rem',
                      color: '#666666', marginTop: '3px',
                      display: 'flex', gap: '0.5rem',
                    }}>
                      <span>{rec.time}</span>
                      <span>·</span>
                      <span style={{ fontFamily: 'monospace', color: '#777777' }}>Latency: {rec.latency}</span>
                    </p>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span className="badge badge-primary">
                    <span className="pulse-dot" />
                    {rec.status}
                  </span>
                  <button className="btn-secondary" style={{ padding: '0.3rem 0.875rem', fontSize: '0.75rem' }}>
                    Inspect
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            marginTop: '1.25rem', paddingTop: '1rem',
            borderTop: '1px solid #E2E2DF',
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#666666',
          }}>
            <span>Page 1 of 54</span>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button className="btn-secondary" style={{ padding: '0.3rem 0.875rem', fontSize: '0.75rem' }}>Previous</button>
              <button className="btn-secondary" style={{ padding: '0.3rem 0.875rem', fontSize: '0.75rem' }}>Next</button>
            </div>
          </div>
        </section>

        {/* ===== SYSTEM HEALTH ===== */}
        <section className="glass" style={{ borderRadius: 'var(--radius-xl)', padding: '1.25rem' }}>
          <div ref={healthRef} style={{
            display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '0.875rem',
          }} className="health-grid">
            {healthMetrics.map((m, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.625rem 0.875rem',
                background: '#FAFAF8', borderRadius: 'var(--radius-lg)', border: '1px solid #E2E2DF',
              }}>
                <span className="material-symbols-outlined" style={{
                  color: '#111111', fontSize: '20px',
                  fontVariationSettings: "'FILL' 1",
                }}>{m.icon}</span>
                <div>
                  <span style={{
                    fontFamily: 'var(--font-body)', fontSize: '0.5625rem', fontWeight: 600,
                    letterSpacing: '0.06em', textTransform: 'uppercase', color: '#777777', display: 'block',
                  }}>{m.label}</span>
                  <span style={{
                    fontFamily: 'var(--font-display)', fontSize: '0.9375rem', fontWeight: 700,
                    color: '#111111',
                  }}>{m.value}</span>
                </div>
              </div>
            ))}
          </div>
          <style>{`
            @media (max-width: 640px) {
              .health-grid { grid-template-columns: 1fr 1fr !important; }
            }
          `}</style>
        </section>

        {/* Footer */}
        <footer style={{
          marginTop: '2.5rem', paddingTop: '1.5rem',
          borderTop: '1px solid #E2E2DF',
          display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center',
          gap: '1rem',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="material-symbols-outlined" style={{ color: '#111111', fontSize: '18px', fontVariationSettings: "'FILL' 1" }}>eco</span>
            <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#666666' }}>
              © 2025 Fieldwise Fertilizer Intelligence · Real-time inference cluster v2.4.8 active
            </p>
          </div>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            {['API Status', 'Model Telemetry', 'Documentation', 'System Logs'].map(l => (
              <a key={l} href="#" style={{
                fontFamily: 'var(--font-body)', fontSize: '0.75rem',
                color: '#666666', textDecoration: 'none',
                transition: 'color 0.2s',
              }}
                onMouseEnter={e => (e.currentTarget.style.color = '#111111')}
                onMouseLeave={e => (e.currentTarget.style.color = '#666666')}
              >{l}</a>
            ))}
          </div>
        </footer>

      </div>
    </main>
  )
}

