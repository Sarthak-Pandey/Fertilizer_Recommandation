/* ============================================================
   Fieldwise Agronomy Console — API Client
   ============================================================
   Centralised fetch wrapper for the FastAPI backend.

   Features:
   - Configurable base URL and API key via Vite env vars
   - Per-request AbortController support (timeout + caller cancellation)
   - Typed error responses matching FastAPI's actual error shapes
   ============================================================ */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const API_BASE_URL: string =
  (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1';

const API_KEY: string =
  (import.meta as any).env?.VITE_API_KEY ?? 'dev-secret-key-123';

const DEFAULT_TIMEOUT_MS = 10_000;

// ---------------------------------------------------------------------------
// Error types
// ---------------------------------------------------------------------------

/**
 * Distinguishes "backend reachable but errored" from "backend unreachable".
 *
 * - `httpStatus` set  → backend responded with an error (401, 422, 500 …)
 * - `httpStatus` null → connectivity failure (network error, timeout, DNS)
 */
export class ApiError extends Error {
  /** HTTP status code, or `null` for connectivity failures. */
  httpStatus: number | null;
  /** Raw detail from the backend, if any. */
  detail: string | null;
  /** The underlying cause, if any (e.g. the original TypeError). */
  cause: unknown;

  constructor(
    message: string,
    httpStatus: number | null = null,
    detail: string | null = null,
    cause?: unknown,
  ) {
    super(message);
    this.name = 'ApiError';
    this.httpStatus = httpStatus;
    this.detail = detail;
    this.cause = cause;
  }

  /** True when the backend never responded (network error, timeout). */
  get isConnectivityFailure(): boolean {
    return this.httpStatus === null;
  }
}

/**
 * Thrown specifically on request timeout (a specialised connectivity failure).
 */
export class TimeoutError extends ApiError {
  constructor(url: string, timeoutMs: number) {
    super(
      `Request to ${url} timed out after ${timeoutMs}ms`,
      null,   // no HTTP status — server never responded
      null,
    );
    this.name = 'TimeoutError';
  }
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Parse FastAPI's error response body into a human-readable message.
 *
 * FastAPI produces two shapes:
 *   HTTPException       → { "detail": "string" }
 *   422 validation err  → { "detail": [ { "loc": [...], "msg": "…", "type": "…" } ] }
 */
async function parseErrorBody(response: Response): Promise<string> {
  try {
    const body = await response.json();

    // Standard HTTPException shape
    if (typeof body.detail === 'string') {
      return body.detail;
    }

    // Pydantic 422 validation shape
    if (Array.isArray(body.detail)) {
      return body.detail
        .map((err: { loc?: (string | number)[]; msg?: string }) => {
          const field = err.loc ? err.loc.slice(1).join('.') : 'unknown';
          return `${field}: ${err.msg ?? 'validation error'}`;
        })
        .join('; ');
    }

    // Generic backend error shape { "success": false, "error": "..." }
    if (typeof body.error === 'string') {
      return body.error;
    }

    return `HTTP ${response.status}`;
  } catch {
    return `HTTP ${response.status} (non-JSON response)`;
  }
}

// ---------------------------------------------------------------------------
// Core request function
// ---------------------------------------------------------------------------

interface RequestOptions {
  /** External AbortSignal for caller-driven cancellation. */
  signal?: AbortSignal;
  /** Per-request timeout in ms (default 10 000). */
  timeoutMs?: number;
  /** If true the request skips the X-API-Key header (for public endpoints). */
  public?: boolean;
}

/**
 * Low-level fetch wrapper. Prefer the convenience methods below.
 */
async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  opts: RequestOptions = {},
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  // Merge caller's signal with an internal timeout signal.
  const timeoutController = new AbortController();
  const timeoutId = setTimeout(() => timeoutController.abort(), timeoutMs);

  // If the caller supplied a signal, abort our controller when it fires.
  const callerSignal = opts.signal;
  const onCallerAbort = () => timeoutController.abort();
  callerSignal?.addEventListener('abort', onCallerAbort);

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (!opts.public) {
    headers['X-API-Key'] = API_KEY;
  }

  try {
    const response = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: timeoutController.signal,
    });

    if (!response.ok) {
      const detail = await parseErrorBody(response);
      throw new ApiError(
        `API ${method} ${path} failed: ${detail}`,
        response.status,
        detail,
      );
    }

    return (await response.json()) as T;
  } catch (err) {
    // Re-throw our own ApiError as-is.
    if (err instanceof ApiError) throw err;

    // Distinguish timeout from other abort/network errors.
    if (err instanceof DOMException && err.name === 'AbortError') {
      if (callerSignal?.aborted) {
        // Caller cancelled — propagate as a generic ApiError.
        throw new ApiError('Request cancelled', null, null, err);
      }
      throw new TimeoutError(url, timeoutMs);
    }

    // Network / DNS / CORS failure.
    throw new ApiError(
      `Network error: ${(err as Error).message ?? 'unknown'}`,
      null,
      null,
      err,
    );
  } finally {
    clearTimeout(timeoutId);
    callerSignal?.removeEventListener('abort', onCallerAbort);
  }
}

// ---------------------------------------------------------------------------
// Public convenience methods
// ---------------------------------------------------------------------------

export const apiClient = {
  /** Authenticated GET. */
  get<T>(path: string, opts?: RequestOptions): Promise<T> {
    return request<T>('GET', path, undefined, opts);
  },

  /** Authenticated POST. */
  post<T>(path: string, body: unknown, opts?: RequestOptions): Promise<T> {
    return request<T>('POST', path, body, opts);
  },

  /** Public (unauthenticated) GET — e.g. health checks. */
  publicGet<T>(path: string, opts?: RequestOptions): Promise<T> {
    return request<T>('GET', path, undefined, { ...opts, public: true });
  },
};
