import { useState, useEffect } from 'react';
import { BookOpen } from 'lucide-react';
import RecommendationResult from '../components/RecommendationResult';
import { getRecommendation } from '../services/recommendationService';
import { defaultSoilReading } from '../data/mockData';
import type { RecommendationResult as RecommendationResultType } from '../types';

export default function FertilizerRecommendationsPage() {
  const [result, setResult] = useState<RecommendationResultType | null>(null);

  useEffect(() => {
    getRecommendation(defaultSoilReading).then(setResult).catch(() => {});
  }, []);

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-[#09262A] tracking-tight">Fertilizer Recommendation Engine</h1>
        <p className="text-xs text-[#64748B]">
          AI inference output inspection, candidate probability distribution breakdown, and application guides.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecommendationResult result={result} isLoading={false} loadingStep={null} />

        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-2xs">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-[#10B981]" />
            <h3 className="text-base font-extrabold text-[#09262A]">Standard Fertilizer Product Specifications</h3>
          </div>
          <div className="space-y-3">
            <div className="p-3.5 bg-[#F9F8F5] rounded-xl border border-[#E2E8F0]">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sm text-[#09262A]">Urea (46-0-0)</span>
                <span className="text-[0.65rem] font-mono px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">Nitrogen Rich</span>
              </div>
              <p className="text-xs text-[#64748B]">
                High-nitrogen synthetic fertilizer ideal for vegetative growth stages and severe nitrogen deficit correction.
              </p>
            </div>
            <div className="p-3.5 bg-[#F9F8F5] rounded-xl border border-[#E2E8F0]">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sm text-[#09262A]">DAP (18-46-0)</span>
                <span className="text-[0.65rem] font-mono px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold">Phosphorus Rich</span>
              </div>
              <p className="text-xs text-[#64748B]">
                Diammonium Phosphate provides concentrated phosphorus for root development during sowing and early vegetative phases.
              </p>
            </div>
            <div className="p-3.5 bg-[#F9F8F5] rounded-xl border border-[#E2E8F0]">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sm text-[#09262A]">MOP (0-0-60)</span>
                <span className="text-[0.65rem] font-mono px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-bold">Potassium Rich</span>
              </div>
              <p className="text-xs text-[#64748B]">
                Muriate of Potash provides essential potassium for grain filling, disease resistance, and fruit setting during flowering.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
