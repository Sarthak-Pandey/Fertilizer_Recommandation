/* ============================================================
   Fieldwise — Recommendation Service (Live API Integration)
   ============================================================
   Connects to the FastAPI backend for all data operations.

   Mock-fallback rule
   ──────────────────
   Falls back to local mock data ONLY on *connectivity* failures
   (network error, timeout, DNS — i.e. the backend never responded).

   A real HTTP error response (401, 422, 500) is NOT masked by mock
   data — it surfaces as a visible error so backend/contract bugs
   are caught, not silently hidden.
   ============================================================ */

import { apiClient, ApiError } from './apiClient';
import type {
  SoilReading,
  RecommendationResult,
  ModelTraceStep,
  PredictionRecord,
  KpiData,
  BackendRecommendRequest,
  BackendRecommendResponse,
  BackendPredictionListResponse,
  BackendStatsResponse,
  BackendHealthResponse,
  BackendPredictionItem,
} from '../types';
import {
  mockPredictionHistory,
  mockKpiData,
} from '../data/mockData';

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/** Map frontend camelCase SoilReading → backend PascalCase request body. */
function toBackendPayload(input: SoilReading): BackendRecommendRequest {
  return {
    Soil_pH: input.soilPh,
    Nitrogen_Level: input.nitrogen,
    Phosphorus_Level: input.phosphorus,
    Potassium_Level: input.potassium,
    Crop_Growth_Stage: input.growthStage,
  };
}

/** Build model-trace steps from a live API response. */
function buildLiveModelTrace(response: BackendRecommendResponse): ModelTraceStep[] {
  return [
    { label: 'Input validation', completed: response.success },
    { label: 'Feature preparation', completed: response.success },
    { label: `Model inference (${response.model_version})`, completed: response.success },
    { label: 'Recommendation generated', completed: response.success },
  ];
}

/** Build a user-facing rationale string from the API response. */
function buildRationale(input: SoilReading, response: BackendRecommendResponse): string {
  const confidence = response.confidence != null ? response.confidence.toFixed(1) : '—';
  return (
    `${response.fertilizer} recommended with ${confidence}% confidence ` +
    `for the ${input.growthStage} stage. ` +
    `Soil pH ${input.soilPh}, N ${input.nitrogen}, P ${input.phosphorus}, K ${input.potassium}. ` +
    `Model: ${response.model_version}.`
  );
}

/** Map a single BackendPredictionItem to the frontend PredictionRecord shape. */
function toPredictionRecord(item: BackendPredictionItem): PredictionRecord {
  const d = new Date(item.created_at);
  return {
    id: item.prediction_id,
    date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
    status: item.status === 'success' ? 'success' : 'error',
    recommendation: item.predicted_fertilizer,
    confidence: item.confidence ?? 0,
    capturedTime: d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
    soilPh: item.input_features?.Soil_pH ?? 0,
    nitrogen: item.input_features?.Nitrogen_Level ?? 0,
    phosphorus: item.input_features?.Phosphorus_Level ?? 0,
    potassium: item.input_features?.Potassium_Level ?? 0,
    growthStage: item.input_features?.Crop_Growth_Stage ?? 'Vegetative',
    modelVersion: item.model_version,
    auditStatus: item.status === 'success' ? 'Verified' : 'Error',
    fullTimestamp: item.created_at,
    latencyMs: item.latency_ms ?? undefined,
  };
}

/**
 * Returns true when the error represents a connectivity failure and
 * mock-fallback is appropriate. Returns false for HTTP errors (401,
 * 422, 500 …) — those must surface to the user.
 */
function isConnectivityFailure(err: unknown): boolean {
  return err instanceof ApiError && err.isConnectivityFailure;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Get a fertilizer recommendation from the live backend.
 *
 * On connectivity failure, falls back to a basic mock recommendation
 * so the UI remains functional during local-only development.
 *
 * On an HTTP error (401, 422, 500), throws — the caller must display
 * the error to the user.
 */
export async function getRecommendation(
  input: SoilReading,
  signal?: AbortSignal,
): Promise<RecommendationResult> {
  const payload = toBackendPayload(input);

  try {
    const response = await apiClient.post<BackendRecommendResponse>(
      '/fertilizer/recommend',
      payload,
      { signal },
    );

    return {
      recommendation: {
        product: response.fertilizer,
        confidence: response.confidence ?? 0,
        rationale: buildRationale(input, response),
      },
      modelTrace: buildLiveModelTrace(response),
      timestamp: new Date().toISOString(),
      predictionId: response.prediction_id ?? crypto.randomUUID(),
    };
  } catch (err) {
    // Mock fallback — ONLY for connectivity failures.
    if (isConnectivityFailure(err)) {
      console.warn('[recommendationService] Backend unreachable, using mock fallback.', err);
      return getMockRecommendation(input);
    }
    throw err;
  }
}

/**
 * Fetch paginated prediction history from the backend.
 * Falls back to mock data on connectivity failure.
 */
export async function fetchPredictions(
  page = 1,
  perPage = 20,
  signal?: AbortSignal,
): Promise<{ records: PredictionRecord[]; total: number; totalPages: number }> {
  try {
    const data = await apiClient.get<BackendPredictionListResponse>(
      `/predictions?page=${page}&per_page=${perPage}`,
      { signal },
    );

    return {
      records: data.items.map(toPredictionRecord),
      total: data.total,
      totalPages: data.total_pages,
    };
  } catch (err) {
    if (isConnectivityFailure(err)) {
      console.warn('[recommendationService] Backend unreachable for predictions, using mock.', err);
      return {
        records: [...mockPredictionHistory],
        total: mockPredictionHistory.length,
        totalPages: 1,
      };
    }
    throw err;
  }
}

/**
 * Fetch aggregated KPI stats from the backend.
 * Falls back to mock data on connectivity failure.
 */
export async function fetchKpiStats(
  signal?: AbortSignal,
): Promise<KpiData> {
  try {
    const data = await apiClient.get<BackendStatsResponse>(
      '/predictions/stats',
      { signal },
    );

    return {
      predictionsLogged: data.total_count,
      averageConfidence: data.average_confidence != null
        ? Math.round(data.average_confidence * 10) / 10
        : 0,
      frequentRecommendation: data.most_frequent_fertilizer ?? '—',
    };
  } catch (err) {
    if (isConnectivityFailure(err)) {
      console.warn('[recommendationService] Backend unreachable for stats, using mock.', err);
      return { ...mockKpiData };
    }
    throw err;
  }
}

/** Health check response shape for the frontend. */
export interface HealthStatus {
  backend: 'healthy' | 'degraded' | 'offline';
  mlService: 'healthy' | 'degraded' | 'offline';
  modelVersion: string;
}

/**
 * Fetch system health from the public `/health` endpoint.
 * Never falls back to mock — if health check fails, services are offline.
 */
export async function fetchHealthStatus(
  signal?: AbortSignal,
): Promise<HealthStatus> {
  try {
    const data = await apiClient.publicGet<BackendHealthResponse>('/health', { signal });

    return {
      backend: normaliseHealthStatus(data.backend),
      mlService: normaliseHealthStatus(data.ml_service?.status),
      modelVersion: data.ml_service?.model_version ?? 'unknown',
    };
  } catch {
    return {
      backend: 'offline',
      mlService: 'offline',
      modelVersion: 'unknown',
    };
  }
}

function normaliseHealthStatus(raw: string | undefined): 'healthy' | 'degraded' | 'offline' {
  if (raw === 'healthy') return 'healthy';
  if (raw === 'degraded') return 'degraded';
  return 'offline';
}

// ---------------------------------------------------------------------------
// Mock fallback (connectivity failure only)
// ---------------------------------------------------------------------------

/**
 * Deterministic mock recommendation used when the backend is unreachable.
 * Intentionally produces a distinguishable model version so the UI can
 * indicate "offline / mock" if desired.
 */
async function getMockRecommendation(input: SoilReading): Promise<RecommendationResult> {
  // Small artificial delay to avoid jarring instant results.
  await new Promise((r) => setTimeout(r, 600));

  const { nitrogen, phosphorus, potassium } = input;
  let product = 'Urea';
  let confidence = 95.2;

  if (potassium < 25 && nitrogen >= 50 && phosphorus >= 20) {
    product = 'MOP';
    confidence = 79.3;
  } else if (phosphorus < 20 && nitrogen >= 50) {
    product = 'DAP';
    confidence = 88.1;
  }

  const rationale =
    `[OFFLINE] ${product} recommended based on local heuristics. ` +
    `Connect the backend for ML-powered predictions.`;

  return {
    recommendation: { product, confidence, rationale },
    modelTrace: [
      { label: 'Input validation', completed: true },
      { label: 'Feature preparation', completed: true },
      { label: 'Model inference (offline)', completed: true },
      { label: 'Recommendation generated', completed: true },
    ],
    timestamp: new Date().toISOString(),
    predictionId: `mock-${crypto.randomUUID().slice(0, 8)}`,
  };
}
