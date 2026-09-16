import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { gsap } from 'gsap'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register, isAuthenticated } = useAuth()

  const cardRef = useRef<HTMLDivElement>(null)

  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('farmer')
  const [organization, setOrganization] = useState('')
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
    if (!email || !password || !fullName) {
      setErrorMsg('Please fill in all required fields.')
      return
    }

    if (password.length < 8) {
      setErrorMsg('Password must be at least 8 characters long.')
      return
    }

    setIsSubmitting(true)
    setErrorMsg(null)

    try {
      await register({
        email,
        password,
        full_name: fullName,
        role,
        organization: organization.trim() || undefined,
      })
      navigate('/overview')
    } catch (err: any) {
      setErrorMsg(err.message || 'Registration failed. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem 1rem' }}>
      <div ref={cardRef} className="glass" style={{
        width: '100%', maxWidth: '480px',
        borderRadius: 'var(--radius-xl)',
        padding: '2.5rem 2rem',
        boxShadow: '0 8px 30px rgba(0,0,0,0.06)',
      }}>
        {/* Brand Logo & Header */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '48px', height: '48px', borderRadius: '12px',
            background: '#111111', margin: '0 auto 1rem auto',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}>
            <span className="material-symbols-outlined" style={{ color: '#FFFFFF', fontSize: '26px', fontVariationSettings: "'FILL' 1" }}>person_add</span>
          </div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.75rem', fontWeight: 700, color: '#111111', letterSpacing: '-0.02em' }}>
            Create an Account
          </h1>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.875rem', color: '#666666', marginTop: '4px' }}>
            Join Fieldwise to access intelligent agricultural decision support
          </p>
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

        {/* Registration Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div>
            <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#333333', marginBottom: '0.375rem' }}>
              Full Name <span style={{ color: '#E53E3E' }}>*</span>
            </label>
            <div style={{ position: 'relative' }}>
              <span className="material-symbols-outlined" style={{
                position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)',
                color: '#888888', fontSize: '20px', pointerEvents: 'none',
              }}>
                badge
              </span>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Dr. Jane Doe"
                style={{
                  width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem',
                  borderRadius: 'var(--radius-md)', border: '1px solid #D1D1CB',
                  background: '#FFFFFF', fontFamily: 'var(--font-body)', fontSize: '0.875rem',
                  outline: 'none', transition: 'border-color 0.2s ease',
                }}
                onFocus={(e) => (e.target.style.borderColor = '#111111')}
                onBlur={(e) => (e.target.style.borderColor = '#D1D1CB')}
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#333333', marginBottom: '0.375rem' }}>
              Email Address <span style={{ color: '#E53E3E' }}>*</span>
            </label>
            <div style={{ position: 'relative' }}>
              <span className="material-symbols-outlined" style={{
                position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)',
                color: '#888888', fontSize: '20px', pointerEvents: 'none',
              }}>
                mail
              </span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="agronomist@farm.com"
                style={{
                  width: '100%', padding: '0.75rem 0.75rem 0.75rem 2.5rem',
                  borderRadius: 'var(--radius-md)', border: '1px solid #D1D1CB',
                  background: '#FFFFFF', fontFamily: 'var(--font-body)', fontSize: '0.875rem',
                  outline: 'none', transition: 'border-color 0.2s ease',
                }}
                onFocus={(e) => (e.target.style.borderColor = '#111111')}
                onBlur={(e) => (e.target.style.borderColor = '#D1D1CB')}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#333333', marginBottom: '0.375rem' }}>
                Primary Role
              </label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{
                  width: '100%', padding: '0.75rem',
                  borderRadius: 'var(--radius-md)', border: '1px solid #D1D1CB',
                  background: '#FFFFFF', fontFamily: 'var(--font-body)', fontSize: '0.875rem',
                  outline: 'none', cursor: 'pointer',
                }}
              >
                <option value="farmer">Farmer / Grower</option>
                <option value="agronomist">Agronomist</option>
                <option value="researcher">Agricultural Researcher</option>
                <option value="consultant">Crop Consultant</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#333333', marginBottom: '0.375rem' }}>
                Organization
              </label>
              <input
                type="text"
                value={organization}
                onChange={(e) => setOrganization(e.target.value)}
                placeholder="Acme Agri Farms"
                style={{
                  width: '100%', padding: '0.75rem',
                  borderRadius: 'var(--radius-md)', border: '1px solid #D1D1CB',
                  background: '#FFFFFF', fontFamily: 'var(--font-body)', fontSize: '0.875rem',
                  outline: 'none', transition: 'border-color 0.2s ease',
                }}
                onFocus={(e) => (e.target.style.borderColor = '#111111')}
                onBlur={(e) => (e.target.style.borderColor = '#D1D1CB')}
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', fontWeight: 600, color: '#333333', marginBottom: '0.375rem' }}>
              Password <span style={{ color: '#E53E3E' }}>*</span>
            </label>
            <div style={{ position: 'relative' }}>
              <span className="material-symbols-outlined" style={{
                position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)',
                color: '#888888', fontSize: '20px', pointerEvents: 'none',
              }}>
                lock
              </span>
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Min 8 characters"
                style={{
                  width: '100%', padding: '0.75rem 2.5rem 0.75rem 2.5rem',
                  borderRadius: 'var(--radius-md)', border: '1px solid #D1D1CB',
                  background: '#FFFFFF', fontFamily: 'var(--font-body)', fontSize: '0.875rem',
                  outline: 'none', transition: 'border-color 0.2s ease',
                }}
                onFocus={(e) => (e.target.style.borderColor = '#111111')}
                onBlur={(e) => (e.target.style.borderColor = '#D1D1CB')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)',
                  background: 'none', border: 'none', cursor: 'pointer', color: '#888888', display: 'flex',
                }}
              >
                <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>
                  {showPassword ? 'visibility_off' : 'visibility'}
                </span>
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            style={{
              width: '100%', padding: '0.875rem',
              borderRadius: 'var(--radius-md)',
              background: '#111111', color: '#FFFFFF',
              fontFamily: 'var(--font-body)', fontSize: '0.875rem', fontWeight: 600,
              border: 'none', cursor: isSubmitting ? 'not-allowed' : 'pointer',
              opacity: isSubmitting ? 0.7 : 1, marginTop: '0.5rem',
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              transition: 'background-color 0.2s ease',
            }}
            onMouseEnter={e => !isSubmitting && (e.currentTarget.style.background = '#222222')}
            onMouseLeave={e => !isSubmitting && (e.currentTarget.style.background = '#111111')}
          >
            {isSubmitting ? (
              <>
                <span className="material-symbols-outlined" style={{ animation: 'spin 1s linear infinite', fontSize: '20px' }}>sync</span>
                Creating account...
              </>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        {/* Navigation Link */}
        <div style={{ textAlign: 'center', marginTop: '1.75rem', fontFamily: 'var(--font-body)', fontSize: '0.8125rem', color: '#666666' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#111111', fontWeight: 600, textDecoration: 'none' }}>
            Sign In
          </Link>
        </div>
      </div>
    </main>
  )
}
