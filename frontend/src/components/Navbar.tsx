import { useRef, useEffect, useState } from 'react'
import { NavLink, Link, useNavigate, useLocation } from 'react-router-dom'
import { gsap } from 'gsap'
import { useAuth } from '../context/AuthContext'

const navLinks = [
  { to: '/overview', label: 'Overview' },
  { to: '/history', label: 'Prediction History' },
  { to: '/audit', label: 'Model Audit' },
]

export default function Navbar() {
  const location = useLocation()
  const barRef = useRef<HTMLElement>(null)
  const logoRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()
  const [showDropdown, setShowDropdown] = useState(false)

  useEffect(() => {
    if (barRef.current) {
      gsap.fromTo(
        barRef.current,
        { y: -80, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
      )
    }
    if (logoRef.current) {
      gsap.fromTo(
        logoRef.current,
        { x: -20, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.6, delay: 0.2, ease: 'power2.out' }
      )
    }
  }, [location.pathname])

  const handleLogout = () => {
    logout()
    setShowDropdown(false)
    navigate('/login')
  }

  if (location.pathname === '/login' || location.pathname === '/register') {
    return null
  }

  return (
    <header ref={barRef} className="navbar" style={{ opacity: 0, position: 'relative', zIndex: 100 }}>
      <div className="container">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>

          {/* Brand */}
          <Link to="/overview" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
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
          </Link>

          {/* Desktop Nav Pills */}
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
            <div className="badge badge-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
              <span className="pulse-dot" />
              <span>SYSTEM ONLINE</span>
            </div>

            {/* Auth Actions / User Menu */}
            {isAuthenticated ? (
              <div style={{ position: 'relative' }}>
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  style={{
                    background: '#EAEAE6', border: '1px solid #D1D1CB',
                    borderRadius: 'var(--radius-full)',
                    padding: '0.25rem 0.75rem 0.25rem 0.375rem',
                    display: 'flex', alignItems: 'center', gap: '0.5rem',
                    cursor: 'pointer', transition: 'all 0.2s ease',
                  }}
                  onMouseEnter={e => (e.currentTarget.style.borderColor = '#111111')}
                  onMouseLeave={e => (e.currentTarget.style.borderColor = '#D1D1CB')}
                >
                  <div style={{
                    width: '28px', height: '28px', borderRadius: '50%',
                    background: '#111111', color: '#FFFFFF',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 600,
                  }}>
                    {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#111111' }}>
                    {user?.full_name || 'User'}
                  </span>
                  <span className="material-symbols-outlined" style={{ fontSize: '18px', color: '#666666' }}>
                    {showDropdown ? 'expand_less' : 'expand_more'}
                  </span>
                </button>

                {/* Dropdown Menu */}
                {showDropdown && (
                  <div className="glass" style={{
                    position: 'absolute', right: 0, top: 'calc(100% + 8px)',
                    width: '220px', borderRadius: 'var(--radius-lg)',
                    padding: '0.75rem', boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
                    border: '1px solid var(--border-color)', zIndex: 1000,
                  }}>
                    <div style={{ padding: '0.5rem', borderBottom: '1px solid #E2E2DF', marginBottom: '0.5rem' }}>
                      <div style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#111111' }}>
                        {user?.full_name}
                      </div>
                      <div style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#666666', marginTop: '2px', wordBreak: 'break-all' }}>
                        {user?.email}
                      </div>
                      {user?.role && (
                        <div style={{
                          marginTop: '6px', display: 'inline-block',
                          padding: '2px 6px', borderRadius: '4px',
                          background: '#EAEAE6', color: '#333333',
                          fontFamily: 'var(--font-body)', fontSize: '0.6875rem', fontWeight: 600,
                          textTransform: 'capitalize',
                        }}>
                          {user.role}
                        </div>
                      )}
                    </div>
                    <button
                      onClick={handleLogout}
                      style={{
                        width: '100%', padding: '0.5rem 0.75rem',
                        borderRadius: 'var(--radius-md)', border: 'none',
                        background: '#FFF5F5', color: '#C53030',
                        fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600,
                        display: 'flex', alignItems: 'center', gap: '0.5rem',
                        cursor: 'pointer', transition: 'background-color 0.2s ease',
                      }}
                      onMouseEnter={e => (e.currentTarget.style.background = '#FED7D7')}
                      onMouseLeave={e => (e.currentTarget.style.background = '#FFF5F5')}
                    >
                      <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>logout</span>
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Link
                  to="/login"
                  style={{
                    padding: '0.375rem 0.875rem', borderRadius: 'var(--radius-full)',
                    fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600,
                    color: '#111111', textDecoration: 'none', background: 'transparent',
                    border: '1px solid #D1D1CB', transition: 'all 0.2s ease',
                  }}
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  style={{
                    padding: '0.375rem 0.875rem', borderRadius: 'var(--radius-full)',
                    fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600,
                    color: '#FFFFFF', textDecoration: 'none', background: '#111111',
                    border: '1px solid #111111', transition: 'all 0.2s ease',
                  }}
                >
                  Register
                </Link>
              </div>
            )}
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
