import { useRef, useEffect } from 'react'
import { NavLink } from 'react-router-dom'
import { gsap } from 'gsap'

const navLinks = [
  { to: '/', label: 'Overview' },
  { to: '/history', label: 'Prediction History' },
  { to: '/audit', label: 'Model Audit' },
]

export default function Navbar() {
  const barRef = useRef<HTMLElement>(null)
  const logoRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    gsap.fromTo(
      barRef.current,
      { y: -80, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
    )
    gsap.fromTo(
      logoRef.current,
      { x: -20, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.6, delay: 0.2, ease: 'power2.out' }
    )
  }, [])

  return (
    <header ref={barRef} className="navbar" style={{ opacity: 0 }}>
      <div className="container">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>

          {/* Brand */}
          <div ref={logoRef} style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
            <div style={{
              width: '36px', height: '36px', borderRadius: '10px',
              background: '#111111',
              border: '1px solid #111111',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 2px 6px rgba(0,0,0,0.12)',
            }}>
              <span className="material-symbols-outlined" style={{
                color: '#FFFFFF',
                fontSize: '20px',
                fontVariationSettings: "'FILL' 1"
              }}>eco</span>
            </div>
            <div>
              <div style={{
                fontFamily: 'var(--font-display)',
                fontSize: '1rem', fontWeight: 600,
                color: '#111111',
                letterSpacing: '-0.02em', lineHeight: 1.1,
              }}>Fieldwise</div>
              <div style={{
                fontFamily: 'var(--font-body)',
                fontSize: '0.625rem', fontWeight: 600,
                color: '#666666',
                letterSpacing: '0.08em', textTransform: 'uppercase',
              }}>Fertilizer Intelligence</div>
            </div>
          </div>

          {/* Desktop Nav Pills (Antimetal inspired soft container) */}
          <nav style={{ display: 'flex', alignItems: 'center', gap: '4px',
            background: '#EAEAE6', padding: '4px',
            borderRadius: 'var(--radius-full)',
            border: '1px solid #E2E2DF',
          }} className="desktop-nav">
            {navLinks.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end
                style={({ isActive }) => ({
                  padding: '0.375rem 1rem',
                  borderRadius: 'var(--radius-full)',
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.8125rem', fontWeight: isActive ? 600 : 500,
                  textDecoration: 'none',
                  transition: 'all 0.2s ease',
                  background: isActive ? '#111111' : 'transparent',
                  color: isActive ? '#FFFFFF' : '#555555',
                  boxShadow: isActive ? '0 1px 4px rgba(0,0,0,0.12)' : 'none',
                })}
              >
                {label}
              </NavLink>
            ))}
          </nav>

          {/* Trailing Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            {/* Status Badge */}
            <div className="badge badge-primary">
              <span className="pulse-dot" />
              FASTAPI ACTIVE
            </div>

            {/* User Avatar */}
            <div style={{
              position: 'relative', cursor: 'pointer',
              width: '36px', height: '36px',
            }}>
              <div style={{
                width: '36px', height: '36px', borderRadius: '50%',
                border: '1px solid #E2E2DF',
                overflow: 'hidden',
                background: '#FFFFFF',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
              }}>
                <span className="material-symbols-outlined" style={{
                  color: '#111111', fontSize: '20px',
                  fontVariationSettings: "'FILL' 1"
                }}>person</span>
              </div>
              <span style={{
                position: 'absolute', bottom: '0', right: '0',
                width: '9px', height: '9px', borderRadius: '50%',
                background: '#111111',
                border: '2px solid var(--canvas)',
              }} />
            </div>
          </div>

        </div>
      </div>
      <style>{`
        @media (max-width: 768px) {
          .desktop-nav { display: none !important; }
        }
      `}</style>
    </header>
  )
}

