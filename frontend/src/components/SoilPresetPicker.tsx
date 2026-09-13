import { Sparkles } from 'lucide-react';
import type { SoilReading, GrowthStage } from '../types';

export interface SoilPreset {
  id: string;
  name: string;
  description: string;
  reading: SoilReading;
  badgeColor: string;
}

export const SOIL_PRESETS: SoilPreset[] = [
  {
    id: 'nitrogen-depleted',
    name: 'Nitrogen Depleted',
    description: 'Low N (15 mg/kg), requires heavy nitrogen fertilizer',
    badgeColor: 'bg-amber-100 text-amber-800 border-amber-300',
    reading: {
      soilPh: 6.2,
      nitrogen: 15,
      phosphorus: 45,
      potassium: 50,
      growthStage: 'Vegetative' as GrowthStage,
    },
  },
  {
    id: 'high-potassium',
    name: 'High Potassium',
    description: 'Elevated K (85 mg/kg) with low Phosphorus',
    badgeColor: 'bg-blue-100 text-blue-800 border-blue-300',
    reading: {
      soilPh: 6.8,
      nitrogen: 55,
      phosphorus: 12,
      potassium: 85,
      growthStage: 'Flowering' as GrowthStage,
    },
  },
  {
    id: 'balanced-soil',
    name: 'Balanced Soil',
    description: 'Optimal NPK levels for standard vegetative crop growth',
    badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-300',
    reading: {
      soilPh: 6.5,
      nitrogen: 45,
      phosphorus: 35,
      potassium: 40,
      growthStage: 'Vegetative' as GrowthStage,
    },
  },
  {
    id: 'acidic-plot',
    name: 'Acidic Plot',
    description: 'Low pH (5.2) with phosphorus deficiency',
    badgeColor: 'bg-rose-100 text-rose-800 border-rose-300',
    reading: {
      soilPh: 5.2,
      nitrogen: 30,
      phosphorus: 15,
      potassium: 35,
      growthStage: 'Sowing' as GrowthStage,
    },
  },
];

interface SoilPresetPickerProps {
  onSelectPreset: (preset: SoilPreset) => void;
  activePresetId?: string;
}

export default function SoilPresetPicker({ onSelectPreset, activePresetId }: SoilPresetPickerProps) {
  return (
    <div className="mb-4">
      <div className="flex items-center gap-1.5 mb-2">
        <Sparkles className="w-3.5 h-3.5 text-[#10B981]" />
        <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#64748B] font-semibold">
          Quick Soil Presets
        </span>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {SOIL_PRESETS.map((preset) => {
          const isSelected = activePresetId === preset.id;
          return (
            <button
              key={preset.id}
              type="button"
              onClick={() => onSelectPreset(preset)}
              className={`
                px-3 py-2 rounded-xl text-left border transition-all duration-150 cursor-pointer flex flex-col justify-between
                ${isSelected
                  ? 'bg-[#09262A] text-white border-[#09262A] shadow-xs ring-2 ring-[#10B981]/40'
                  : 'bg-[#F9F8F5] text-[#0F172A] border-[#E2E8F0] hover:bg-[#F5F4EF] hover:border-[#CBD5E1]'
                }
              `}
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-xs font-bold ${isSelected ? 'text-white' : 'text-[#09262A]'}`}>
                  {preset.name}
                </span>
              </div>
              <p className={`text-[0.68rem] leading-tight line-clamp-2 ${isSelected ? 'text-[#94A3B8]' : 'text-[#64748B]'}`}>
                {preset.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
