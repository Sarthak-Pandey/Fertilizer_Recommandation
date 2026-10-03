import { useRef, useEffect } from 'react'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

// ─── Left Stages Data ────────────────────────────────────────────────────────

interface LeftStage {
  id: string
  badge: string
  title: string
  body: string
}

const LEFT_STAGES: LeftStage[] = [
  {
    id: 'vision',
    badge: 'THE VISION',
    title: 'Production should\nrun itself.',
    body: 'Production is too complex to run manually. Engineers should set direction, ship product, and approve important changes. The rest should be handled autonomously.',
  },
  {
    id: 'worldmodel',
    badge: 'THE WORLD MODEL',
    title: 'A layer that owns\nthe runtime.',
    body: 'At its core sits a live world model, a continuous understanding of how your stack behaves. On top, an army of specialized agents acts on the model to diagnose, fix, prevent, and answer any question.',
  },
  {
    id: 'autonomous',
    badge: 'THE AUTONOMOUS LAYER',
    title: 'Everyone else watches.\nWe operate.',
    body: 'Most software stops at recommendations and assistance, keeping humans in the loop as the operational layer. Antimetal is designed to continuously investigate, operate, and improve production systems itself.',
  },
]

// ─── Integration Brand Chips Data ────────────────────────────────────────────

const INTEGRATIONS = [
  { id: 'k8s', name: 'Kubernetes', icon: '/assets/landing/integrations/k8s.png' },
  { id: 'grafana', name: 'Grafana', icon: '/assets/landing/integrations/grafana.png' },
  { id: 'github', name: 'GitHub', icon: '/assets/landing/integrations/github.png' },
  { id: 'datadog', name: 'Datadog', icon: '/assets/landing/integrations/datadog.png' },
  { id: 'aws', name: 'AWS', icon: '/assets/landing/integrations/aws.png' },
  { id: 'linear', name: 'Linear', icon: '/assets/landing/integrations/linear.png' },
  { id: 'cloudflare', name: 'Cloudflare', icon: '/assets/landing/integrations/cloudflare.png' },
  { id: 'pagerduty', name: 'PagerDuty', icon: '/assets/landing/integrations/pagerduty.png' },
]

// ─── Sub-components ──────────────────────────────────────────────────────────

function CornerBrackets({ className = '' }: { className?: string }) {
  return (
    <>
      <span className={`vstack-bracket vstack-bracket-tl ${className}`} />
      <span className={`vstack-bracket vstack-bracket-tr ${className}`} />
      <span className={`vstack-bracket vstack-bracket-bl ${className}`} />
      <span className={`vstack-bracket vstack-bracket-br ${className}`} />
    </>
  )
}

function DepthWireframe({ hasConnector = false }: { hasConnector?: boolean }) {
  return (
    <div className="vstack-card-depth" aria-hidden="true">
      <span className="depth-line depth-tr" />
      <span className="depth-line depth-br" />
      <span className="depth-line depth-bl" />
      <span className="depth-line depth-back" />
      {hasConnector && <span className="depth-line depth-connector-left" />}
    </div>
  )
}

function RightCard({
  title,
  subtitle,
  children,
  className = '',
  hasDepth = true,
  hasConnector = false,
}: {
  title: string
  subtitle: string
  children?: React.ReactNode
  className?: string
  hasDepth?: boolean
  hasConnector?: boolean
}) {
  return (
    <div className={`vstack-card ${className}`}>
      <CornerBrackets />
      {hasDepth && <DepthWireframe hasConnector={hasConnector} />}
      <div className="vstack-card-inner">
        <h3 className="vstack-card-title">{title}</h3>
        <p className="vstack-card-subtitle">{subtitle}</p>
        {children}
      </div>
    </div>
  )
}

// ─── Main Component ──────────────────────────────────────────────────────────

export default function ProductOverview() {
  const sectionRef = useRef<HTMLDivElement>(null)
  const leftTrackRef = useRef<HTMLDivElement>(null)
  const stackRef = useRef<HTMLDivElement>(null)
  const middleLayerRef = useRef<HTMLDivElement>(null)
  const agentsCardRef = useRef<HTMLDivElement>(null)
  const dotBoxRef = useRef<HTMLDivElement>(null)
  const worldModelCardRef = useRef<HTMLDivElement>(null)
  const integrationsRef = useRef<HTMLDivElement>(null)
  const productionCardRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const section = sectionRef.current
      if (!section) return

      const leftCards = section.querySelectorAll('.vstage-card')
      const depthLines = section.querySelectorAll('.vstack-card-depth')

      ScrollTrigger.create({
        trigger: section,
        start: 'top top',
        end: '+=3000',
        pin: true,
        anticipatePin: 1,
        scrub: 1,
        onUpdate(self) {
          const p = self.progress

          // ─── 1. LEFT COLUMN TRANSLATION & CARD STATES ─────────────────────
          const cardStep = 338 // height + gap in px

          let trackY = 0
          if (p < 0.28) {
            trackY = 0
          } else if (p < 0.40) {
            const t = gsap.utils.mapRange(0.28, 0.40, 0, 1, p)
            trackY = -cardStep * t
          } else if (p < 0.64) {
            trackY = -cardStep
          } else if (p < 0.76) {
            const t = gsap.utils.mapRange(0.64, 0.76, 0, 1, p)
            trackY = -cardStep * (1 + t)
          } else {
            trackY = -cardStep * 2
          }

          if (leftTrackRef.current) {
            gsap.set(leftTrackRef.current, { y: trackY })
          }

          // Card 0 active weight: 1 -> 0 between 0.28 and 0.38
          const a0 = p < 0.28 ? 1 : p > 0.38 ? 0 : gsap.utils.mapRange(0.28, 0.38, 1, 0, p)
          // Card 1 active weight: 0 -> 1 between 0.30 and 0.40, 1 -> 0 between 0.64 and 0.74
          const a1In = p < 0.30 ? 0 : p > 0.40 ? 1 : gsap.utils.mapRange(0.30, 0.40, 0, 1, p)
          const a1Out = p < 0.64 ? 0 : p > 0.74 ? 1 : gsap.utils.mapRange(0.64, 0.74, 0, 1, p)
          const a1 = a1In * (1 - a1Out)
          // Card 2 active weight: 0 -> 1 between 0.66 and 0.78
          const a2 = p < 0.66 ? 0 : p > 0.78 ? 1 : gsap.utils.mapRange(0.66, 0.78, 0, 1, p)

          const weights = [a0, a1, a2]
          leftCards.forEach((card, idx) => {
            const w = weights[idx] ?? 0
            const darkBg = card.querySelector('.vstage-dark-bg')
            const activeContent = card.querySelector('.vstage-content-active')
            const inactiveContent = card.querySelector('.vstage-content-inactive')
            const brackets = card.querySelectorAll('.vstage-bracket')

            if (darkBg) gsap.set(darkBg, { opacity: w })
            if (activeContent) gsap.set(activeContent, { opacity: w })
            if (inactiveContent) gsap.set(inactiveContent, { opacity: 1 - w })
            if (brackets.length) gsap.set(brackets, { opacity: 1 - w })
          })

          // ─── 2. RIGHT COLUMN ISOMETRIC 3D TILT & DEPTH WIREFRAME ─────────
          // Enters tilt 0.04 -> 0.18, stays tilted 0.18 -> 0.75, flattens 0.75 -> 0.92
          let tiltWeight = 0
          if (p < 0.04) {
            tiltWeight = 0
          } else if (p < 0.18) {
            tiltWeight = gsap.utils.mapRange(0.04, 0.18, 0, 1, p)
          } else if (p < 0.75) {
            tiltWeight = 1
          } else if (p < 0.92) {
            tiltWeight = gsap.utils.mapRange(0.75, 0.92, 1, 0, p)
          } else {
            tiltWeight = 0
          }

          const currentSkewY = -9.5 * tiltWeight
          const currentScaleY = 1 - 0.04 * tiltWeight

          if (stackRef.current) {
            gsap.set(stackRef.current, {
              transform: `skewY(${currentSkewY}deg) scaleY(${currentScaleY})`,
            })
          }

          if (depthLines.length) {
            gsap.set(depthLines, { opacity: tiltWeight })
          }

          // ─── 3. MIDDLE LAYERS STAGGERED REVEAL ────────────────────────────
          // Agents card reveal: 0.16 -> 0.32
          const agentsProgress = p < 0.16 ? 0 : p > 0.32 ? 1 : gsap.utils.mapRange(0.16, 0.32, 0, 1, p)
          if (agentsCardRef.current) {
            gsap.set(agentsCardRef.current, {
              opacity: agentsProgress,
              x: (1 - agentsProgress) * 45,
            })
          }

          // Dot Box reveal: 0.20 -> 0.36
          const dotProgress = p < 0.20 ? 0 : p > 0.36 ? 1 : gsap.utils.mapRange(0.20, 0.36, 0, 1, p)
          if (dotBoxRef.current) {
            gsap.set(dotBoxRef.current, {
              opacity: dotProgress,
              scale: 0.92 + 0.08 * dotProgress,
            })
          }

          // World Model card reveal: 0.36 -> 0.52
          const wmProgress = p < 0.36 ? 0 : p > 0.52 ? 1 : gsap.utils.mapRange(0.36, 0.52, 0, 1, p)
          if (worldModelCardRef.current) {
            gsap.set(worldModelCardRef.current, {
              opacity: wmProgress,
              x: (1 - wmProgress) * 45,
            })
          }

          // Integration icons row reveal: 0.50 -> 0.68
          const integProgress = p < 0.50 ? 0 : p > 0.68 ? 1 : gsap.utils.mapRange(0.50, 0.68, 0, 1, p)
          if (integrationsRef.current) {
            gsap.set(integrationsRef.current, {
              opacity: integProgress,
              y: (1 - integProgress) * 20,
            })
          }
        },
      })
    }, sectionRef)

    return () => ctx.revert()
  }, [])

  return (
    <section ref={sectionRef} className="vstack-section" id="product">
      {/* Sticky two-column frame pinned by GSAP ScrollTrigger */}
      <div className="vstack-sticky-frame">

        {/* ── LEFT COLUMN: 3 stacked cards scrolling into focus ── */}
        <div className="vstack-left">
          <div className="vstack-left-viewport">
            <div ref={leftTrackRef} className="vstack-left-track">
              {LEFT_STAGES.map((stage, i) => (
                <div key={stage.id} className="vstage-card" data-stage={i}>
                  {/* Corner brackets for inactive state */}
                  <CornerBrackets className="vstage-bracket" />

                  {/* Dark background overlay for active state */}
                  <div className="vstage-dark-bg" />

                  {/* Inactive state content (dark text on dashed transparent) */}
                  <div className="vstage-content vstage-content-inactive">
                    <div className="vstage-badge">{stage.badge}</div>
                    <h2 className="vstage-title">
                      {stage.title.split('\n').map((line, li) => (
                        <span key={li}>
                          {line}
                          {li < stage.title.split('\n').length - 1 && <br />}
                        </span>
                      ))}
                    </h2>
                    <p className="vstage-body">{stage.body}</p>
                  </div>

                  {/* Active state content (white text on dark solid) */}
                  <div className="vstage-content vstage-content-active">
                    <div className="vstage-badge">{stage.badge}</div>
                    <h2 className="vstage-title">
                      {stage.title.split('\n').map((line, li) => (
                        <span key={li}>
                          {line}
                          {li < stage.title.split('\n').length - 1 && <br />}
                        </span>
                      ))}
                    </h2>
                    <p className="vstage-body">{stage.body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── RIGHT COLUMN: 3D isometric perspective card diagram ── */}
        <div className="vstack-right">
          <div ref={stackRef} className="vstack-3d-stack">

            {/* Card 1: Your Team (always visible) */}
            <RightCard
              title="Your Team"
              subtitle="Defines priorities, direction, and goals."
              className="vstack-card-team"
              hasDepth={true}
              hasConnector={true}
            />

            {/* Middle Section (Reveals on scroll) */}
            <div ref={middleLayerRef} className="vstack-middle-layer">
              {/* Grid: Left side has Agents & World Model; Right side has Dot Chevron Box */}
              <div className="vstack-middle-grid">
                {/* Left Sub-column */}
                <div className="vstack-middle-subcol">
                  {/* Card 2: Antimetal Agents */}
                  <div ref={agentsCardRef} className="vstack-subcard-wrap">
                    <RightCard
                      title="Antimetal Agents"
                      subtitle="Army of specialists that act on production."
                      className="vstack-card-agents"
                      hasDepth={true}
                      hasConnector={false}
                    />
                  </div>

                  {/* Card 3: Antimetal World Model */}
                  <div ref={worldModelCardRef} className="vstack-subcard-wrap">
                    <RightCard
                      title="Antimetal World Model"
                      subtitle="A live view of how your stack actually behaves."
                      className="vstack-card-worldmodel"
                      hasDepth={true}
                      hasConnector={true}
                    />
                  </div>
                </div>

                {/* Right Sub-column: Dot Pyramid Chevron Box */}
                <div ref={dotBoxRef} className="vstack-dot-box">
                  <CornerBrackets />
                  <DepthWireframe hasConnector={false} />
                  <div className="vstack-dot-box-inner">
                    {/* Exact 10-dot Chevron Formation from video */}
                    <svg
                      width="92"
                      height="84"
                      viewBox="0 0 120 110"
                      fill="none"
                      className="vstack-chevron-svg"
                      aria-hidden="true"
                    >
                      {/* Apex: 1 dot */}
                      <circle cx="60" cy="20" r="6" fill="#161514" />
                      {/* Row 2: 3 dots */}
                      <circle cx="44" cy="40" r="6" fill="#161514" />
                      <circle cx="60" cy="40" r="6" fill="#161514" />
                      <circle cx="76" cy="40" r="6" fill="#161514" />
                      {/* Row 3: 4 dots */}
                      <circle cx="28" cy="60" r="6" fill="#161514" />
                      <circle cx="44" cy="60" r="6" fill="#161514" />
                      <circle cx="76" cy="60" r="6" fill="#161514" />
                      <circle cx="92" cy="60" r="6" fill="#161514" />
                      {/* Row 4: 2 dots */}
                      <circle cx="28" cy="80" r="6" fill="#161514" />
                      <circle cx="92" cy="80" r="6" fill="#161514" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Horizontal Row of Integration Chips */}
              <div ref={integrationsRef} className="vstack-integrations-row">
                {INTEGRATIONS.map((integ) => (
                  <div key={integ.id} className="vstack-integ-chip" title={integ.name}>
                    <CornerBrackets />
                    <div className="vstack-integ-chip-inner">
                      <img
                        src={integ.icon}
                        alt={integ.name}
                        className="vstack-brand-img"
                      />
                    </div>
                  </div>
                ))}
                {/* "+ 92 more" chip */}
                <div className="vstack-integ-chip vstack-integ-more-chip">
                  <CornerBrackets />
                  <div className="vstack-integ-chip-inner">
                    <span className="vstack-integ-more-text">+ 92 more</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Card 4: Production (always visible at bottom) */}
            <div ref={productionCardRef} className="vstack-production-wrap">
              <RightCard
                title="Production"
                subtitle="Runtime systems, infrastructure, code execution, and everything around them."
                className="vstack-card-production"
                hasDepth={true}
                hasConnector={false}
              />
            </div>

          </div>
        </div>

      </div>
    </section>
  )
}
