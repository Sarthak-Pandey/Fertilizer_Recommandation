import React, { useEffect, useRef, useState, useCallback } from 'react'
import { Link } from 'react-router-dom'
import type { TimelineItemData } from './types'
import { LabelOverlay } from './LabelOverlay'

interface TimelineViewportProps {
  items: TimelineItemData[]
  selectedItem: TimelineItemData | null
  onSelectItem: (item: TimelineItemData) => void
  onHoverItem?: (item: TimelineItemData | null) => void
  height?: number
  className?: string
  title?: string
  subtitle?: string
}

export const TimelineViewport: React.FC<TimelineViewportProps> = ({
  items,
  selectedItem,
  onSelectItem,
  onHoverItem,
  height = 360,
  className = '',
  title = 'Interactive Telemetry Timeline',
  subtitle = 'Drag, scrub, or use arrow keys to inspect agronomic inference logs across time.',
}) => {
  const containerRef = useRef<HTMLDivElement>(null)

  // Dimensions
  const [viewportWidth, setViewportWidth] = useState(1000)
  const [viewportHeight, setViewportHeight] = useState(height)

  // Interaction State
  const [isDragging, setIsDragging] = useState(false)
  const [hoveredId, setHoveredId] = useState<string | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)

  // Timeline coordinate math: panOffset is horizontal shift in pixels
  const [panOffset, setPanOffset] = useState<number>(0)
  const [zoomScale, setZoomScale] = useState<number>(1.0)

  // Drag tracking refs
  const isPointerDownRef = useRef(false)
  const pointerStartXRef = useRef(0)
  const pointerStartYRef = useRef(0)
  const hasHorizontalLockRef = useRef(false)
  const lastPointerXRef = useRef(0)
  const lastPointerTimeRef = useRef(0)
  const velocityRef = useRef(0)
  const panOffsetRef = useRef(0)
  const zoomScaleRef = useRef(1.0)
  const animInertiaRef = useRef<number | null>(null)
  const playheadAnimRef = useRef<number | null>(null)

  // Keep refs in sync
  useEffect(() => {
    panOffsetRef.current = panOffset
  }, [panOffset])

  useEffect(() => {
    zoomScaleRef.current = zoomScale
  }, [zoomScale])

  // Track Y position relative to container
  const timelineY = Math.max(160, viewportHeight - 80)

  // Calculate time bounds deterministically
  const minTime = items.length > 0 ? Math.min(...items.map((i) => i.timestamp)) : 1718300000000
  const maxTime = items.length > 0 ? Math.max(...items.map((i) => i.timestamp)) : 1718386400000
  const timeSpan = Math.max(maxTime - minTime, 3600000) // At least 1 hour

  // Bounds clamping for panOffset
  const clampPan = useCallback(
    (pan: number) => {
      const totalContentWidth = Math.max(viewportWidth * 1.5, 1200) * zoomScale
      const minPan = -(totalContentWidth - viewportWidth + 140)
      const maxPan = 140
      return Math.max(minPan, Math.min(maxPan, pan))
    },
    [viewportWidth, zoomScale]
  )

  // Convert timestamp to pixel coordinate on screen
  const timeToPixel = useCallback(
    (timestamp: number) => {
      if (timeSpan === 0) return viewportWidth / 2 + panOffset
      const normalized = (timestamp - minTime) / timeSpan
      const totalContentWidth = Math.max(viewportWidth * 1.5, 1200) * zoomScale
      const startX = 140
      return startX + normalized * (totalContentWidth - 280) + panOffset
    },
    [minTime, timeSpan, viewportWidth, panOffset, zoomScale]
  )

  // Convert screen pixel coordinate to timestamp
  const pixelToTime = useCallback(
    (pixelX: number) => {
      const totalContentWidth = Math.max(viewportWidth * 1.5, 1200) * zoomScale
      const startX = 140
      const contentX = pixelX - panOffset - startX
      const normalized = Math.max(0, Math.min(1, contentX / (totalContentWidth - 280)))
      return minTime + normalized * timeSpan
    },
    [minTime, timeSpan, viewportWidth, panOffset, zoomScale]
  )

  // Center the view on a specific item with critically damped spring
  const centerOnItem = useCallback(
    (item: TimelineItemData, animate = true) => {
      const centerScreen = viewportWidth / 2
      const targetPan = clampPan(centerScreen - (timeToPixel(item.timestamp) - panOffsetRef.current))

      if (animate) {
        const startPan = panOffsetRef.current
        const diff = targetPan - startPan
        let startT: number | null = null

        const animateSnap = (timestamp: number) => {
          if (!startT) startT = timestamp
          const elapsed = timestamp - startT
          const progress = Math.min(1, elapsed / 300)
          const ease = 1 - Math.pow(1 - progress, 3)

          const next = startPan + diff * ease
          setPanOffset(next)
          panOffsetRef.current = next

          if (progress < 1) {
            requestAnimationFrame(animateSnap)
          }
        }
        requestAnimationFrame(animateSnap)
      } else {
        setPanOffset(targetPan)
        panOffsetRef.current = targetPan
      }
    },
    [clampPan, timeToPixel, viewportWidth]
  )

  // Snap to nearest item if within 48px of playhead (§9.2)
  const snapToNearest = useCallback(() => {
    if (items.length === 0) return
    const centerScreen = viewportWidth / 2

    let closestItem: TimelineItemData | null = null
    let minDiff = Infinity

    items.forEach((item) => {
      const x = timeToPixel(item.timestamp)
      const diff = Math.abs(x - centerScreen)
      if (diff < minDiff) {
        minDiff = diff
        closestItem = item
      }
    })

    if (closestItem && minDiff < 48) {
      centerOnItem(closestItem, true)
    }
  }, [items, timeToPixel, viewportWidth, centerOnItem])

  // Observe container size with ResizeObserver
  useEffect(() => {
    const el = containerRef.current
    if (!el) return

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height: h } = entry.contentRect
        if (width > 0) setViewportWidth(width)
        if (h > 0) setViewportHeight(h)
      }
    })

    ro.observe(el)
    return () => ro.disconnect()
  }, [])

  // Inertia decay animation: velocity * 0.92 per frame (§9.2)
  const startInertia = useCallback(() => {
    if (Math.abs(velocityRef.current) < 0.05) {
      snapToNearest()
      return
    }

    const step = () => {
      velocityRef.current *= 0.92
      if (Math.abs(velocityRef.current) < 0.05) {
        snapToNearest()
        return
      }

      setPanOffset((prev) => {
        const next = clampPan(prev + velocityRef.current)
        panOffsetRef.current = next
        return next
      })

      animInertiaRef.current = requestAnimationFrame(step)
    }

    animInertiaRef.current = requestAnimationFrame(step)
  }, [clampPan, snapToNearest])

  // Center on selected item when selection changes externally
  useEffect(() => {
    if (selectedItem && !isDragging) {
      centerOnItem(selectedItem, true)
    }
  }, [selectedItem, isDragging, centerOnItem])

  // Pointer Drag Handlers with 8px horizontal threshold for touch-action (§9.2)
  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if (e.button !== 0) return

    if (animInertiaRef.current) cancelAnimationFrame(animInertiaRef.current)
    if (playheadAnimRef.current) cancelAnimationFrame(playheadAnimRef.current)
    setIsPlaying(false)

    isPointerDownRef.current = true
    pointerStartXRef.current = e.clientX
    pointerStartYRef.current = e.clientY
    lastPointerXRef.current = e.clientX
    lastPointerTimeRef.current = performance.now()
    velocityRef.current = 0
    hasHorizontalLockRef.current = false

    e.currentTarget.setPointerCapture(e.pointerId)
  }

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isPointerDownRef.current) return

    const dx = e.clientX - lastPointerXRef.current
    const totalDx = Math.abs(e.clientX - pointerStartXRef.current)
    const totalDy = Math.abs(e.clientY - pointerStartYRef.current)

    // 8px threshold before horizontal pan lock (§9.2)
    if (!hasHorizontalLockRef.current) {
      if (totalDx > 8 && totalDx > totalDy) {
        hasHorizontalLockRef.current = true
        setIsDragging(true)
      } else if (totalDy > 8) {
        // Vertical scroll permitted, release capture
        isPointerDownRef.current = false
        try {
          e.currentTarget.releasePointerCapture(e.pointerId)
        } catch {
          // Ignore
        }
        return
      }
    }

    if (!hasHorizontalLockRef.current) return

    const now = performance.now()
    const dt = Math.max(1, now - lastPointerTimeRef.current)

    velocityRef.current = (dx / dt) * 16 // Pixels per frame (~60fps)
    lastPointerXRef.current = e.clientX
    lastPointerTimeRef.current = now

    setPanOffset((prev) => {
      const next = clampPan(prev + dx)
      panOffsetRef.current = next
      return next
    })
  }

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isPointerDownRef.current) return
    isPointerDownRef.current = false
    setIsDragging(false)

    try {
      e.currentTarget.releasePointerCapture(e.pointerId)
    } catch {
      // Ignore
    }

    if (hasHorizontalLockRef.current) {
      startInertia()
    }
  }

  const handlePointerCancel = (e: React.PointerEvent<HTMLDivElement>) => {
    isPointerDownRef.current = false
    setIsDragging(false)
    try {
      e.currentTarget.releasePointerCapture(e.pointerId)
    } catch {
      // Ignore
    }
  }

  // Wheel zoom around pointer + horizontal panning (§9.2)
  const handleWheel = (e: React.WheelEvent<HTMLDivElement>) => {
    if (e.shiftKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
      // Horizontal pan
      e.preventDefault()
      const delta = e.deltaX !== 0 ? e.deltaX : e.deltaY
      setPanOffset((prev) => {
        const next = clampPan(prev - delta)
        panOffsetRef.current = next
        return next
      })
    } else {
      // Vertical wheel = Zoom around pointer
      e.preventDefault()
      const rect = containerRef.current?.getBoundingClientRect()
      const mouseX = rect ? e.clientX - rect.left : viewportWidth / 2

      const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89
      const newZoom = Math.max(0.5, Math.min(3.0, zoomScale * zoomFactor))

      // Keep pointer fixed in time
      const timeAtPointer = pixelToTime(mouseX)
      setZoomScale(newZoom)
      zoomScaleRef.current = newZoom

      // Re-center around timeAtPointer
      const newPixelAtTime = timeToPixel(timeAtPointer)
      const offsetDiff = newPixelAtTime - mouseX
      setPanOffset((prev) => clampPan(prev - offsetDiff))
    }
  }

  // Keyboard navigation & accessibility (§9.2, §12)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (items.length === 0) return

    const currentIndex = selectedItem
      ? items.findIndex((i) => i.id === selectedItem.id)
      : -1

    if (e.key === 'ArrowRight') {
      e.preventDefault()
      if (e.shiftKey) {
        // Shift+Right: Jump 1 day or 5 items
        const nextIdx = Math.min(items.length - 1, (currentIndex === -1 ? 0 : currentIndex) + 5)
        onSelectItem(items[nextIdx])
      } else {
        const nextIdx = Math.min(items.length - 1, currentIndex + 1)
        onSelectItem(items[nextIdx])
      }
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault()
      if (e.shiftKey) {
        // Shift+Left: Jump back
        const prevIdx = Math.max(0, (currentIndex === -1 ? items.length - 1 : currentIndex) - 5)
        onSelectItem(items[prevIdx])
      } else {
        const prevIdx = Math.max(0, currentIndex - 1)
        onSelectItem(items[prevIdx])
      }
    } else if (e.key === '+' || e.key === '=') {
      e.preventDefault()
      setZoomScale((z) => Math.min(3.0, z * 1.2))
    } else if (e.key === '-' || e.key === '_') {
      e.preventDefault()
      setZoomScale((z) => Math.max(0.5, z * 0.8))
    } else if (e.key === ' ' || e.key === 'Spacebar') {
      e.preventDefault()
      togglePlayback()
    }
  }

  // Auto-play / Simulate scrub playback
  const togglePlayback = () => {
    if (isPlaying) {
      setIsPlaying(false)
      if (playheadAnimRef.current) cancelAnimationFrame(playheadAnimRef.current)
    } else {
      setIsPlaying(true)
      let lastT = performance.now()

      const playStep = (timestamp: number) => {
        const dt = (timestamp - lastT) / 1000
        lastT = timestamp

        setPanOffset((prev) => {
          const next = prev - 45 * dt
          const totalContentWidth = Math.max(viewportWidth * 1.5, 1200) * zoomScaleRef.current
          const minPan = -(totalContentWidth - viewportWidth + 140)

          if (next <= minPan) {
            panOffsetRef.current = 140
            return 140
          }
          panOffsetRef.current = next
          return next
        })

        playheadAnimRef.current = requestAnimationFrame(playStep)
      }

      playheadAnimRef.current = requestAnimationFrame(playStep)
    }
  }

  // Generate dynamic ruler time ticks
  const ticksCount = 18
  const rulerTicks = Array.from({ length: ticksCount }).map((_, idx) => {
    const fraction = idx / (ticksCount - 1)
    const tickTime = minTime + fraction * timeSpan
    const pixelX = timeToPixel(tickTime)
    const date = new Date(tickTime)
    const label = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit' })
    const isMajor = idx % 3 === 0
    return { id: `tick-${idx}`, pixelX, label, isMajor }
  })

  // Center needle position
  const centerScreenX = viewportWidth / 2
  const activeScrubTime = pixelToTime(centerScreenX)
  const activeScrubDateStr = new Date(activeScrubTime).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  const ariaValueText = selectedItem
    ? `${selectedItem.id}, ${selectedItem.title}, ${selectedItem.dateLabel}, ${selectedItem.confidence || 98}% confidence`
    : `Scrubber at ${activeScrubDateStr}`

  // Empty state handling (§9.2)
  if (items.length === 0) {
    return (
      <div
        className={`wv-timeline-wrapper ${className}`}
        style={{
          height: `${viewportHeight}px`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 'var(--space-4)',
          background: 'var(--surface-low)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-frame)',
        }}
      >
        <p style={{ color: 'var(--ink-2)', fontSize: '0.9375rem' }}>
          No recommendations yet. Run your first one from Overview.
        </p>
        <Link to="/overview" className="btn btn-secondary">
          Go to Overview
        </Link>
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      className={`wv-timeline-wrapper ${className}`}
      role="slider"
      tabIndex={0}
      aria-label="Agronomic Telemetry Waveform Timeline"
      aria-valuemin={minTime}
      aria-valuemax={maxTime}
      aria-valuenow={selectedItem?.timestamp || activeScrubTime}
      aria-valuetext={ariaValueText}
      onKeyDown={handleKeyDown}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onPointerCancel={handlePointerCancel}
      onWheel={handleWheel}
      style={{
        position: 'relative',
        width: '100%',
        height: `${viewportHeight}px`,
        cursor: isDragging ? 'grabbing' : 'grab',
        touchAction: 'pan-y',
      }}
    >
      {/* Top Controls Header */}
      <div
        style={{
          position: 'absolute',
          top: '1rem',
          left: '1.25rem',
          right: '1.25rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          zIndex: 25,
          pointerEvents: 'auto',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '2px' }}>
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '50%',
                background: 'var(--status-success)',
              }}
            />
            <h3
              style={{
                fontFamily: 'var(--font-body)',
                fontSize: '0.9375rem',
                fontWeight: 600,
                color: 'var(--ink)',
                letterSpacing: '-0.01em',
              }}
            >
              {title}
            </h3>
            <span
              className="status-badge badge-deployed"
              style={{ fontSize: '0.6875rem' }}
            >
              {items.length} KEYFRAMES
            </span>
          </div>
          <p
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.6875rem',
              color: 'var(--ink-3)',
              maxWidth: '480px',
            }}
          >
            {subtitle}
          </p>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {/* Active Time Indicator Badge */}
          <div
            style={{
              padding: '0.25rem 0.75rem',
              borderRadius: 'var(--radius-pill)',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.6875rem',
              fontWeight: 500,
              color: 'var(--ink)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.375rem',
            }}
          >
            <span className="material-symbols-outlined" style={{ fontSize: '14px', color: 'var(--ink-3)' }}>
              schedule
            </span>
            <span>{activeScrubDateStr}</span>
          </div>

          {/* Zoom controls */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              background: 'var(--surface)',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid var(--border)',
              padding: '2px',
            }}
          >
            <button
              onClick={() => setZoomScale((z) => Math.max(0.5, z * 0.85))}
              style={{
                width: '26px',
                height: '26px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                borderRadius: '50%',
                color: 'var(--ink)',
              }}
              title="Zoom out (-)"
            >
              <span className="material-symbols-outlined" style={{ fontSize: '14px' }}>remove</span>
            </button>
            <span
              style={{
                fontSize: '0.6875rem',
                fontFamily: 'var(--font-mono)',
                fontWeight: 600,
                padding: '0 4px',
                minWidth: '38px',
                textAlign: 'center',
                color: 'var(--ink-2)',
              }}
            >
              {Math.round(zoomScale * 100)}%
            </span>
            <button
              onClick={() => setZoomScale((z) => Math.min(3.0, z * 1.15))}
              style={{
                width: '26px',
                height: '26px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                borderRadius: '50%',
                color: 'var(--ink)',
              }}
              title="Zoom in (+)"
            >
              <span className="material-symbols-outlined" style={{ fontSize: '14px' }}>add</span>
            </button>
          </div>

          {/* Play/Pause Button */}
          <button
            onClick={togglePlayback}
            style={{
              height: '30px',
              padding: '0 0.75rem',
              borderRadius: 'var(--radius-pill)',
              background: isPlaying ? 'var(--status-live)' : 'var(--ink)',
              color: isPlaying ? 'var(--ink)' : 'var(--surface)',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '0.6875rem',
              fontWeight: 600,
              fontFamily: 'var(--font-body)',
              transition: 'background var(--dur-micro) var(--ease-settle)',
            }}
          >
            <span className="material-symbols-outlined" style={{ fontSize: '14px' }}>
              {isPlaying ? 'pause' : 'play_arrow'}
            </span>
            <span>{isPlaying ? 'Pause' : 'Scrub'}</span>
          </button>
        </div>
      </div>

      {/* SVG Canvas for Track Line & Ruler Ticks */}
      <svg
        width={viewportWidth}
        height={viewportHeight}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          pointerEvents: 'none',
          zIndex: 3,
        }}
      >
        {/* Main Baseline Track */}
        <line
          x1={0}
          y1={timelineY}
          x2={viewportWidth}
          y2={timelineY}
          stroke="var(--border)"
          strokeWidth={2}
        />

        {/* Ruler Ticks */}
        {rulerTicks.map((tick) => {
          if (tick.pixelX < -50 || tick.pixelX > viewportWidth + 50) return null
          const tickHeight = tick.isMajor ? 14 : 7
          const y1 = timelineY - tickHeight / 2
          const y2 = timelineY + tickHeight / 2

          return (
            <g key={tick.id}>
              <line
                x1={tick.pixelX}
                y1={y1}
                x2={tick.pixelX}
                y2={y2}
                stroke={tick.isMajor ? 'var(--border-strong)' : 'var(--border)'}
                strokeWidth={tick.isMajor ? 1.5 : 1}
              />
              {tick.isMajor && (
                <text
                  x={tick.pixelX}
                  y={timelineY + 22}
                  textAnchor="middle"
                  fill="var(--ink-3)"
                  fontSize="9px"
                  fontFamily="var(--font-mono)"
                  letterSpacing="0.04em"
                >
                  {tick.label}
                </text>
              )}
            </g>
          )
        })}
      </svg>

      {/* Dynamic Label Overlay (Synchronized Pills + SVG Leader Lines) */}
      <LabelOverlay
        items={items}
        timeToPixel={timeToPixel}
        timelineY={timelineY}
        viewportWidth={viewportWidth}
        viewportHeight={viewportHeight}
        selectedId={selectedItem?.id || null}
        hoveredId={hoveredId}
        zoomScale={zoomScale}
        onSelectItem={onSelectItem}
        onHoverItem={(id) => {
          setHoveredId(id)
          if (onHoverItem) {
            const it = id ? items.find((i) => i.id === id) || null : null
            onHoverItem(it)
          }
        }}
        isDragging={isDragging}
      />

      {/* Playhead Center Scrubber Needle (§9.2: 1px --status-live needle + 6px cap + mono badge) */}
      <div
        className="wv-playhead-line"
        style={{
          left: `${centerScreenX}px`,
        }}
      >
        <div className="wv-playhead-cap" />
        <div className="wv-playhead-badge">
          {activeScrubDateStr}
        </div>
      </div>
    </div>
  )
}
