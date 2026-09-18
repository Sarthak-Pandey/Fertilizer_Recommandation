import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { gsap } from 'gsap'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login, register, isAuthenticated } = useAuth()

  const cardRef = useRef<HTMLDivElement>(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/overview')
    }
  }, [isAuthenticated, navigate])

  useEffect(() => {
    if (cardRef.current) {
      gsap.fromTo(
        cardRef.current,
        { opacity: 0, y: 25, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'power3.out' }
      )
    }
  }, [])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!email || !password) {
      setErrorMsg('Please enter both email and password.')
      return
    }

    setIsSubmitting(true)
    setErrorMsg(null)

    try {
      await login({ email, password })
      navigate('/overview')
    } catch (err: any) {
      setErrorMsg(err.message || 'Login failed. Please check your credentials.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleQuickDemoLogin = async () => {
    setIsSubmitting(true)
    setErrorMsg(null)
    const demoEmail = `demo.farmer.${Math.floor(Math.random() * 10000)}@gmail.com`
    const demoPass = 'DemoPassword123!'

    try {
      await register({
        email: demoEmail,
        password: demoPass,
        full_name: 'Demo Farmer',
        role: 'farmer',
        organization: 'Fieldwise Experimental Farm',
      })
      navigate('/overview')
    } catch {
      // Fallback try standard demo credentials
      try {
        await login({ email: 'sarthak.pandey@gmail.com', password: 'Password123!' })
        navigate('/overview')
      } catch (err: any) {
        setErrorMsg(err.message || 'Quick demo authentication failed.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem 1rem' }}>
      <div ref={cardRef} className="glass" style={{
        width: '100%', maxWidth: '440px',
        borderRadius: 'var(--radius-xl)',
        padding: '2.5rem 2rem',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
      }}>
        {/* Brand Logo & Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '48px', height: '48px', borderRadius: '12px',
            overflow: 'hidden',
            background: '#111111', margin: '0 auto 1rem auto',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}>
            <img src="/logo.png" alt="Fieldwise Logo" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.75rem', fontWeight: 700, color: '#111111', letterSpacing: '-0.02em' }}>
            Welcome Back
          </h1>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.875rem', color: '#666666', marginTop: '4px' }}>
            Sign in to access your autonomous fertilizer telemetry
          </p>
        </div>

        {/* Quick Demo Login CTA */}
        <div style={{ marginBottom: '1.5rem' }}>
          <button
            type="button"
            onClick={handleQuickDemoLogin}
            disabled={isSubmitting}
            style={{
              width: '100%', padding: '0.75rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid #111111',
              background: '#F0F0EC', color: '#111111',
              fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600,
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem',
              cursor: 'pointer', transition: 'all 0.2s ease',
            }}
            onMouseEnter={e => (e.currentTarget.style.background = '#E6E6E2')}
            onMouseLeave={e => (e.currentTarget.style.background = '#F0F0EC')}
          >
            <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>bolt</span>
            Instant 1-Click Demo Sign In
          </button>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '1rem',
            margin: '1.25rem 0 0.5rem 0', color: '#888888',
            fontFamily: 'var(--font-body)', fontSize: '0.75rem',
          }}>
            <div style={{ flex: 1, height: '1px', background: '#E2E2DF' }} />
            <span>or sign in with email</span>
            <div style={{ flex: 1, height: '1px', background: '#E2E2DF' }} />
          </div>
        </div>

        {/* Error Banner */}
        {errorMsg && (
          <div style={{
            padding: '0.75rem 1rem', borderRadius: 'var(--radius-md)',
            background: '#FFF5F5', border: '1px solid #FEB2B2',
            color: '#C53030', fontFamily: 'var(--font-body)', fontSize: '0.8125rem',
            marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem',
          }}>
            <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>error</span>
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Email */}
          <div>
            <label style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#111111', display: 'block', marginBottom: '0.375rem' }}>
              Email Address
            </label>
            <div style={{ position: 'relative' }}>
              <span className="material-symbols-outlined" style={{
                position: 'absolute', left: '0.875rem', top: '50%', transform: 'translateY(-50%)',
                color: '#777777', fontSize: '18px',
              }}>mail</span>
              <input
                type="email"
                required
                placeholder="farmer@example.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="input"
                style={{ paddingLeft: '2.5rem', width: '100%' }}
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#111111', display: 'block', marginBottom: '0.375rem' }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <span className="material-symbols-outlined" style={{
                position: 'absolute', left: '0.875rem', top: '50%', transform: 'translateY(-50%)',
                color: '#777777', fontSize: '18px',
              }}>lock</span>
              <input
                type={showPassword ? 'text' : 'password'}
                required
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="input"
                style={{ paddingLeft: '2.5rem', paddingRight: '2.5rem', width: '100%' }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute', right: '0.75rem', top: '50%', transform: 'translateY(-50%)',
                  background: 'none', border: 'none', cursor: 'pointer', color: '#777777',
                  display: 'flex', alignItems: 'center',
                }}
              >
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>
                  {showPassword ? 'visibility_off' : 'visibility'}
                </span>
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="btn-primary"
            style={{ width: '100%', padding: '0.875rem', fontSize: '0.875rem', marginTop: '0.5rem', justifyContent: 'center' }}
          >
            {isSubmitting ? (
              <>
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>hourglass_top</span>
                <span>Signing In...</span>
              </>
            ) : (
              <>
                <span>Sign In</span>
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>arrow_forward</span>
              </>
            )}
          </button>
        </form>

        {/* Footer Link */}
        <div style={{ textAlign: 'center', marginTop: '1.75rem', paddingTop: '1.25rem', borderTop: '1px solid #E2E2DF' }}>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.8125rem', color: '#666666' }}>
            Don't have an account?{' '}
            <Link to="/register" style={{ color: '#111111', fontWeight: 600, textDecoration: 'none' }}>
              Create Account
            </Link>
          </p>
        </div>
      </div>
    </main>
  )
}
