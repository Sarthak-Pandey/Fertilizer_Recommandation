import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function LandingFooter() {
  const { isAuthenticated } = useAuth()

  return (
    <footer
      style={{
        borderTop: '1px solid rgba(17, 17, 17, 0.1)',
        padding: '4rem 2rem 3rem',
        maxWidth: '1380px',
        margin: '0 auto',
        fontFamily: 'var(--font-body)',
      }}
    >
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: '3rem',
          marginBottom: '4rem',
        }}
      >
        {/* BRAND & DESCRIPTION */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '1rem' }}>
            <div
              style={{
                width: '28px',
                height: '28px',
                borderRadius: '8px',
                overflow: 'hidden',
                background: '#111111',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <img src="/logo.png" alt="Fieldwise Logo" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
            <span style={{ fontWeight: 600, fontSize: '1.125rem', color: '#111111', letterSpacing: '-0.02em' }}>
              Fieldwise
            </span>
          </div>
          <p style={{ fontSize: '0.875rem', color: '#666666', lineHeight: 1.6, maxWidth: '300px' }}>
            Precision agricultural intelligence powered by ensemble machine learning models for optimal soil nutrition.
          </p>
        </div>

        {/* NAVIGATION LINKS */}
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#888888', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
            NAVIGATION
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem', fontSize: '0.875rem' }}>
            <a href="#features" style={{ color: '#333333', textDecoration: 'none' }}>
              System Capabilities
            </a>
            <a href="#architecture" style={{ color: '#333333', textDecoration: 'none' }}>
              Ensemble Architecture
            </a>
            <a href="#research" style={{ color: '#333333', textDecoration: 'none' }}>
              Yield Metrics
            </a>
          </div>
        </div>

        {/* ACCESS / APP */}
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#888888', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
            APPLICATION
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem', fontSize: '0.875rem' }}>
            {isAuthenticated ? (
              <Link to="/overview" style={{ color: '#111111', fontWeight: 600, textDecoration: 'none' }}>
                Go to App Dashboard →
              </Link>
            ) : (
              <>
                <Link to="/login" style={{ color: '#333333', textDecoration: 'none' }}>
                  Sign In
                </Link>
                <Link to="/register" style={{ color: '#333333', textDecoration: 'none' }}>
                  Register Account
                </Link>
              </>
            )}
          </div>
        </div>

        {/* SYSTEM STATUS */}
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#888888', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
            STATUS & ENGINE
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10B981' }} />
            <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#111111' }}>Models Operational</span>
          </div>
          <div style={{ fontSize: '0.8125rem', color: '#666666' }}>
            XGBoost Ensemble v2.4 · Inference Active
          </div>
        </div>
      </div>

      {/* BOTTOM COPYRIGHT */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderTop: '1px solid rgba(17, 17, 17, 0.06)',
          paddingTop: '1.75rem',
          fontSize: '0.8125rem',
          color: '#888888',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>© {new Date().getFullYear()} Fieldwise Inc. Autonomous Fertilizer Intelligence.</div>
        <div>Designed with Editorial Precision.</div>
      </div>
    </footer>
  )
}
