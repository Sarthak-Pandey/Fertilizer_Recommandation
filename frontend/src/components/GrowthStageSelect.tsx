import { ChevronDown } from 'lucide-react';
import type { GrowthStage } from '../types';

interface GrowthStageSelectProps {
  value: GrowthStage;
  onChange: (value: GrowthStage) => void;
}

const stages: GrowthStage[] = ['Germination', 'Seedling', 'Vegetative', 'Reproductive', 'Maturity'];

export default function GrowthStageSelect({ value, onChange }: GrowthStageSelectProps) {
  return (
    <div className="flex-1 min-w-[160px]">
      <label htmlFor="growth-stage" className="block text-xs font-medium text-[#102D32] mb-1.5">
        Growth stage
      </label>
      <div className="relative">
        <select
          id="growth-stage"
          value={value}
          onChange={(e) => onChange(e.target.value as GrowthStage)}
          className="w-full px-3 py-2.5 rounded-lg border border-[#DDD9CE] bg-white text-sm text-[#102D32] font-medium appearance-none focus:outline-none focus:ring-2 focus:ring-[#4D947A]/30 focus:border-[#4D947A] transition-all duration-150 cursor-pointer pr-10"
          aria-label="Growth stage"
        >
          {stages.map((stage) => (
            <option key={stage} value={stage}>{stage}</option>
          ))}
        </select>
        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6E858B] pointer-events-none" />
      </div>
    </div>
  );
}
