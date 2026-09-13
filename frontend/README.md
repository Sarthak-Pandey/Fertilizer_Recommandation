# Fieldwise — Agronomy Console Frontend

Production-quality frontend for the **Fieldwise Fertilizer Intelligence** system. This is an AI/ML-powered fertilizer recommendation console where users enter soil information and receive a recommendation with confidence scores, model trace, and audit trail.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## Technology Stack

| Technology | Purpose |
|---|---|
| React 19 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool & dev server |
| Tailwind CSS 4 | Utility-first CSS |
| Lucide React | Icon system |

## Architecture

```
UI (React Components)
         ↓
Service Layer (src/services/)
         ↓
Mock Recommendation Logic
         ↓
(Future: Backend API → ML Service)
```

### Current State

The frontend currently uses **deterministic mock logic** for fertilizer recommendations. The recommendation service (`src/services/recommendationService.ts`) returns predictions based on simple nutrient thresholds:

- **Low nitrogen** → Urea (95.2% confidence)
- **Low phosphorus** → DAP (88.1% confidence)
- **Low potassium** → MOP (79.3% confidence)

> ⚠️ **This is NOT a real ML inference.** The current recommendation is mock data and is not yet connected to the existing backend/ml-service.

### Future Integration

To connect to the real backend API, update `src/services/recommendationService.ts`:

```typescript
// Replace the mock implementation with:
export async function getRecommendation(input: SoilReading): Promise<RecommendationResult> {
  const response = await fetch('/api/recommendation', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      soil_ph: input.soilPh,
      nitrogen: input.nitrogen,
      phosphorus: input.phosphorus,
      potassium: input.potassium,
      growth_stage: input.growthStage,
    }),
  });
  return response.json();
}
```

No UI component changes are required — the service abstraction ensures the interface remains stable.

## Project Structure

```
frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── src/
│   ├── main.tsx            # Entry point
│   ├── App.tsx             # Root component
│   ├── index.css           # Design system & Tailwind
│   ├── components/
│   │   ├── AppShell.tsx
│   │   ├── Sidebar.tsx
│   │   ├── TopHeader.tsx
│   │   ├── PageHeader.tsx
│   │   ├── KpiCard.tsx
│   │   ├── SoilReadingCard.tsx
│   │   ├── SoilInput.tsx
│   │   ├── GrowthStageSelect.tsx
│   │   ├── RecommendationResult.tsx
│   │   ├── ModelTrace.tsx
│   │   ├── PredictionHistory.tsx
│   │   ├── PredictionRow.tsx
│   │   ├── DailyVolumeCard.tsx
│   │   ├── ServicePulse.tsx
│   │   ├── StatusBadge.tsx
│   │   └── Footer.tsx
│   ├── pages/
│   │   └── OverviewPage.tsx
│   ├── services/
│   │   └── recommendationService.ts
│   ├── data/
│   │   └── mockData.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── index.ts
└── public/
```

## Features

- **Soil reading form** with pH, N/P/K inputs and growth stage dropdown
- **Animated recommendation flow** with step-by-step loading states
- **Prediction history** with expandable rows and pagination
- **KPI dashboard** cards
- **Daily volume** analytics chart
- **Service pulse** system health monitor
- **Responsive design** — desktop, tablet, and mobile layouts
- **Keyboard accessible** with proper ARIA labels
- **Grid background** and polished visual design
