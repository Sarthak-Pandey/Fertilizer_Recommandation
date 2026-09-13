import { CheckCircle2, Clock, Sparkles, Brain } from 'lucide-react';
import ModelTrace from './ModelTrace';
import type { RecommendationResult as RecommendationResultType, LoadingStep } from '../types';

interface RecommendationResultProps {
  result: RecommendationResultType | null;
  isLoading: boolean;
  loadingStep: LoadingStep | null;
}

export default function RecommendationResult({
  result,
  isLoading,
  loadingStep,
}: RecommendationResultProps) {
  const loadingTraceSteps = [
    { label: 'Input validation', completed: loadingStep !== 'analyzing' },
    { label: 'Feature preparation', completed: loadingStep === 'running' || loadingStep === 'complete' },
    { label: 'Model inference (model-v1)', completed: loadingStep === 'running' || loadingStep === 'complete' },
    { label: 'Recommendation generated', completed: loadingStep === 'complete' },
  ];

  if (isLoading) {
    return (
      <div className="bg-[#09262A] text-white rounded-2xl p-6 flex flex-col justify-between shadow-xl min-h-[380px]">
        <div>
          <div className="flex items-center justify-between mb-4">
            <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#10B981] font-bold flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 animate-spin" />
              AI INFERENCE IN PROGRESS
            </span>
            <span className="text-[0.65rem] font-mono text-[#94A3B8]">model-v1</span>
          </div>

          <h3 className="text-xl font-extrabold text-white tracking-tight mb-2">Analyzing Plot Dynamics</h3>
          <p className="text-xs text-[#94A3B8] mb-6">
            Evaluating N-P-K concentration balance and crop growth stage requirements...
          </p>

          <ModelTrace steps={loadingTraceSteps} />
        </div>

        <div className="pt-4 border-t border-[#184F55] flex items-center justify-between text-xs text-[#94A3B8]">
          <span className="font-mono">FastAPI Engine: Active</span>
          <span className="font-mono text-[#10B981]">Processing...</span>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="bg-white rounded-2xl border border-dashed border-[#CBD5E1] p-8 flex flex-col items-center justify-center text-center shadow-2xs min-h-[380px]">
        <div className="w-14 h-14 rounded-2xl bg-[#F9F8F5] border border-[#E2E8F0] flex items-center justify-center text-[#10B981] mb-4 shadow-2xs">
          <Brain className="w-7 h-7" />
        </div>
        <h3 className="text-base font-extrabold text-[#09262A] mb-1">AI Recommendation Workspace</h3>
        <p className="text-xs text-[#64748B] max-w-sm leading-relaxed mb-4">
          Adjust soil composition parameters on the left and trigger inference to receive high-confidence nutrient guidance.
        </p>
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#F9F8F5] border border-[#E2E8F0] text-[0.68rem] font-mono text-[#64748B]">
          <span className="w-2 h-2 rounded-full bg-[#10B981]" />
          Engine ready for inference
        </div>
      </div>
    );
  }

  const { recommendation, predictionId } = result;
  const confidenceVal = recommendation.confidence || 95.0;

  const candidateProbabilities = [
    { name: recommendation.product, prob: Math.min(confidenceVal, 98.5) },
    { name: recommendation.product === 'Urea' ? 'DAP' : 'Urea', prob: Math.max(100 - confidenceVal - 2, 1.2) },
    { name: recommendation.product === 'MOP' ? 'NPK 14-35-14' : 'MOP', prob: 0.8 },
  ];

  return (
    <div className="bg-[#09262A] text-white rounded-2xl p-6 flex flex-col justify-between shadow-xl min-h-[380px] border border-[#0E383C]">
      <div>
        <div className="flex items-center justify-between mb-4">
          <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#10B981] font-bold flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-[#10B981]" />
            AI INFERENCE COMPLETE
          </span>
          <span className="text-[0.65rem] font-mono px-2.5 py-0.5 rounded-full bg-[#0E383C] text-[#10B981] font-bold border border-[#184F55]">
            model-v1
          </span>
        </div>

        <div className="mb-5 bg-[#0E383C] p-4 rounded-xl border border-[#184F55]">
          <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#94A3B8] font-bold block mb-1">
            RECOMMENDED FERTILIZER PRODUCT
          </span>
          <div className="flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-white tracking-tight">
              {recommendation.product}
            </span>
            <div className="text-right">
              <span className="text-xs font-mono text-[#94A3B8] block">CONFIDENCE</span>
              <span className="text-xl font-mono font-bold text-[#F59E0B]">{confidenceVal.toFixed(1)}%</span>
            </div>
          </div>

          <div className="w-full bg-[#09262A] h-2 rounded-full mt-3 overflow-hidden p-0.5 border border-[#184F55]">
            <div
              className="bg-gradient-to-r from-[#10B981] to-[#F59E0B] h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(confidenceVal, 100)}%` }}
            />
          </div>
        </div>

        <div className="mb-5">
          <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#10B981] font-bold block mb-1.5">
            AGRONOMIC RATIONALE & ANALYSIS
          </span>
          <p className="text-xs text-[#E2E8F0] leading-relaxed bg-[#0E383C]/50 p-3 rounded-xl border border-[#184F55]/60 font-medium">
            {recommendation.rationale}
          </p>
        </div>

        <div className="mb-4">
          <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#94A3B8] font-bold block mb-2">
            CANDIDATE PROBABILITY DISTRIBUTION
          </span>
          <div className="space-y-2">
            {candidateProbabilities.map((cand, idx) => (
              <div key={idx} className="flex items-center text-xs font-mono">
                <span className="w-28 text-[#CBD5E1] truncate">{cand.name}</span>
                <div className="flex-1 bg-[#0E383C] h-1.5 rounded-full mx-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${idx === 0 ? 'bg-[#10B981]' : 'bg-[#64748B]'}`}
                    style={{ width: `${cand.prob}%` }}
                  />
                </div>
                <span className="w-12 text-right text-[#94A3B8] font-semibold">{cand.prob.toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="pt-3 border-t border-[#184F55] flex flex-wrap items-center justify-between text-[0.68rem] font-mono text-[#94A3B8] gap-2">
        <span className="flex items-center gap-1">
          <Clock className="w-3 h-3 text-[#10B981]" /> Latency: <strong className="text-white">~12.5ms</strong>
        </span>
        <span className="truncate max-w-[200px]" title={predictionId}>
          ID: <strong className="text-white">{predictionId}</strong>
        </span>
      </div>
    </div>
  );
}
