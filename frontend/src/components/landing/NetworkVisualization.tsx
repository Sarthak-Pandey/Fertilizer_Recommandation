import { useEffect, useRef } from 'react'

interface Node {
  x: number
  y: number
  baseX: number
  baseY: number
  radius: number
  vx: number
  vy: number
  isCentral?: boolean
  clusterId?: number
}

interface Edge {
  source: number
  target: number
}

export default function NetworkVisualization() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const animFrameRef = useRef<number | null>(null)
  const mouseRef = useRef<{ x: number; y: number; active: boolean }>({ x: -1000, y: -1000, active: false })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Reduced motion check
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    let width = 0
    let height = 0
    let dpr = window.devicePixelRatio || 1

    let nodes: Node[] = []
    let edges: Edge[] = []

    const initNetwork = (w: number, h: number) => {
      nodes = []
      edges = []

      // Generate cluster centers
      // Reference visual: main cluster vertically stretched on right side (center-right)
      const centerX = w * 0.65
      const centerY = h * 0.48

      const clusterCenters = [
        { x: centerX, y: centerY, count: 28, spread: Math.min(w, h) * 0.22 },
        { x: centerX + w * 0.1, y: centerY - h * 0.22, count: 14, spread: Math.min(w, h) * 0.16 },
        { x: centerX - w * 0.08, y: centerY + h * 0.26, count: 16, spread: Math.min(w, h) * 0.18 },
        { x: w * 0.25, y: h * 0.35, count: 5, spread: Math.min(w, h) * 0.1 },
        { x: w * 0.85, y: h * 0.75, count: 4, spread: Math.min(w, h) * 0.08 },
      ]

      let nodeIndex = 0

      // Central important node
      nodes.push({
        x: centerX,
        y: centerY,
        baseX: centerX,
        baseY: centerY,
        radius: 12,
        vx: (Math.random() - 0.5) * 0.15,
        vy: (Math.random() - 0.5) * 0.15,
        isCentral: true,
        clusterId: 0,
      })
      nodeIndex++

      // Create nodes around clusters
      clusterCenters.forEach((cluster, cIdx) => {
        for (let i = 0; i < cluster.count; i++) {
          const angle = Math.random() * Math.PI * 2
          const distance = Math.pow(Math.random(), 0.8) * cluster.spread
          const nx = cluster.x + Math.cos(angle) * distance
          const ny = cluster.y + Math.sin(angle) * distance

          // Radii distribution matching reference image: ranging from 2px to 11px
          let r = 2.5
          const rand = Math.random()
          if (rand > 0.92) r = 11
          else if (rand > 0.78) r = 7
          else if (rand > 0.55) r = 4.5
          else r = 2.5

          nodes.push({
            x: nx,
            y: ny,
            baseX: nx,
            baseY: ny,
            radius: r,
            vx: (Math.random() - 0.5) * 0.25,
            vy: (Math.random() - 0.5) * 0.25,
            clusterId: cIdx,
          })
          nodeIndex++
        }
      })

      // Add a few scattered isolated peripheral nodes
      for (let i = 0; i < 8; i++) {
        const nx = w * (0.15 + Math.random() * 0.75)
        const ny = h * (0.1 + Math.random() * 0.8)
        nodes.push({
          x: nx,
          y: ny,
          baseX: nx,
          baseY: ny,
          radius: Math.random() > 0.6 ? 5 : 3,
          vx: (Math.random() - 0.5) * 0.2,
          vy: (Math.random() - 0.5) * 0.2,
          clusterId: -1,
        })
      }

      // Generate connection edges based on distance and cluster proximity
      const maxDistance = Math.min(w, h) * 0.2
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x
          const dy = nodes[i].y - nodes[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)

          // Connect if close enough and random chance depending on distance
          if (dist < maxDistance) {
            const prob = 1 - dist / maxDistance
            if (Math.random() < prob * 0.45) {
              edges.push({ source: i, target: j })
            }
          }
        }
      }
    }

    const resize = () => {
      const parent = canvas.parentElement
      if (!parent) return
      width = parent.clientWidth
      height = parent.clientHeight
      dpr = window.devicePixelRatio || 1

      canvas.width = width * dpr
      canvas.height = height * dpr
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`

      ctx.scale(dpr, dpr)
      initNetwork(width, height)
    }

    resize()
    window.addEventListener('resize', resize)

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      mouseRef.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
        active: true,
      }
    }

    const handleMouseLeave = () => {
      mouseRef.current.active = false
    }

    canvas.addEventListener('mousemove', handleMouseMove)
    canvas.addEventListener('mouseleave', handleMouseLeave)

    // Animation Loop
    let time = 0
    const render = () => {
      ctx.clearRect(0, 0, width, height)
      time += 0.015

      // 1. Draw Edges (Thin gray lines)
      ctx.lineWidth = 0.6
      ctx.strokeStyle = 'rgba(17, 17, 17, 0.12)'

      edges.forEach((edge) => {
        const n1 = nodes[edge.source]
        const n2 = nodes[edge.target]
        if (!n1 || !n2) return

        ctx.beginPath()
        ctx.moveTo(n1.x, n1.y)
        ctx.lineTo(n2.x, n2.y)
        ctx.stroke()
      })

      // 2. Update and Draw Nodes
      nodes.forEach((node) => {
        if (!prefersReducedMotion) {
          // Floating drift oscillation
          node.x = node.baseX + Math.sin(time + node.baseY * 0.05) * 6
          node.y = node.baseY + Math.cos(time + node.baseX * 0.05) * 6

          // Mouse interaction (Magnetic push / pull effect)
          if (mouseRef.current.active) {
            const mDx = node.x - mouseRef.current.x
            const mDy = node.y - mouseRef.current.y
            const mDist = Math.sqrt(mDx * mDx + mDy * mDy)
            const maxMouseDist = 140

            if (mDist < maxMouseDist && mDist > 0) {
              const force = (1 - mDist / maxMouseDist) * 18
              node.x += (mDx / mDist) * force
              node.y += (mDy / mDist) * force
            }
          }
        }

        // Draw node body
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fillStyle = '#111111'
        ctx.fill()

        // Highlight central node with subtle orange accent ring
        if (node.isCentral) {
          ctx.beginPath()
          ctx.arc(node.x, node.y, node.radius + 6, 0, Math.PI * 2)
          ctx.strokeStyle = 'rgba(255, 107, 0, 0.45)'
          ctx.lineWidth = 1.5
          ctx.stroke()
        }
      })

      animFrameRef.current = requestAnimationFrame(render)
    }

    render()

    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current)
      window.removeEventListener('resize', resize)
      canvas.removeEventListener('mousemove', handleMouseMove)
      canvas.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [])

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
          cursor: 'crosshair',
        }}
      />
    </div>
  )
}
