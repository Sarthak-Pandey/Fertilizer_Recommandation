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

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    let width = 0
    let height = 0
    let dpr = window.devicePixelRatio || 1

    let nodes: Node[] = []
    let edges: Edge[] = []

    const initNetwork = (w: number, h: number) => {
      nodes = []
      edges = []

      // Determine node density based on screen width
      const isMobile = w < 768
      const clusterMultiplier = isMobile ? 0.5 : 1.0

      // Main cluster centered in the visual container
      const centerX = w * 0.55
      const centerY = h * 0.5

      const clusterCenters = [
        { x: centerX, y: centerY, count: Math.round(26 * clusterMultiplier), spread: Math.min(w, h) * 0.22 },
        { x: centerX + w * 0.12, y: centerY - h * 0.22, count: Math.round(14 * clusterMultiplier), spread: Math.min(w, h) * 0.16 },
        { x: centerX - w * 0.12, y: centerY + h * 0.24, count: Math.round(16 * clusterMultiplier), spread: Math.min(w, h) * 0.18 },
        { x: w * 0.2, y: h * 0.35, count: Math.round(6 * clusterMultiplier), spread: Math.min(w, h) * 0.12 },
        { x: w * 0.8, y: h * 0.7, count: Math.round(5 * clusterMultiplier), spread: Math.min(w, h) * 0.1 },
      ]

      // 1. Central focal node
      nodes.push({
        x: centerX,
        y: centerY,
        baseX: centerX,
        baseY: centerY,
        radius: isMobile ? 8 : 10,
        vx: 0,
        vy: 0,
        isCentral: true,
        clusterId: 0,
      })

      // 2. Generate cluster nodes
      clusterCenters.forEach((cluster, cIdx) => {
        for (let i = 0; i < cluster.count; i++) {
          const angle = Math.random() * Math.PI * 2
          const distance = Math.pow(Math.random(), 0.85) * cluster.spread
          const nx = cluster.x + Math.cos(angle) * distance
          const ny = cluster.y + Math.sin(angle) * distance

          let r = 2.5
          const rand = Math.random()
          if (rand > 0.92) r = 9
          else if (rand > 0.78) r = 6.5
          else if (rand > 0.55) r = 4
          else r = 2.5

          if (isMobile) r *= 0.85

          nodes.push({
            x: nx,
            y: ny,
            baseX: nx,
            baseY: ny,
            radius: r,
            vx: (Math.random() - 0.5) * 0.2,
            vy: (Math.random() - 0.5) * 0.2,
            clusterId: cIdx,
          })
        }
      })

      // 3. Add peripheral nodes
      const peripheralCount = isMobile ? 4 : 8
      for (let i = 0; i < peripheralCount; i++) {
        const nx = w * (0.1 + Math.random() * 0.8)
        const ny = h * (0.1 + Math.random() * 0.8)
        nodes.push({
          x: nx,
          y: ny,
          baseX: nx,
          baseY: ny,
          radius: Math.random() > 0.6 ? 4.5 : 2.5,
          vx: (Math.random() - 0.5) * 0.15,
          vy: (Math.random() - 0.5) * 0.15,
          clusterId: -1,
        })
      }

      // 4. Generate edges based on proximity
      const maxDistance = Math.min(w, h) * 0.22
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x
          const dy = nodes[i].y - nodes[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)

          if (dist < maxDistance) {
            const prob = 1 - dist / maxDistance
            if (Math.random() < prob * 0.48) {
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
      time += 0.012

      // 1. Draw Edges
      ctx.lineWidth = 0.65
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

      // 2. Update & Draw Nodes
      nodes.forEach((node) => {
        if (!prefersReducedMotion) {
          node.x = node.baseX + Math.sin(time + node.baseY * 0.04) * 5
          node.y = node.baseY + Math.cos(time + node.baseX * 0.04) * 5

          if (mouseRef.current.active) {
            const mDx = node.x - mouseRef.current.x
            const mDy = node.y - mouseRef.current.y
            const mDist = Math.sqrt(mDx * mDx + mDy * mDy)
            const maxMouseDist = 130

            if (mDist < maxMouseDist && mDist > 0) {
              const force = (1 - mDist / maxMouseDist) * 14
              node.x += (mDx / mDist) * force
              node.y += (mDy / mDist) * force
            }
          }
        }

        // Node Body
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fillStyle = '#111111'
        ctx.fill()

        // Highlight central focal node with subtle orange ring & pulse
        if (node.isCentral) {
          const pulseRing = 6 + Math.sin(time * 2.5) * 2
          ctx.beginPath()
          ctx.arc(node.x, node.y, node.radius + pulseRing, 0, Math.PI * 2)
          ctx.strokeStyle = 'rgba(255, 107, 0, 0.5)'
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
