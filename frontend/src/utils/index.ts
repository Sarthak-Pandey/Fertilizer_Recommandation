/* ============================================================
   Fieldwise — Utility functions
   ============================================================ */

/**
 * Format a confidence value as a percentage string.
 */
export function formatConfidence(value: number): string {
  return `${value.toFixed(1)}%`;
}

/**
 * Generate a short UUID-like prediction ID.
 */
export function generateId(): string {
  const hex = () => Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0');
  return `${hex()}${hex()}-${hex()}-`;
}

/**
 * Clamp a number between min and max.
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
