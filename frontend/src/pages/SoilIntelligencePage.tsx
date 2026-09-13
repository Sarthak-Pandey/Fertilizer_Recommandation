import { useState } from 'react';
import SoilReadingCard from '../components/SoilReadingCard';
import RecommendationResult from '../components/RecommendationResult';
import { getRecommendation } from '../services/recommendationService';
import { defaultSoilReading } from '../data/mockData';
import type { SoilReading, RecommendationResult as RecommendationResultType, LoadingStep } from '../types';

export default function SoilIntelligencePage() {
  const [soilReading, setSoilReading] = useState<SoilReading>({ ...defaultSoilReading });
  const [result, setResult] = useState<RecommendationResultType | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<LoadingStep | null>(null);

  const handleGenerate = async () => {
    if (isLoading) return;
    setIsLoading(true);
    setResult(null);

    const steps: LoadingStep[] = ['analyzing', 'evaluating', 'running', 'complete'];
    for (const step of steps) {
      setLoadingStep(step);
      await new Promise((r) => setTimeout(r, 300));
    }

    try {
      const rec = await getRecommendation(soilReading);
      setResult(rec);
    } finally {
      setIsLoading(false);
      setLoadingStep(null);
    }
  };

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-[#09262A] tracking-tight">Soil Intelligence Workspace</h1>
        <p className="text-xs text-[#64748B]">
          Detailed plot composition analysis, pH balancing, and N-P-K nutrient probe evaluation.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SoilReadingCard
          reading={soilReading}
          onChange={setSoilReading}
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />
        <RecommendationResult
          result={result}
          isLoading={isLoading}
          loadingStep={loadingStep}
        />
      </div>
    </div>
  );
}
