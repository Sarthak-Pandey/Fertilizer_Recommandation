import { useRef, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { gsap } from 'gsap'
import { useAuth } from '../../context/AuthContext'

export default function LandingNavbar() {
  const { isAuthenticated } = useAuth()
  const navRef = useRef<HTMLElement>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    if (navRef.current) {
      gsap.fromTo(
        navRef.current,
        { y: -30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.9, delay: 0.1, ease: 'power3.out' }
      )
    }
  }, [])

  const scrollToSection = (id: string) => {
    setMobileMenuOpen(false)
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <header
      ref={navRef}
      style={{
        position: 'fixed',
        top: '1.25rem',
        left: 0,
        right: 0,
        zIndex: 999,
        padding: '0 1.5rem',
        pointerEvents: 'none',
        opacity: 0,
      }}
    >
      <div
        style={{
          maxWidth: '1280px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          pointerEvents: 'auto',
          gap: '1rem',
        }}
      >
        {/* LEFT NAV PILL */}
        <div
          className="floating-pill-nav desktop-only"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1.25rem',
            padding: '0.45rem 1.25rem',
            borderRadius: '9999px',
          }}
        >
          <button
            onClick={() => scrollToSection('features')}
            style={{
              background: 'none',
              border: 'none',
              color: '#444444',
              fontFamily: 'var(--font-body)',
              fontSize: '0.8125rem',
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'color 0.2s ease, transform 0.2s ease',
              padding: '0.2rem 0.25rem',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#111111')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#444444')}
          >
            Product
          </button>
          <button
            onClick={() => scrollToSection('architecture')}
            style={{
              background: 'none',
              border: 'none',
              color: '#444444',
              fontFamily: 'var(--font-body)',
              fontSize: '0.8125rem',
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'color 0.2s ease, transform 0.2s ease',
              padding: '0.2rem 0.25rem',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#111111')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#444444')}
          >
            Architecture
          </button>
          <button
            onClick={() => scrollToSection('research')}
            style={{
              background: 'none',
              border: 'none',
              color: '#444444',
              fontFamily: 'var(--font-body)',
              fontSize: '0.8125rem',
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'color 0.2s ease, transform 0.2s ease',
              padding: '0.2rem 0.25rem',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#111111')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#444444')}
          >
            Research
          </button>
        </div>

        {/* CENTER BRAND PILL */}
        <div
          className="floating-pill-nav"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.625rem',
            padding: '0.45rem 1.5rem',
            borderRadius: '9999px',
          }}
        >
          <div
            style={{
              width: '26px',
              height: '26px',
              borderRadius: '7px',
              overflow: 'hidden',
              background: '#111111',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
            }}
          >
            <img src="/logo.png" alt="Fieldwise Logo" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          </div>
          <span
            style={{
              fontFamily: 'var(--font-body)',
              fontWeight: 600,
              fontSize: '0.9375rem',
              color: '#111111',
              letterSpacing: '-0.015em',
            }}
          >
            Fieldwise
          </span>
        </div>

        {/* RIGHT ACTION PILL */}
        <div
          className="floating-pill-nav desktop-only"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '0.35rem 0.35rem 0.35rem 1.25rem',
            borderRadius: '9999px',
          }}
        >
          {isAuthenticated ? (
            <Link
              to="/overview"
              style={{
                background: '#111111',
                color: '#FFFFFF',
                padding: '0.45rem 1.25rem',
                borderRadius: '9999px',
                fontFamily: 'var(--font-body)',
                fontSize: '0.8125rem',
                fontWeight: 600,
                textDecoration: 'none',
                transition: 'all 0.2s ease',
              }}
            >
              Open Dashboard
            </Link>
          ) : (
            <>
              <Link
                to="/login"
                style={{
                  color: '#444444',
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.8125rem',
                  fontWeight: 500,
                  textDecoration: 'none',
                  transition: 'color 0.2s ease',
                  padding: '0.2rem 0.5rem',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.color = '#111111')}
                onMouseLeave={(e) => (e.currentTarget.style.color = '#444444')}
              >
                Sign In
              </Link>
              <Link
                to="/register"
                style={{
                  background: '#111111',
                  color: '#FFFFFF',
                  padding: '0.45rem 1.25rem',
                  borderRadius: '9999px',
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.8125rem',
                  fontWeight: 600,
                  textDecoration: 'none',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                }}
              >
                Get Started
              </Link>
            </>
          )}
        </div>

        {/* MOBILE TOGGLE BUTTON */}
        <button
          className="mobile-only floating-pill-nav"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={{
            display: 'none',
            padding: '0.5rem 0.75rem',
            borderRadius: '9999px',
            border: 'none',
            color: '#111111',
            cursor: 'pointer',
          }}
          aria-label="Toggle Menu"
        >
          <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>
            {mobileMenuOpen ? 'close' : 'menu'}
          </span>
        </button>
      </div>

      {/* MOBILE MENU DROPDOWN */}
      {mobileMenuOpen && (
        <div
          className="floating-pill-nav"
          style={{
            margin: '0.75rem 1.5rem 0',
            padding: '1.25rem',
            borderRadius: '1.25rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            pointerEvents: 'auto',
          }}
        >
          <button
            onClick={() => scrollToSection('features')}
            style={{
              background: 'none',
              border: 'none',
              textAlign: 'left',
              color: '#111111',
              fontFamily: 'var(--font-body)',
              fontSize: '0.9375rem',
              fontWeight: 500,
            }}
          >
            Product Features
          </button>
          <button
            onClick={() => scrollToSection('architecture')}
            style={{
              background: 'none',
              border: 'none',
              textAlign: 'left',
              color: '#111111',
              fontFamily: 'var(--font-body)',
              fontSize: '0.9375rem',
              fontWeight: 500,
            }}
          >
            System Architecture
          </button>
          <button
            onClick={() => scrollToSection('research')}
            style={{
              background: 'none',
              border: 'none',
              textAlign: 'left',
              color: '#111111',
              fontFamily: 'var(--font-body)',
              fontSize: '0.9375rem',
              fontWeight: 500,
            }}
          >
            Agronomic Research
          </button>
          <hr style={{ border: 'none', borderTop: '1px solid rgba(0,0,0,0.08)' }} />
          {isAuthenticated ? (
            <Link
              to="/overview"
              style={{
                background: '#111111',
                color: '#FFFFFF',
                padding: '0.625rem',
                borderRadius: '9999px',
                fontFamily: 'var(--font-body)',
                fontSize: '0.875rem',
                fontWeight: 600,
                textAlign: 'center',
                textDecoration: 'none',
              }}
            >
              Open Dashboard
            </Link>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <Link
                to="/register"
                style={{
                  background: '#111111',
                  color: '#FFFFFF',
                  padding: '0.625rem',
                  borderRadius: '9999px',
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  textAlign: 'center',
                  textDecoration: 'none',
                }}
              >
                Get Started
              </Link>
              <Link
                to="/login"
                style={{
                  background: 'transparent',
                  color: '#111111',
                  border: '1px solid rgba(0,0,0,0.2)',
                  padding: '0.625rem',
                  borderRadius: '9999px',
                  fontFamily: 'var(--font-body)',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  textAlign: 'center',
                  textDecoration: 'none',
                }}
              >
                Sign In
              </Link>
            </div>
          )}
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .desktop-only { display: none !important; }
          .mobile-only { display: flex !important; }
        }
      `}</style>
    </header>
  )
}
