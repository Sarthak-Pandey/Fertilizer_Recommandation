# 🌾 Fieldwise — Precision Fertilizer Intelligence (Frontend)

An enterprise-grade, editorial React 19 + TypeScript + Vite application powered by ensemble machine learning models for agronomic soil nutrient recommendation.

---

## 🎨 Visual Language & Design System

- **Aesthetic**: Premium, futuristic, minimal editorial AI startup aesthetic inspired by Antimetal design principles.
- **Palette**: Warm off-white canvas (`#DCDDD7`), near-black primary text (`#111111`), and subtle warm orange accent (`#FF6B00`).
- **Typography**: Editorial header typography in **Instrument Serif** paired with **Inter** for clean body text and **Outfit** for metrics.
- **Interactive Canvas Network**: Custom physics-backed HTML5 Canvas network (`NetworkVisualization.tsx`) featuring circular nodes of varying radii, connection edges, organic drift, magnetic cursor attraction, and an orange-rimmed central node.
- **Motion & Physics**: **GSAP + ScrollTrigger** entrance timelines and **Lenis** smooth scrolling.

---

## 🗺️ Route Architecture

```text
/                   → Public Editorial Landing Page (No Auth Required)
/login              → User Sign In
/register           → User Registration
/overview           → Main Agronomic Dashboard (Protected / Authenticated)
/history            → Telemetry Prediction History & Log
/audit              → ML Model Audit & Governance Metrics
```

---

## 🛠️ Stack & Dependencies

- **Framework**: React 19, Vite, TypeScript 5+
- **Routing**: React Router 7 (`react-router-dom`)
- **Animation**: GSAP 3, `@gsap/react`, ScrollTrigger
- **Smooth Scroll**: Lenis (`lenis`)
- **Icons**: Lucide React & Google Material Symbols Outlined

---

## 🚀 Running Locally

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start Vite dev server
npm run dev

# 4. Build production bundle
npm run build
```

The application will launch locally at `http://localhost:5173/` (or next available port).
