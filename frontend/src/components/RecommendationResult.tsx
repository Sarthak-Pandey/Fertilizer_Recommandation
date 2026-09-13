import { Circle, Crosshair } from 'lucide-react';
import ModelTrace from './ModelTrace';
import type { RecommendationResult as RecommendationResultType, LoadingStep } from '../types';

interface RecommendationResultProps {
  result: RecommendationResultType | null;
  isLoading: boolean;
  loadingStep: LoadingStep | null;
}

const loadingMessages: Record<LoadingStep, string> = {
  analyzing: 'Analyzing soil profile...',
  evaluating: 'Evaluating nutrient balance...',
  running: 'Running recommendation model...',
  complete: 'Recommendation generated.',
};

export default function RecommendationResult({ result, isLoading, loadingStep }: RecommendationResultProps) {
  return (
    <div className="bg-[#163238] rounded-2xl p-6 text-white relative overflow-hidden result-decoration min-h-[340px] flex flex-col">
      {/* Step label */}
      <div className="mb-4">
        <span className="step-label text-[#6E858B]">Step 02 / Current Result</span>
      </div>

      {/* Loading state */}
      {isLoading && loadingStep && (
        <div className="flex-1 flex flex-col justify-center items-center text-center">
          <div className="w-12 h-12 rounded-full bg-[#20383D] flex items-center justify-center mb-4">
            <Crosshair className="w-5 h-5 text-[#4D947A] animate-spin" style={{ animationDuration: '3s' }} />
          </div>
          <div className="space-y-2">
            {Object.entries(loadingMessages).map(([step, message]) => {
              const stepOrder: LoadingStep[] = ['analyzing', 'evaluating', 'running', 'complete'];
              const currentIndex = stepOrder.indexOf(loadingStep);
              const messageIndex = stepOrder.indexOf(step as LoadingStep);
              const isVisible = messageIndex <= currentIndex;
              const isCurrent = messageIndex === currentIndex;

              if (!isVisible) return null;

              return (
                <div
                  key={step}
                  className={`text-xs font-mono animate-fade-in-up ${
                    isCurrent ? 'text-[#4D947A]' : 'text-white/50'
                  }`}
                >
                  {message}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !result && (
        <div className="flex-1 flex flex-col justify-center">
          <div className="w-10 h-10 rounded-full bg-[#F2C14E] flex items-center justify-center mb-4">
            <Circle className="w-4 h-4 text-[#102D32]" fill="#102D32" />
          </div>
          <h3 className="text-xl font-bold text-[#F2C14E] leading-tight mb-2">
            Your recommendation will land<br />here.
          </h3>
          <p className="text-sm text-[#6E858B] mb-5">
            Run the analysis on the left to classify the soil chemistry and receive
            an suitable fertilizer formulation.
          </p>

          {/* Endpoint info */}
          <div className="mb-3">
            <span className="text-[0.65rem] text-[#6E858B]">Endpoint: </span>
            <span className="text-[0.65rem] font-mono text-[#4D947A]">POST /api/v1/fertilizer/recommend</span>
          </div>

          {/* Model info */}
          <div className="flex items-center justify-between">
            <div>
              <span className="text-[0.65rem] text-[#6E858B]">Model: </span>
              <span className="text-[0.65rem] font-mono text-white/70">model-v1</span>
            </div>
            <div>
              <span className="text-[0.65rem] text-[#6E858B]">ID: </span>
              <span className="text-[0.65rem] font-mono text-[#F2C14E]/80">870a9c1a...</span>
            </div>
          </div>
        </div>
      )}

      {/* Result state */}
      {!isLoading && result && (
        <div className="flex-1 animate-fade-in-up">
          <div className="mb-4">
            <div className="meta-label text-[#6E858B]/70 mb-1">Recommended Product</div>
            <div className="text-3xl font-bold text-[#F2C14E] tracking-tight">
              {result.recommendation.product}
            </div>
          </div>

          <div className="flex gap-6 mb-4">
            <div>
              <div className="meta-label text-[#6E858B]/70 mb-0.5">Confidence</div>
              <div className="text-lg font-bold text-white">{result.recommendation.confidence}%</div>
            </div>
          </div>

          <div className="mb-4">
            <div className="meta-label text-[#6E858B]/70 mb-1">Rationale</div>
            <p className="text-xs text-white/70 leading-relaxed">
              {result.recommendation.rationale}
            </p>
          </div>

          <ModelTrace steps={result.modelTrace} />
        </div>
      )}
    </div>
  );
}
