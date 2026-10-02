import React from 'react'

export interface LeaderConnection {
  id: string
  trackX: number
  trackY: number
  pillX: number
  pillY: number
  color: string
  opacity: number
  active?: boolean
}

interface LeaderSvgProps {
  connections: LeaderConnection[]
  width: number
  height: number
}

export const LeaderSvg: React.FC<LeaderSvgProps> = ({ connections, width, height }) => {
  return (
    <svg
      className="wv-leader-svg"
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        overflow: 'visible',
        zIndex: 5,
      }}
    >
      <defs>
        {connections.map((c) => (
          <linearGradient
            key={`grad-${c.id}`}
            id={`leader-grad-${c.id}`}
            x1="0%"
            y1="100%"
            x2="0%"
            y2="0%"
          >
            <stop offset="0%" stopColor={c.color} stopOpacity={0.8} />
            <stop offset="100%" stopColor={c.color} stopOpacity={c.active ? 1 : 0.6} />
          </linearGradient>
        ))}
      </defs>

      {connections.map((c) => {
        if (c.opacity <= 0.01) return null

        // Anchor at bottom or center of pill
        const x1 = c.trackX
        const y1 = c.trackY
        const x2 = c.pillX
        const y2 = c.pillY

        // Smooth cubic Bezier from track point up towards pill
        const dy = Math.abs(y2 - y1)
        const controlY1 = y1 - dy * 0.45
        const controlY2 = y2 + dy * 0.45
        const pathData = `M ${x1.toFixed(2)} ${y1.toFixed(2)} C ${x1.toFixed(2)} ${controlY1.toFixed(2)}, ${x2.toFixed(2)} ${controlY2.toFixed(2)}, ${x2.toFixed(2)} ${y2.toFixed(2)}`

        return (
          <g key={c.id} style={{ opacity: c.opacity, transition: 'opacity 0.2s ease' }}>
            {/* Soft glow shadow path */}
            {c.active && (
              <path
                d={pathData}
                fill="none"
                stroke={c.color}
                strokeWidth={3}
                strokeOpacity={0.25}
                strokeLinecap="round"
              />
            )}

            {/* Main connecting leader line */}
            <path
              d={pathData}
              fill="none"
              stroke={`url(#leader-grad-${c.id})`}
              strokeWidth={c.active ? 1.75 : 1.25}
              strokeDasharray={c.active ? 'none' : '3 3'}
              strokeLinecap="round"
            />

            {/* Timeline origin point marker (dot on the track) */}
            <circle
              cx={x1}
              cy={y1}
              r={c.active ? 4.5 : 3}
              fill={c.color}
              stroke="#FFFFFF"
              strokeWidth={1.5}
            />

            {/* Subtle destination anchor dot at pill */}
            <circle
              cx={x2}
              cy={y2}
              r={2}
              fill={c.color}
              opacity={0.85}
            />
          </g>
        )
      })}
    </svg>
  )
}
