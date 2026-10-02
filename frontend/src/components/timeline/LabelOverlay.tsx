import React, { useEffect, useRef, useState } from 'react'
import type { TimelineItemData } from './types'
import { LeaderSvg } from './LeaderSvg'
import type { LeaderConnection } from './LeaderSvg'
import { TimelinePill } from './TimelinePill'

interface LabelOverlayProps {
  items: TimelineItemData[]
  timeToPixel: (timestamp: number) => number
  timelineY: number
  viewportWidth: number
  viewportHeight: number
  selectedId: string | null
  hoveredId: string | null
  zoomScale: number
  onSelectItem: (item: TimelineItemData) => void
  onHoverItem: (id: string | null) => void
  isDragging: boolean
}

interface InterpolatedItem {
  id: string
  item: TimelineItemData
  curX: number
  curY: number
  targetX: number
  targetY: number
  curScale: number
  targetScale: number
  curOpacity: number
  targetOpacity: number
  size: number
  level: number
  trackX: number
  trackY: number
}

export const LabelOverlay: React.FC<LabelOverlayProps> = ({
  items,
  timeToPixel,
  timelineY,
  viewportWidth,
  viewportHeight,
  selectedId,
  hoveredId,
  zoomScale: _zoomScale,
  onSelectItem,
  onHoverItem,
  isDragging,
}) => {
  const [renderItems, setRenderItems] = useState<InterpolatedItem[]>([])
  const [connections, setConnections] = useState<LeaderConnection[]>([])
  const itemsStateRef = useRef<{ [id: string]: InterpolatedItem }>({})
  const animFrameRef = useRef<number | null>(null)
  const lastTimeRef = useRef<number>(0)

  // 1. Target calculation & Collision Avoidance
  useEffect(() => {
    // Sort items horizontally
    const positioned = items
      .map((item) => ({
        item,
        trackX: timeToPixel(item.timestamp),
        trackY: timelineY,
      }))
      .sort((a, b) => a.trackX - b.trackX)

    // Greedy multi-level stacking (3 levels) to avoid overlap
    const minDistance = 150
    const lastXForLevel: number[] = [-9999, -9999, -9999]
    const levelAssignments: { [id: string]: number } = {}

    positioned.forEach(({ item, trackX }) => {
      let chosenLevel = 0
      for (let lvl = 0; lvl < 3; lvl++) {
        if (trackX - lastXForLevel[lvl] >= minDistance) {
          chosenLevel = lvl
          break
        }
      }
      levelAssignments[item.id] = chosenLevel
      lastXForLevel[chosenLevel] = trackX
    })

    const updatedState = { ...itemsStateRef.current }

    positioned.forEach(({ item, trackX, trackY }) => {
      const level = levelAssignments[item.id] ?? 0
      const targetY = trackY - (60 + 44 * level)
      const targetX = trackX

      const inView = trackX >= -120 && trackX <= viewportWidth + 120
      const isSelected = selectedId === item.id
      const isHovered = hoveredId === item.id
      const activeState = isSelected || isHovered

      const targetOpacity = inView ? (activeState ? 1 : 0.92) : 0
      const targetScale = inView ? (isSelected ? 1.05 : isHovered ? 1.02 : 1.0) : 0.5

      const existing = updatedState[item.id]

      if (existing) {
        existing.item = item
        existing.targetX = targetX
        existing.targetY = targetY
        existing.trackX = trackX
        existing.trackY = trackY
        existing.targetOpacity = targetOpacity
        existing.targetScale = targetScale
        existing.level = level
      } else {
        updatedState[item.id] = {
          id: item.id,
          item,
          curX: targetX,
          curY: targetY + 15,
          targetX,
          targetY,
          curScale: 0.5,
          targetScale,
          curOpacity: 0,
          targetOpacity,
          size: item.size || 0.9,
          level,
          trackX,
          trackY,
        }
      }
    })

    itemsStateRef.current = updatedState
  }, [items, timeToPixel, timelineY, viewportWidth, selectedId, hoveredId])

  // 2. High-performance spring lerp physics loop
  useEffect(() => {
    let active = true

    const tick = (now: number) => {
      if (!active) return

      if (lastTimeRef.current === 0) lastTimeRef.current = now
      const dt = Math.min(now - lastTimeRef.current, 64)
      lastTimeRef.current = now

      const baseLerp = isDragging ? 0.32 : 0.16
      const lerpFactor = 1 - Math.pow(1 - baseLerp, dt / 16.67)

      const currentMap = itemsStateRef.current
      const nextRenderList: InterpolatedItem[] = []
      const nextConnections: LeaderConnection[] = []

      for (const id in currentMap) {
        const entry = currentMap[id]

        const dx = entry.targetX - entry.curX
        const dy = entry.targetY - entry.curY
        const dScale = entry.targetScale - entry.curScale
        const dOpacity = entry.targetOpacity - entry.curOpacity

        if (
          Math.abs(dx) > 0.05 ||
          Math.abs(dy) > 0.05 ||
          Math.abs(dScale) > 0.005 ||
          Math.abs(dOpacity) > 0.005
        ) {
          entry.curX += dx * lerpFactor
          entry.curY += dy * lerpFactor
          entry.curScale += dScale * lerpFactor
          entry.curOpacity += dOpacity * lerpFactor
        } else {
          entry.curX = entry.targetX
          entry.curY = entry.targetY
          entry.curScale = entry.targetScale
          entry.curOpacity = entry.targetOpacity
        }

        if (entry.curOpacity > 0.01) {
          nextRenderList.push({ ...entry })

          const isSelected = selectedId === entry.id
          const isHovered = hoveredId === entry.id
          const dotColor = entry.item.dotColor || '#E5A700'

          nextConnections.push({
            id: entry.id,
            trackX: entry.trackX,
            trackY: entry.trackY,
            pillX: entry.curX,
            pillY: entry.curY + 16,
            color: dotColor,
            opacity: entry.curOpacity,
            active: isSelected || isHovered,
          })
        }
      }

      setRenderItems(nextRenderList)
      setConnections(nextConnections)

      animFrameRef.current = requestAnimationFrame(tick)
    }

    animFrameRef.current = requestAnimationFrame(tick)

    return () => {
      active = false
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current)
    }
  }, [isDragging, selectedId, hoveredId])

  return (
    <div className="wv-label-overlay">
      <LeaderSvg
        connections={connections}
        width={viewportWidth}
        height={viewportHeight}
      />

      {renderItems.map((entry) => {
        const isSelected = selectedId === entry.id
        const isHovered = hoveredId === entry.id
        const item = entry.item

        return (
          <TimelinePill
            key={entry.id}
            item={item}
            left={entry.curX}
            top={entry.curY}
            scale={entry.curScale}
            opacity={entry.curOpacity}
            size={entry.size}
            bg={item.pillBg || 'rgba(255, 255, 255, 0.94)'}
            text={item.pillText || '#1a1714'}
            border={item.pillBorder || 'rgba(17, 17, 17, 0.12)'}
            dot={item.dotColor || '#E5A700'}
            active={isSelected}
            hovered={isHovered}
            onClick={() => onSelectItem(item)}
            onMouseEnter={() => onHoverItem(item.id)}
            onMouseLeave={() => onHoverItem(null)}
          />
        )
      })}
    </div>
  )
}
