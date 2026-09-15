import { NavLink } from 'react-router-dom'

const tabs = [
  { to: '/overview', icon: 'dashboard', label: 'Overview' },
  { to: '/history', icon: 'science', label: 'History' },
  { to: '/audit', icon: 'monitor_heart', label: 'Audit' },
]

export default function MobileNav() {
  return (
    <nav className="mobile-nav">
      {tabs.map(({ to, icon, label }) => (
        <NavLink
          key={to}
          to={to}
          end
          style={({ isActive }) => ({
            display: 'flex', flexDirection: 'column',
            alignItems: 'center', justifyContent: 'center',
            gap: '2px', textDecoration: 'none',
            padding: '0.4rem 0.875rem',
            borderRadius: 'var(--radius-full)',
            color: isActive ? '#FFFFFF' : '#555555',
            background: isActive ? '#111111' : 'transparent',
            transition: 'all 0.2s ease',
          })}
        >
          <span className="material-symbols-outlined" style={{
            fontSize: '20px',
            fontVariationSettings: "'FILL' 1",
          }}>{icon}</span>
          <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.625rem', fontWeight: 600, letterSpacing: '0.03em' }}>{label}</span>
        </NavLink>
      ))}
    </nav>
  )
}

