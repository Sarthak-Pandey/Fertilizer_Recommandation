import { useState } from 'react';
import { ChevronDown, CheckCircle2 } from 'lucide-react';
import type { PredictionRecord } from '../types';

interface PredictionRowProps {
  record: PredictionRecord;
  index: number;
}

export default function PredictionRow({ record, index }: PredictionRowProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border-b border-[#DDD9CE]/50 last:border-b-0">
      {/* Main row */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center gap-4 py-3.5 px-1 hover:bg-[#F7F5EF]/50 transition-colors text-left cursor-pointer"
        aria-expanded={isExpanded}
        aria-label={`Prediction ${record.id}, expand for details`}
      >
        {/* # */}
        <div className="w-8 text-xs font-mono text-[#6E858B]">{index}</div>

        {/* Recommendation Output */}
        <div className="flex-[2] min-w-0">
          <div className="text-sm font-medium text-[#102D32]">{record.recommendation}</div>
          <div className="text-[0.65rem] font-mono text-[#6E858B] truncate">{record.id}</div>
        </div>

        {/* Confidence */}
        <div className="flex-1 hidden sm:flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#4D947A]" />
          <span className="text-sm text-[#102D32]">{record.confidence}%</span>
        </div>

        {/* Date Status */}
        <div className="flex-1 hidden sm:block">
          <div className="text-xs text-[#102D32]">{record.date}</div>
          <div className="text-[0.6rem] text-[#4D947A]">{record.status}</div>
        </div>

        {/* Latency */}
        <div className="flex-1 hidden md:block">
          <span className="text-xs font-mono text-[#6E858B]">42ms</span>
        </div>

        {/* Timestamp */}
        <div className="flex-1 text-xs text-[#6E858B] font-mono hidden md:block">
          {record.capturedTime}
        </div>

        {/* Audit */}
        <div className="w-14 hidden lg:flex items-center justify-center">
          <CheckCircle2 className="w-4 h-4 text-[#4D947A]" />
        </div>

        {/* Chevron */}
        <ChevronDown
          className={`w-4 h-4 text-[#6E858B] shrink-0 transition-transform duration-200 ${
            isExpanded ? 'rotate-180' : ''
          }`}
        />
      </button>

      {/* Expanded details */}
      <div
        className={`transition-expand ${
          isExpanded ? 'max-h-96 opacity-100 pb-4' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="bg-[#F7F5EF] rounded-xl p-4 mx-1 grid grid-cols-2 sm:grid-cols-3 gap-3">
          {[
            { label: 'Soil pH', value: record.soilPh.toString() },
            { label: 'Nitrogen', value: `${record.nitrogen} mg/kg` },
            { label: 'Phosphorus', value: `${record.phosphorus} mg/kg` },
            { label: 'Potassium', value: `${record.potassium} mg/kg` },
            { label: 'Growth stage', value: record.growthStage },
            { label: 'Recommendation', value: record.recommendation },
            { label: 'Confidence', value: `${record.confidence}%` },
            { label: 'Model version', value: record.modelVersion },
            { label: 'Audit status', value: record.auditStatus },
          ].map((item) => (
            <div key={item.label}>
              <div className="text-[0.6rem] font-mono uppercase tracking-[0.12em] text-[#6E858B] mb-0.5">
                {item.label}
              </div>
              <div className="text-xs font-medium text-[#102D32]">{item.value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
