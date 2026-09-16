export interface UserProfile {
  id: string
  email: string
  full_name?: string
  role?: string
  organization?: string
  created_at?: string
}

export interface UserRegisterPayload {
  email: string
  password: string
  full_name?: string
  role?: string
  organization?: string
}

export interface UserLoginPayload {
  email: string
  password: string
}

export interface AuthTokenResponse {
  access_token: string
  refresh_token?: string
  token_type: string
  user: UserProfile
}

export interface RecommendRequest {
  Soil_pH: number
  Nitrogen_Level: number
  Phosphorus_Level: number
  Potassium_Level: number
  Crop_Growth_Stage: string
  Soil_Type?: string
  Soil_Moisture?: number
  Temperature?: number
  Humidity?: number
  Rainfall?: number
  Crop_Type?: string
}

export interface RecommendResponse {
  success: boolean
  fertilizer: string
  confidence?: number
  model_version: string
  preprocessing_version: string
  feature_schema_version: string
  prediction_id?: string
  probabilities?: Record<string, number>
  latency_ms?: number
  error?: string
}

export interface PredictionDetail {
  prediction_id: string
  request_id?: string
  input_features: Record<string, any>
  predicted_fertilizer: string
  gate_decision?: string
  specialist_used?: string
  confidence?: number
  model_version: string
  preprocessing_version: string
  feature_schema_version: string
  latency_ms?: number
  status: string
  error_message?: string
  created_at: string
}

export interface PredictionListResponse {
  items: PredictionDetail[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

export interface PredictionStatsResponse {
  total_count: number
  average_confidence?: number
  most_frequent_fertilizer?: string
  daily_counts: Record<string, number>
}

export interface HealthResponse {
  backend: string
  ml_service: {
    status: string
    model_version?: string
    [key: string]: any
  } | string
}

export interface ReadinessResponse {
  backend: string
  ml_service: {
    status: string
    model_loaded?: boolean
    model_version?: string
    [key: string]: any
  } | string
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_KEY = import.meta.env.VITE_API_KEY || 'dev-secret-key-123'

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL.replace(/\/$/, '')}${endpoint}`
  const token = localStorage.getItem('auth_token')

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
    ...(options.headers as Record<string, string>),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (!response.ok) {
    let errorMessage = `HTTP error ${response.status}`
    try {
      const errJson = await response.json()
      if (errJson.detail) {
        errorMessage = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      } else if (errJson.error) {
        errorMessage = errJson.error
      }
    } catch {
      // Failed to parse JSON error, use default status text
    }
    throw new Error(errorMessage)
  }

  return response.json()
}

export const api = {
  // Authentication API Endpoints
  async register(data: UserRegisterPayload): Promise<AuthTokenResponse> {
    return request<AuthTokenResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async login(data: UserLoginPayload): Promise<AuthTokenResponse> {
    return request<AuthTokenResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async getMe(): Promise<UserProfile> {
    return request<UserProfile>('/api/v1/auth/me', {
      method: 'GET',
    })
  },

  async logout(): Promise<{ success: boolean; message: string }> {
    return request<{ success: boolean; message: string }>('/api/v1/auth/logout', {
      method: 'POST',
    })
  },

  // Prediction & Core System API Endpoints
  async recommendFertilizer(data: RecommendRequest): Promise<RecommendResponse> {
    return request<RecommendResponse>('/api/v1/fertilizer/recommend', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  async getPredictions(page = 1, perPage = 20): Promise<PredictionListResponse> {
    return request<PredictionListResponse>(`/api/v1/predictions?page=${page}&per_page=${perPage}`, {
      method: 'GET',
    })
  },

  async getPredictionStats(): Promise<PredictionStatsResponse> {
    return request<PredictionStatsResponse>('/api/v1/predictions/stats', {
      method: 'GET',
    })
  },

  async getPredictionById(id: string): Promise<PredictionDetail> {
    return request<PredictionDetail>(`/api/v1/predictions/${id}`, {
      method: 'GET',
    })
  },

  async getSystemHealth(): Promise<HealthResponse> {
    return request<HealthResponse>('/api/v1/health', {
      method: 'GET',
    })
  },

  async getSystemReadiness(): Promise<ReadinessResponse> {
    return request<ReadinessResponse>('/api/v1/ready', {
      method: 'GET',
    })
  },
}

