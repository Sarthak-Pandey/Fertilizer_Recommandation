import { Check } from 'lucide-react';
import type { ModelTraceStep } from '../types';

interface ModelTraceProps {
  steps: ModelTraceStep[];
}

export default function ModelTrace({ steps }: ModelTraceProps) {
  return (
    <div className="mt-4">
      <div className="meta-label mb-2 text-[#6E858B]/70">Model Trace</div>
      <div className="space-y-1.5">
        {steps.map((step, i) => (
          <div
            key={step.label}
            className="flex items-center gap-2 text-xs animate-fade-in-up"
            style={{ animationDelay: `${i * 150}ms` }}
          >
            {step.completed ? (
              <span className="w-4 h-4 rounded-full bg-[#4D947A] flex items-center justify-center animate-check-in" style={{ animationDelay: `${i * 150}ms` }}>
                <Check className="w-2.5 h-2.5 text-white" strokeWidth={3} />
              </span>
            ) : (
              <span className="w-4 h-4 rounded-full border border-white/20" />
            )}
            <span className="text-white/80">{step.label}</span>
            {step.completed && (
              <span className="text-[#4D947A] font-mono text-[0.65rem]">✓</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
