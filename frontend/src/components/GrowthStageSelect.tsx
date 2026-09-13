import { ChevronDown } from 'lucide-react';
import type { GrowthStage } from '../types';

interface GrowthStageSelectProps {
  value: GrowthStage;
  onChange: (value: GrowthStage) => void;
}

const stageOptions: { value: GrowthStage; label: string }[] = [
  { value: 'Sowing', label: 'Sowing (S1 - S2)' },
  { value: 'Vegetative', label: 'Vegetative (V4 - V8)' },
  { value: 'Flowering', label: 'Flowering (R1 - R3)' },
  { value: 'Harvest', label: 'Harvest (H1 - H2)' },
];

export default function GrowthStageSelect({ value, onChange }: GrowthStageSelectProps) {
  return (
    <div className="flex-1 min-w-[160px]">
      <label htmlFor="growth-stage" className="block text-[0.62rem] font-mono uppercase tracking-[0.14em] text-[#102D32] font-bold mb-1.5">
        GROWTH STAGE
      </label>
      <div className="relative">
        <select
          id="growth-stage"
          value={value}
          onChange={(e) => onChange(e.target.value as GrowthStage)}
          className="w-full px-3 py-2.5 rounded-xl border border-[#DDD9CE] bg-white text-xs text-[#102D32] font-semibold appearance-none focus:outline-none focus:ring-2 focus:ring-[#4D947A]/30 focus:border-[#4D947A] transition-all duration-150 cursor-pointer pr-10 shadow-2xs"
          aria-label="Growth stage"
        >
          {stageOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#6E858B] pointer-events-none" />
      </div>
    </div>
  );
}
