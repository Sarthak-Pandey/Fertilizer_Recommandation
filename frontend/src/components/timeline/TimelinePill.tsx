import React from 'react'
import type { TimelineItemData } from './types'

interface TimelinePillProps {
  item: TimelineItemData
  left: number
  top: number
  scale?: number
  opacity?: number
  size?: number
  bg?: string
  text?: string
  border?: string
  dot?: string
  active?: boolean
  hovered?: boolean
  onClick?: () => void
  onMouseEnter?: () => void
  onMouseLeave?: () => void
}

export const TimelinePill: React.FC<TimelinePillProps> = ({
  item,
  left,
  top,
  scale = 1,
  opacity = 1,
  size = 1.0,
  bg = 'rgba(255, 255, 255, 0.94)',
  text = '#1a1714',
  border = 'rgba(17, 17, 17, 0.12)',
  dot = '#E5A700',
  active = false,
  hovered = false,
  onClick,
  onMouseEnter,
  onMouseLeave,
}) => {
  const currentScale = active ? Math.max(scale, 1.04) : hovered ? Math.max(scale, 1.02) : scale
  const transform = `translateX(-50%) translateY(-50%) scale(${currentScale.toFixed(3)})`

  return (
    <div
      className={`wv-pill ${active ? 'wv-pill-active' : ''} ${hovered ? 'wv-pill-hover' : ''}`}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      style={{
        ['--wv-pill-size' as any]: size,
        ['--wv-pill-bg' as any]: bg,
        ['--wv-pill-text' as any]: text,
        ['--wv-pill-border' as any]: active ? '#111111' : border,
        ['--wv-pill-dot' as any]: dot,
        left: `${left.toFixed(3)}px`,
        top: `${top.toFixed(3)}px`,
        transform,
        opacity,
        visibility: opacity > 0.01 ? 'visible' : 'hidden',
        position: 'absolute',
        zIndex: active ? 20 : hovered ? 15 : 10,
        pointerEvents: opacity > 0.05 ? 'auto' : 'none',
        willChange: 'transform, opacity, left, top',
      }}
    >
      <span className="wv-pill-dot-indicator" style={{ background: dot }} />
      <div className="wv-pill-content">
        <div className="wv-pill-header">
          <span className="wv-pill-title">{item.title}</span>
          {item.confidence !== undefined && (
            <span className="wv-pill-conf">{item.confidence}%</span>
          )}
        </div>
        <div className="wv-pill-meta">
          <span className="wv-pill-date">{item.dateLabel}</span>
          {item.status && (
            <span className="wv-pill-badge">{item.status}</span>
          )}
        </div>
      </div>
      {(item.latency || item.stage) && (
        <div className="wv-pill-chip">
          {item.stage || `${item.latency}ms`}
        </div>
      )}
    </div>
  )
}
