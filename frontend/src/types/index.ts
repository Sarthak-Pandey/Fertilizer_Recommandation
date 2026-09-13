/* ============================================================
   Fieldwise Agronomy Console — Type Definitions
   ============================================================ */

export type GrowthStage =
  | 'Vegetative'
  | 'Reproductive'
  | 'Maturity'
  | 'Seedling'
  | 'Germination';

export interface SoilReading {
  soilPh: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  growthStage: GrowthStage;
}

export interface Recommendation {
  product: string;
  confidence: number;
  rationale: string;
}

export interface ModelTraceStep {
  label: string;
  completed: boolean;
}

export interface RecommendationResult {
  recommendation: Recommendation;
  modelTrace: ModelTraceStep[];
  timestamp: string;
  predictionId: string;
}

export type LoadingStep =
  | 'analyzing'
  | 'evaluating'
  | 'running'
  | 'complete';

export interface PredictionRecord {
  id: string;
  date: string;
  status: 'success' | 'error';
  recommendation: string;
  confidence: number;
  capturedTime: string;
  soilPh: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  growthStage: GrowthStage;
  modelVersion: string;
  auditStatus: string;
  fullTimestamp: string;
}

export interface KpiData {
  predictionsLogged: number;
  averageConfidence: number;
  frequentRecommendation: string;
}

export interface ServiceStatus {
  name: string;
  status: 'healthy' | 'degraded' | 'offline';
  type: string;
}

export interface DailyVolume {
  value: number;
  description: string;
  data: number[];
}

export type NavigationItem = 'overview' | 'prediction-history' | 'model-audit';
