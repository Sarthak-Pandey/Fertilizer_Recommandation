export interface TimelineItemData {
  id: string
  timestamp: number // Normalized timestamp in milliseconds or arbitrary units
  dateLabel: string // e.g. "Jun 14, 09:42"
  title: string     // e.g. "Urea 46-0-0"
  subtitle?: string  // e.g. "Vegetative V4"
  status?: string    // e.g. "Deployed" | "In Review" | "Field Verified"
  badge?: string
  confidence?: number // e.g. 99.1
  latency?: number    // e.g. 28
  soilPh?: number
  n?: number
  p?: number
  k?: number
  stage?: string
  dotColor?: string  // e.g. "#E5A700", "#10B981"
  size?: number      // e.g. 0.61, 0.85, 1.0
  pillBg?: string
  pillText?: string
  pillBorder?: string
}

export interface PillPosition {
  x: number
  y: number
  trackX: number
  trackY: number
  scale: number
  opacity: number
  visible: boolean
  size: number
  dotColor: string
  bg: string
  text: string
  border: string
  item: TimelineItemData
}

export interface TimelineTheme {
  primaryDot: string
  trackColor: string
  rulerColor: string
  needleColor: string
  needleGlow: string
}
