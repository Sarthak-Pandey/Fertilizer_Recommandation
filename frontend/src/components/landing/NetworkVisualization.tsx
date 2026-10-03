import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'

interface NodeItem {
  id: number
  color: string
  radius: number
  basePos: THREE.Vector3
  currentPos: THREE.Vector3
  phase: number
  freq: number
  isLandmark?: boolean
  label?: string
}

// Telemetry pill content matching reference screenshot
const DEFAULT_TELEMETRY = 'HEALTH CHECK TOO LAX · 30S · PEERS 5S'

export default function NetworkVisualization() {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const pillRef = useRef<HTMLDivElement | null>(null)
  const leaderPathRef = useRef<SVGPathElement | null>(null)
  const leaderOriginDotRef = useRef<SVGCircleElement | null>(null)
  const leaderTargetDotRef = useRef<SVGCircleElement | null>(null)
  const pillTextRef = useRef<HTMLSpanElement | null>(null)
  const pillDotRef = useRef<HTMLSpanElement | null>(null)

  const [activeTelemetry, setActiveTelemetry] = useState(DEFAULT_TELEMETRY)
  const [activeDotColor, setActiveDotColor] = useState('#E5A700')

  useEffect(() => {
    const container = containerRef.current
    const canvas = canvasRef.current
    if (!container || !canvas) return

    // 1. Scene & Camera Setup
    const scene = new THREE.Scene()
    scene.background = null // Transparent canvas so background matches editorial theme

    let width = container.clientWidth || 540
    let height = container.clientHeight || 500

    const camera = new THREE.PerspectiveCamera(43, width / height, 0.1, 1500)
    let cameraZ = 425
    camera.position.set(0, 0, cameraZ)

    const renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    })
    renderer.setSize(width, height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))

    // 2. Soft 3D Lighting for realistic velvety shading on spheres
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.96)
    scene.add(ambientLight)

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.72)
    dirLight.position.set(140, 200, 220)
    scene.add(dirLight)

    // 3. Exact Solid Color Palette Sampled Directly from Reference Image
    const C_BLACK = '#0D0D0D'
    const C_ORANGE = '#FF723B'
    const C_YELLOW = '#EAA800'
    const C_OLIVE = '#A19822'

    const rootGroup = new THREE.Group()
    rootGroup.scale.set(0.88, 0.88, 0.88)
    rootGroup.position.set(-14, -4, 0)
    scene.add(rootGroup)

    // Using MeshBasicMaterial for 100% solid, pure, unshaded matte colors matching the reference image
    const materialCache = new Map<string, THREE.MeshBasicMaterial>()
    const getMaterial = (colorHex: string) => {
      if (!materialCache.has(colorHex)) {
        materialCache.set(
          colorHex,
          new THREE.MeshBasicMaterial({
            color: new THREE.Color(colorHex),
          })
        )
      }
      return materialCache.get(colorHex)!
    }

    const sharedSphereGeo = new THREE.SphereGeometry(1, 20, 16)

    // 4. Construct Precise Structure Matching Reference Image
    const nodes: NodeItem[] = []
    const meshes: THREE.Mesh[] = []

    // Helper to add a node
    const addNode = (
      id: number,
      pos: THREE.Vector3,
      radius: number,
      color: string,
      isLandmark = false,
      label?: string
    ) => {
      const node: NodeItem = {
        id,
        color,
        radius,
        basePos: pos.clone(),
        currentPos: pos.clone(),
        phase: (id * 1.37) % (Math.PI * 2),
        freq: 0.8 + ((id * 31) % 50) / 100,
        isLandmark,
        label,
      }
      nodes.push(node)

      const mesh = new THREE.Mesh(sharedSphereGeo, getMaterial(color))
      mesh.scale.set(radius, radius, radius)
      mesh.position.copy(pos)
      mesh.userData = { id, color, label }
      rootGroup.add(mesh)
      meshes.push(mesh)
    }

    // A. Central Hub Node (Center of radial burst)
    addNode(0, new THREE.Vector3(0, 0, 0), 3.0, C_BLACK, true)

    // B. Landmark Nodes Handcrafted to Match Image 1 Exactly
    // 1: Top-Left ~10:00 - VERY LARGE BLACK SPHERE
    addNode(1, new THREE.Vector3(-86, 94, 18), 13.5, C_BLACK, true)
    // 2: Inner Top-Left ~10:15 - LARGE BLACK SPHERE
    addNode(2, new THREE.Vector3(-34, 34, 36), 10.0, C_BLACK, true)
    // 3: Top-Left ~11:00 - LARGE ORANGE SPHERE
    addNode(3, new THREE.Vector3(-24, 96, -14), 10.8, C_ORANGE, true)
    // 4: Bottom Center ~6:00 - VERY LARGE YELLOW SPHERE (Image 1 bottom)
    addNode(4, new THREE.Vector3(-14, -120, 14), 12.0, C_YELLOW, true)
    // 5: Center-Right ~3:00 - LARGE BLACK SPHERE
    addNode(5, new THREE.Vector3(124, 16, -18), 9.6, C_BLACK, true)
    // 6: Outer-Right ~3:30 - LARGE ORANGE SPHERE
    addNode(6, new THREE.Vector3(146, -6, 28), 9.6, C_ORANGE, true)
    // 7: Upper-Right ~1:30 - GOLD NODE WITH LEADER LINE (Image 1 top right)
    addNode(7, new THREE.Vector3(82, 102, 22), 7.8, C_YELLOW, true, DEFAULT_TELEMETRY)
    // 8: Bottom-Right ~5:00 - LARGE ORANGE SPHERE
    addNode(8, new THREE.Vector3(42, -84, 25), 9.2, C_ORANGE, true)
    // 9: Bottom-Left ~7:30 - LARGE OLIVE SPHERE
    addNode(9, new THREE.Vector3(-96, -70, -12), 9.0, C_OLIVE, true)
    // 10: Center-Left ~9:00 - LARGE OLIVE SPHERE (Image 1 left edge)
    addNode(10, new THREE.Vector3(-114, 28, -10), 9.0, C_OLIVE, true)
    // 11: Upper-Right ~2:00 - MEDIUM BLACK
    addNode(11, new THREE.Vector3(98, 64, -15), 7.0, C_BLACK, true)
    // 12: Upper Center ~12:00 - MEDIUM BLACK
    addNode(12, new THREE.Vector3(18, 116, -8), 6.6, C_BLACK, true)
    // 13: Inner Bottom-Right ~4:00 - MEDIUM ORANGE
    addNode(13, new THREE.Vector3(36, -42, 38), 7.0, C_ORANGE, true)
    // 14: Inner Bottom ~6:30 - MEDIUM YELLOW
    addNode(14, new THREE.Vector3(-8, -62, 20), 6.2, C_YELLOW, true)
    // 15: Inner Top ~12:30 - MEDIUM ORANGE
    addNode(15, new THREE.Vector3(24, 54, 24), 6.2, C_ORANGE, true)
    // 16: Bottom ~5:45 - MEDIUM YELLOW
    addNode(16, new THREE.Vector3(12, -106, -5), 5.8, C_YELLOW, true)
    // 17: Center-Left ~8:30 - MEDIUM OLIVE
    addNode(17, new THREE.Vector3(-78, -38, 15), 6.2, C_OLIVE, true)
    // 18: Upper-Left ~10:30 - MEDIUM ORANGE
    addNode(18, new THREE.Vector3(-66, 122, -6), 5.5, C_ORANGE, true)
    // 19: Right ~2:45 - MEDIUM YELLOW
    addNode(19, new THREE.Vector3(88, 32, 22), 5.8, C_YELLOW, true)
    // 20: Bottom-Left ~8:00 - MEDIUM BLACK
    addNode(20, new THREE.Vector3(-72, -88, 10), 6.2, C_BLACK, true)

    // C. Procedural Spherical Fibonacci Burst (Remaining ~68 nodes)
    // Uniform, organic radial distribution to complete the exact dandelion density
    const FIB_COUNT = 68
    let pseudoRand = 12345
    const getRand = () => {
      pseudoRand = (pseudoRand * 16807) % 2147483647
      return (pseudoRand - 1) / 2147483646
    }

    for (let k = 0; k < FIB_COUNT; k++) {
      const phi = Math.acos(1 - (2 * (k + 0.5)) / FIB_COUNT)
      const theta = Math.PI * (1 + Math.sqrt(5)) * k // Golden angle

      const dirX = Math.sin(phi) * Math.cos(theta)
      const dirY = Math.sin(phi) * Math.sin(theta)
      const dirZ = Math.cos(phi) * 0.75 // Flattened z-depth for optimal front-facing perspective

      // Varying radial distances from center
      const rDist = 28 + Math.pow(getRand(), 0.72) * 128
      const pos = new THREE.Vector3(dirX * rDist, dirY * rDist, dirZ * rDist)

      // Color distribution matching reference: 62% Black, 15% Orange, 13% Yellow, 10% Olive
      const cRoll = getRand()
      const color =
        cRoll > 0.86
          ? C_ORANGE
          : cRoll > 0.73
          ? C_YELLOW
          : cRoll > 0.62
          ? C_OLIVE
          : C_BLACK

      // Size distribution: 25% medium, 50% small, 25% tiny pinprick specks
      const sRoll = getRand()
      let radius = 1.8
      if (sRoll > 0.78) {
        radius = 3.6 + getRand() * 2.0 // medium
      } else if (sRoll > 0.32) {
        radius = 1.9 + getRand() * 1.3 // small
      } else {
        radius = 0.9 + getRand() * 0.6 // tiny pinpoint speck
      }

      addNode(nodes.length, pos, radius, color)
    }

    // 5. Radial Stems (Signature Dandelion Aesthetic)
    // In Image 1, all lines originate from the center hub and radiate outward
    const totalLines = nodes.length - 1
    const linePositions = new Float32Array(totalLines * 2 * 3)
    const lineGeometry = new THREE.BufferGeometry()
    lineGeometry.setAttribute(
      'position',
      new THREE.BufferAttribute(linePositions, 3)
    )

    // Line material: crisp, delicate warm-charcoal stems
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x909088,
      transparent: true,
      opacity: 0.62,
      linewidth: 1,
    })

    const lineSegments = new THREE.LineSegments(lineGeometry, lineMaterial)
    rootGroup.add(lineSegments)

    // 6. Interaction Physics Model (Movable in EVERY Direction + Momentum)
    let isDragging = false
    let lastPointerX = 0
    let lastPointerY = 0

    // Rotation angles
    let rotX = 0.05
    let rotY = 0
    let velX = 0
    let velY = 0

    // Continuous anticlockwise rotation (negative Y rotation)
    const autoSpeed = -0.0032

    // Hover parallax tracking
    let normMouseX = 0
    let normMouseY = 0
    let curHoverTiltX = 0
    let curHoverTiltY = 0

    // Tracked Node for Leader Line (Node 7: golden-yellow node in upper-right)
    let trackedNodeIndex = 7

    const raycaster = new THREE.Raycaster()
    const mouseVector = new THREE.Vector2()

    const onPointerDown = (e: PointerEvent) => {
      isDragging = true
      lastPointerX = e.clientX
      lastPointerY = e.clientY
      velX = 0
      velY = 0
      canvas.setPointerCapture(e.pointerId)
      container.style.cursor = 'grabbing'
    }

    const onPointerMove = (e: PointerEvent) => {
      const rect = container.getBoundingClientRect()
      normMouseX = (e.clientX - rect.left) / rect.width - 0.5
      normMouseY = (e.clientY - rect.top) / rect.height - 0.5

      if (!isDragging) {
        // Raycast to check for hover over nodes
        mouseVector.x = ((e.clientX - rect.left) / rect.width) * 2 - 1
        mouseVector.y = -(((e.clientY - rect.top) / rect.height) * 2 - 1)
        raycaster.setFromCamera(mouseVector, camera)
        const intersects = raycaster.intersectObjects(meshes)
        if (intersects.length > 0 && intersects[0].object.userData?.id !== undefined) {
          const hoveredId = intersects[0].object.userData.id
          if (hoveredId > 0 && hoveredId !== trackedNodeIndex) {
            trackedNodeIndex = hoveredId
            const node = nodes[hoveredId]
            setActiveDotColor(node.color)
            if (node.label) {
              setActiveTelemetry(node.label)
            }
          }
        }
        return
      }

      const deltaX = e.clientX - lastPointerX
      const deltaY = e.clientY - lastPointerY
      lastPointerX = e.clientX
      lastPointerY = e.clientY

      const sensitivity = 0.0058
      // Dragging horizontally rotates yaw, dragging vertically rotates pitch
      rotY += deltaX * sensitivity
      rotX += deltaY * sensitivity

      // Clamp vertical pitch smoothly between -82° and +82° to prevent flip
      rotX = Math.max(-1.43, Math.min(1.43, rotX))

      // Track rotational velocity for momentum
      velY = deltaX * sensitivity
      velX = deltaY * sensitivity
    }

    const onPointerUp = (e: PointerEvent) => {
      if (isDragging) {
        isDragging = false
        try {
          canvas.releasePointerCapture(e.pointerId)
        } catch {
          // ignore
        }
        container.style.cursor = 'grab'
      }
    }

    const onWheel = (e: WheelEvent) => {
      e.preventDefault()
      cameraZ = Math.max(300, Math.min(580, cameraZ + e.deltaY * 0.35))
    }

    canvas.addEventListener('pointerdown', onPointerDown)
    window.addEventListener('pointermove', onPointerMove)
    window.addEventListener('pointerup', onPointerUp)
    window.addEventListener('pointercancel', onPointerUp)
    canvas.addEventListener('wheel', onWheel, { passive: false })
    container.style.cursor = 'grab'

    // 7. High-Performance Render Loop (60-120fps)
    let animId: number
    const tempProj = new THREE.Vector3()

    const animate = (now: number) => {
      const time = now * 0.001

      // A. Organic Breathing Waves (Stems and nodes gently breathe in 3D)
      const linePosAttr = lineGeometry.attributes.position as THREE.BufferAttribute
      const positions = linePosAttr.array as Float32Array

      let lineIdx = 0

      // Update Center Hub Position
      const centerNode = nodes[0]
      centerNode.currentPos.set(0, 0, 0)
      meshes[0].position.set(0, 0, 0)

      for (let i = 1; i < nodes.length; i++) {
        const node = nodes[i]
        const breath = Math.sin(time * 1.1 + node.phase) * 0.035

        node.currentPos.x =
          node.basePos.x * (1 + breath) +
          Math.sin(time * 0.8 + node.phase * 1.2) * 1.2
        node.currentPos.y =
          node.basePos.y * (1 + breath) +
          Math.cos(time * 0.7 + node.phase * 1.1) * 1.2
        node.currentPos.z =
          node.basePos.z * (1 + breath) +
          Math.sin(time * 0.9 + node.phase * 0.9) * 1.2

        meshes[i].position.copy(node.currentPos)

        // Radial stem from origin (0,0,0) to node
        positions[lineIdx++] = 0
        positions[lineIdx++] = 0
        positions[lineIdx++] = 0

        positions[lineIdx++] = node.currentPos.x
        positions[lineIdx++] = node.currentPos.y
        positions[lineIdx++] = node.currentPos.z
      }

      linePosAttr.needsUpdate = true

      // B. Motion & Movable Physics (Anticlockwise Rotation + Inertia)
      if (!isDragging) {
        // Inertia damping
        if (Math.abs(velX) > 0.0001 || Math.abs(velY) > 0.0001) {
          rotX += velX
          rotY += velY
          velX *= 0.938
          velY *= 0.938
          rotX = Math.max(-1.43, Math.min(1.43, rotX))
        }
        // Continuous anticlockwise rotation around Y axis
        rotY += autoSpeed
      }

      // Smooth hover parallax tilt
      curHoverTiltX += (normMouseY * 0.18 - curHoverTiltX) * 0.06
      curHoverTiltY += (normMouseX * 0.24 - curHoverTiltY) * 0.06

      // Subtle 3D precession wave for rich dimensional aesthetics
      const precessionX = Math.sin(time * 0.5) * 0.04
      const precessionZ = Math.cos(time * 0.4) * 0.03

      rootGroup.rotation.x = rotX + curHoverTiltX + precessionX
      rootGroup.rotation.y = rotY + curHoverTiltY
      rootGroup.rotation.z = precessionZ

      // Camera smooth zoom
      camera.position.z += (cameraZ - camera.position.z) * 0.08

      // Render Scene
      renderer.render(scene, camera)

      // C. Update Leader Line & Pill Overlay
      const trackedMesh = meshes[trackedNodeIndex] || meshes[7]
      if (trackedMesh && pillRef.current && leaderPathRef.current) {
        tempProj.copy(trackedMesh.position)
        tempProj.applyMatrix4(rootGroup.matrixWorld)

        const isFrontFacing = tempProj.z > -160
        tempProj.project(camera)

        const screenX = (tempProj.x * 0.5 + 0.5) * width
        const screenY = (-tempProj.y * 0.5 + 0.5) * height

        // Calculate pill anchor point inside bounds
        const isRightSide = screenX > width * 0.5
        let targetPillX = isRightSide
          ? Math.min(width - 16, Math.max(screenX + 50, width * 0.65))
          : Math.max(16, Math.min(screenX - 50, width * 0.35))

        let targetPillY = Math.max(34, Math.min(height - 34, screenY - 24))

        // Connect SVG leader line from node to pill
        const pillAnchorX = isRightSide ? targetPillX - 14 : targetPillX + 14
        const pillAnchorY = targetPillY

        const midX = screenX + (pillAnchorX - screenX) * 0.5
        const svgD = `M ${screenX.toFixed(1)} ${screenY.toFixed(
          1
        )} C ${midX.toFixed(1)} ${screenY.toFixed(
          1
        )}, ${midX.toFixed(1)} ${pillAnchorY.toFixed(
          1
        )}, ${pillAnchorX.toFixed(1)} ${pillAnchorY.toFixed(1)}`

        leaderPathRef.current.setAttribute('d', svgD)

        if (leaderOriginDotRef.current) {
          leaderOriginDotRef.current.setAttribute('cx', screenX.toFixed(1))
          leaderOriginDotRef.current.setAttribute('cy', screenY.toFixed(1))
        }
        if (leaderTargetDotRef.current) {
          leaderTargetDotRef.current.setAttribute('cx', pillAnchorX.toFixed(1))
          leaderTargetDotRef.current.setAttribute('cy', pillAnchorY.toFixed(1))
        }

        pillRef.current.style.left = `${targetPillX}px`
        pillRef.current.style.top = `${targetPillY}px`
        pillRef.current.style.transform = isRightSide
          ? 'translateX(-100%) translateY(-50%) scaleY(1)'
          : 'translateX(0px) translateY(-50%) scaleY(1)'

        const opacity = isFrontFacing ? 1 : 0.3
        leaderPathRef.current.style.opacity = `${opacity}`
        pillRef.current.style.opacity = `${opacity}`
      }

      animId = requestAnimationFrame(animate)
    }

    animId = requestAnimationFrame(animate)

    // 8. Resize Handler
    const handleResize = () => {
      if (!container) return
      width = container.clientWidth
      height = container.clientHeight
      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
    }

    window.addEventListener('resize', handleResize)

    // 9. Cleanup
    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', handleResize)
      canvas.removeEventListener('pointerdown', onPointerDown)
      window.removeEventListener('pointermove', onPointerMove)
      window.removeEventListener('pointerup', onPointerUp)
      window.removeEventListener('pointercancel', onPointerUp)
      canvas.removeEventListener('wheel', onWheel)

      sharedSphereGeo.dispose()
      lineGeometry.dispose()
      lineMaterial.dispose()
      materialCache.forEach((m) => m.dispose())
      renderer.dispose()
    }
  }, [])

  return (
    <div
      ref={containerRef}
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        overflow: 'visible',
        userSelect: 'none',
        touchAction: 'none',
      }}
    >
      {/* 3D WebGL Canvas */}
      <canvas
        ref={canvasRef}
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
        }}
      />

      {/* Worldview Telemetry Overlay (Exact HTML Structure from DevTools) */}
      <div className="wv-label-overlay" style={{ display: 'block' }}>
        {/* SVG Leader Line connecting 3D projected node to pill */}
        <svg
          className="wv-leader-svg"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            ref={leaderPathRef}
            d=""
            fill="none"
            stroke={activeDotColor}
            strokeWidth="1.25"
            strokeDasharray="3 3"
            strokeLinecap="round"
          />
          <circle
            ref={leaderOriginDotRef}
            cx="0"
            cy="0"
            r="3"
            fill={activeDotColor}
          />
          <circle
            ref={leaderTargetDotRef}
            cx="0"
            cy="0"
            r="2"
            fill={activeDotColor}
          />
        </svg>

        {/* Floating Telemetry Pill (Directly matching inspect element snippet) */}
        <div
          ref={pillRef}
          className="wv-pill"
          style={{
            ['--wv-pill-size' as any]: 0.65,
            ['--wv-pill-bg' as any]: 'rgba(255, 255, 255, 0.55)',
            ['--wv-pill-text' as any]: '#1a1714',
            ['--wv-pill-border' as any]: 'rgba(26, 23, 20, 0.08)',
            ['--wv-pill-dot' as any]: activeDotColor,
            transform: 'translateX(0px) translateY(-50%) scaleY(1)',
            opacity: 1,
            left: '0px',
            top: '0px',
          }}
        >
          <span
            ref={pillDotRef}
            className="wv-pill-dot-indicator"
            style={{ background: activeDotColor }}
          />
          <span ref={pillTextRef} style={{ whiteSpace: 'nowrap' }}>
            {activeTelemetry}
          </span>
        </div>
      </div>
    </div>
  )
}
