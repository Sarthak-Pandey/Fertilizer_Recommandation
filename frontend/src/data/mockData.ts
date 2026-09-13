/* ============================================================
   Fieldwise — Mock Data
   ============================================================ */

import type { PredictionRecord, KpiData, ServiceStatus, DailyVolume } from '../types';

export const mockPredictionHistory: PredictionRecord[] = [
  {
    id: 'e36c9ac9-0668-',
    date: 'Sep 12, 2026',
    status: 'success',
    recommendation: 'Urea',
    confidence: 95.2,
    capturedTime: '07:10 PM',
    soilPh: 6.4,
    nitrogen: 42,
    phosphorus: 28,
    potassium: 35,
    growthStage: 'Vegetative',
    modelVersion: 'model-v1',
    auditStatus: 'Verified',
    fullTimestamp: '2026-09-12T19:10:00Z',
  },
  {
    id: '06c0f9f5-0269-',
    date: 'Sep 12, 2026',
    status: 'success',
    recommendation: 'DAP',
    confidence: 88.1,
    capturedTime: '07:03 PM',
    soilPh: 7.1,
    nitrogen: 55,
    phosphorus: 12,
    potassium: 40,
    growthStage: 'Reproductive',
    modelVersion: 'model-v1',
    auditStatus: 'Verified',
    fullTimestamp: '2026-09-12T19:03:00Z',
  },
  {
    id: 'e8e1b9bf-06ee-',
    date: 'Sep 12, 2026',
    status: 'success',
    recommendation: 'MOP',
    confidence: 79.3,
    capturedTime: '06:51 PM',
    soilPh: 5.8,
    nitrogen: 60,
    phosphorus: 45,
    potassium: 15,
    growthStage: 'Maturity',
    modelVersion: 'model-v1',
    auditStatus: 'Verified',
    fullTimestamp: '2026-09-12T18:51:00Z',
  },
  {
    id: '0f8bdae0-4d05-',
    date: 'Sep 12, 2026',
    status: 'success',
    recommendation: 'Urea',
    confidence: 95.2,
    capturedTime: '06:26 PM',
    soilPh: 6.4,
    nitrogen: 42,
    phosphorus: 28,
    potassium: 35,
    growthStage: 'Vegetative',
    modelVersion: 'model-v1',
    auditStatus: 'Verified',
    fullTimestamp: '2026-09-12T18:26:00Z',
  },
];

export const mockKpiData: KpiData = {
  predictionsLogged: 156,
  averageConfidence: 98.6,
  frequentRecommendation: 'Urea',
};

export const mockServiceStatuses: ServiceStatus[] = [
  { name: 'Recommendation API', status: 'healthy', type: 'REST' },
  { name: 'ML inference service', status: 'healthy', type: 'model-v1' },
];

export const mockDailyVolume: DailyVolume = {
  value: 12,
  description: 'Predictions processed over the last 7 recorded days',
  data: [3, 7, 5, 9, 4, 12, 8],
};

export const defaultSoilReading = {
  soilPh: 6.4,
  nitrogen: 48.0,
  phosphorus: 20.0,
  potassium: 30.0,
  growthStage: 'Vegetative' as const,
};
