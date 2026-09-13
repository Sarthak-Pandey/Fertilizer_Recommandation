/* ============================================================
   Fieldwise Agronomy Console — Type Definitions
   ============================================================ */

// ---------------------------------------------------------------------------
// Frontend domain types
// ---------------------------------------------------------------------------

/**
 * Growth stage values — aligned with the backend CropGrowthStage enum
 * (backend/schemas/recommendation.py).
 */
export type GrowthStage =
  | 'Sowing'
  | 'Vegetative'
  | 'Flowering'
  | 'Harvest';

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
  latencyMs?: number;
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

export type NavigationItem =
  | 'overview'
  | 'soil-intelligence'
  | 'recommendations'
  | 'prediction-history'
  | 'model-audit'
  | 'system-health';

// ---------------------------------------------------------------------------
// Backend API contract types
// ---------------------------------------------------------------------------

/** POST /api/v1/fertilizer/recommend — request body */
export interface BackendRecommendRequest {
  Soil_pH: number;
  Nitrogen_Level: number;
  Phosphorus_Level: number;
  Potassium_Level: number;
  Crop_Growth_Stage: GrowthStage;
}

/** POST /api/v1/fertilizer/recommend — response body */
export interface BackendRecommendResponse {
  success: boolean;
  fertilizer: string;
  confidence: number | null;
  model_version: string;
  preprocessing_version: string;
  feature_schema_version: string;
  prediction_id: string | null;
  probabilities: Record<string, number> | null;
  latency_ms: number | null;
}

/** Single item inside GET /api/v1/predictions response */
export interface BackendPredictionItem {
  prediction_id: string;
  request_id: string | null;
  input_features: Record<string, any>;
  predicted_fertilizer: string;
  gate_decision: string | null;
  specialist_used: string | null;
  confidence: number | null;
  model_version: string;
  preprocessing_version: string;
  feature_schema_version: string;
  latency_ms: number | null;
  status: string;
  error_message: string | null;
  created_at: string;
}

/** GET /api/v1/predictions — paginated response */
export interface BackendPredictionListResponse {
  items: BackendPredictionItem[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

/** GET /api/v1/predictions/stats — response */
export interface BackendStatsResponse {
  total_count: number;
  average_confidence: number | null;
  most_frequent_fertilizer: string | null;
  daily_counts: Record<string, number>;
}

/** GET /api/v1/health — response */
export interface BackendHealthResponse {
  backend: string;
  ml_service: {
    status: string;
    model_version?: string;
    [key: string]: any;
  };
}
