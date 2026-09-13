/* ============================================================
   Fieldwise — Recommendation Service (Abstraction Layer)
   ============================================================
   
   Currently uses deterministic mock logic.
   Replace mockRecommendation() with a real API call later:
   
   POST /recommendation
   {
     soil_ph: number,
     nitrogen: number,
     phosphorus: number,
     potassium: number,
     growth_stage: string
   }
   ============================================================ */

import type { SoilReading, RecommendationResult, ModelTraceStep } from '../types';

function generatePredictionId(): string {
  const hex = () => Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0');
  return `${hex()}${hex()}-${hex()}-`;
}

function computeRecommendation(input: SoilReading): { product: string; confidence: number; rationale: string } {
  const { nitrogen, phosphorus, potassium } = input;

  // Deterministic thresholds
  const nitrogenLow = nitrogen < 50;
  const phosphorusLow = phosphorus < 20;
  const potassiumLow = potassium < 25;

  if (potassiumLow && !nitrogenLow && !phosphorusLow) {
    return {
      product: 'MOP',
      confidence: 79.3,
      rationale: `Potassium levels are critically low at ${potassium} mg/kg. MOP (Muriate of Potash) is recommended to restore nutrient balance for the ${input.growthStage.toLowerCase()} stage.`,
    };
  }

  if (phosphorusLow && !nitrogenLow) {
    return {
      product: 'DAP',
      confidence: 88.1,
      rationale: `Phosphorus demand is elevated at ${phosphorus} mg/kg for the current ${input.growthStage.toLowerCase()} stage. DAP (Diammonium Phosphate) provides the required phosphorus supplementation.`,
    };
  }

  if (nitrogenLow) {
    return {
      product: 'Urea',
      confidence: 95.2,
      rationale: `Nitrogen demand is elevated for the current ${input.growthStage.toLowerCase()} stage. Urea provides optimal nitrogen supplementation at the detected soil pH of ${input.soilPh}.`,
    };
  }

  // Default: balanced nutrients — recommend Urea
  return {
    product: 'Urea',
    confidence: 95.2,
    rationale: `Nitrogen demand is elevated for the current ${input.growthStage.toLowerCase()} stage. Soil nutrient balance suggests Urea as the primary recommendation.`,
  };
}

function buildModelTrace(): ModelTraceStep[] {
  return [
    { label: 'Input validation', completed: true },
    { label: 'Feature preparation', completed: true },
    { label: 'Model inference', completed: true },
    { label: 'Recommendation generated', completed: true },
  ];
}

/**
 * Mock recommendation — deterministic frontend logic.
 * 
 * To connect to the real backend later, replace the body of this
 * function with a fetch() call to POST /recommendation.
 */
export async function getRecommendation(input: SoilReading): Promise<RecommendationResult> {
  // Simulate network latency
  await new Promise((resolve) => setTimeout(resolve, 2800));

  const { product, confidence, rationale } = computeRecommendation(input);

  return {
    recommendation: {
      product,
      confidence,
      rationale,
    },
    modelTrace: buildModelTrace(),
    timestamp: new Date().toISOString(),
    predictionId: generatePredictionId(),
  };
}

/**
 * Future: Replace with real API call
 * 
 * export async function getRecommendation(input: SoilReading): Promise<RecommendationResult> {
 *   const response = await fetch('/api/recommendation', {
 *     method: 'POST',
 *     headers: { 'Content-Type': 'application/json' },
 *     body: JSON.stringify({
 *       soil_ph: input.soilPh,
 *       nitrogen: input.nitrogen,
 *       phosphorus: input.phosphorus,
 *       potassium: input.potassium,
 *       growth_stage: input.growthStage,
 *     }),
 *   });
 *   return response.json();
 * }
 */
