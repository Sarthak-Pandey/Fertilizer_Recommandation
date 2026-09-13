import { useState } from 'react';
import { Sprout, RotateCcw } from 'lucide-react';
import SoilInput from './SoilInput';
import GrowthStageSelect from './GrowthStageSelect';
import SoilPresetPicker from './SoilPresetPicker';
import type { SoilPreset } from './SoilPresetPicker';
import type { SoilReading } from '../types';
import { defaultSoilReading } from '../data/mockData';

interface SoilReadingCardProps {
  reading: SoilReading;
  onChange: (reading: SoilReading) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

export default function SoilReadingCard({ reading, onChange, onGenerate, isLoading }: SoilReadingCardProps) {
  const [selectedPresetId, setSelectedPresetId] = useState<string | undefined>();

  const handleLoadSample = () => {
    onChange({ ...defaultSoilReading });
    setSelectedPresetId(undefined);
  };

  const handleSelectPreset = (preset: SoilPreset) => {
    onChange({ ...preset.reading });
    setSelectedPresetId(preset.id);
  };

  const getPhStatus = (ph: number) => {
    if (ph < 6.0) return { label: 'Acidic', color: 'text-amber-600 bg-amber-50 border-amber-200' };
    if (ph > 7.5) return { label: 'Alkaline', color: 'text-[#3B82F6] bg-blue-50 border-blue-200' };
    return { label: 'Optimal', color: 'text-emerald-700 bg-emerald-50 border-emerald-200' };
  };

  const phStatus = getPhStatus(reading.soilPh);

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 flex flex-col justify-between shadow-2xs">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse" />
            <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#10B981] font-bold">
              SOIL INTELLIGENCE WORKSPACE
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleLoadSample}
              className="flex items-center gap-1.5 text-[0.65rem] font-mono px-3 py-1 rounded-full border border-[#E2E8F0] bg-[#F9F8F5] text-[#64748B] font-bold hover:bg-[#E2E8F0] hover:text-[#0F172A] transition-colors cursor-pointer"
            >
              <RotateCcw className="w-3 h-3" />
              <span>RESET DEFAULTS</span>
            </button>
          </div>
        </div>

        <h3 className="text-xl font-extrabold text-[#09262A] tracking-tight mb-1">Field Plot Composition</h3>
        <p className="text-xs text-[#64748B] mb-5 font-medium leading-relaxed">
          Provide lab probe measurements or select a preset profile to compute precision nutrient recommendations.
        </p>

        <SoilPresetPicker onSelectPreset={handleSelectPreset} activePresetId={selectedPresetId} />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5 pt-3 border-t border-[#E2E8F0]">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label htmlFor="soil-ph" className="block text-[0.65rem] font-mono uppercase tracking-wider text-[#09262A] font-bold">
                SOIL pH SCALE (0 – 14)
              </label>
              <span className={`text-[0.6rem] font-mono px-2 py-0.5 rounded-full border font-bold uppercase ${phStatus.color}`}>
                {phStatus.label}
              </span>
            </div>
            <div className="relative flex items-center gap-3">
              <input
                id="soil-ph"
                type="number"
                step="0.1"
                min="0"
                max="14"
                value={reading.soilPh}
                onChange={(e) => onChange({ ...reading, soilPh: parseFloat(e.target.value) || 0 })}
                className="w-24 px-3 py-2 rounded-xl border border-[#CBD5E1] bg-white text-xs text-[#09262A] font-mono font-bold focus:outline-none focus:ring-2 focus:ring-[#10B981]/30 focus:border-[#10B981] transition-all shadow-2xs"
                aria-label="Soil pH value"
              />
              <div className="flex-1">
                <input
                  type="range"
                  min="3.5"
                  max="9.0"
                  step="0.1"
                  value={reading.soilPh}
                  onChange={(e) => onChange({ ...reading, soilPh: parseFloat(e.target.value) || 0 })}
                  className="w-full h-2 bg-[#E2E8F0] rounded-lg appearance-none cursor-pointer accent-[#10B981]"
                />
                <div className="flex justify-between text-[0.58rem] font-mono text-[#94A3B8] mt-1">
                  <span>Acidic (3.5)</span>
                  <span>6.5</span>
                  <span>Alkaline (9.0)</span>
                </div>
              </div>
            </div>
          </div>

          <GrowthStageSelect
            value={reading.growthStage}
            onChange={(stage) => onChange({ ...reading, growthStage: stage })}
          />
        </div>

        <div className="flex items-center justify-between mb-3 pt-3 border-t border-[#E2E8F0]">
          <span className="text-[0.65rem] font-mono uppercase tracking-wider text-[#09262A] font-bold">
            NUTRIENT PROBE COMPOSITION
          </span>
          <span className="text-[0.65rem] font-mono text-[#64748B]">
            Unit: mg/kg dry soil
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
          <SoilInput
            id="nitrogen"
            label="Nitrogen (N)"
            value={reading.nitrogen}
            onChange={(v) => onChange({ ...reading, nitrogen: v })}
            unit="mg/kg"
          />
          <SoilInput
            id="phosphorus"
            label="Phosphorus (P)"
            value={reading.phosphorus}
            onChange={(v) => onChange({ ...reading, phosphorus: v })}
            unit="mg/kg"
          />
          <SoilInput
            id="potassium"
            label="Potassium (K)"
            value={reading.potassium}
            onChange={(v) => onChange({ ...reading, potassium: v })}
            unit="mg/kg"
          />
        </div>
      </div>

      <button
        type="button"
        onClick={onGenerate}
        disabled={isLoading}
        className="w-full flex items-center justify-center gap-2.5 px-5 py-3.5 rounded-xl bg-[#09262A] hover:bg-[#0E383C] text-white text-xs font-bold tracking-wide transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer shadow-md"
        aria-label="Run AI Inference"
      >
        {isLoading ? (
          <div className="flex items-center gap-2">
            <div className="flex gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#10B981] animate-ping" />
              <span className="w-2 h-2 rounded-full bg-[#F59E0B] animate-ping" />
              <span className="w-2 h-2 rounded-full bg-white animate-ping" />
            </div>
            <span className="font-mono text-xs text-white">Running Model Inference Pipeline...</span>
          </div>
        ) : (
          <>
            <Sprout className="w-4 h-4 text-[#10B981]" strokeWidth={2.5} />
            <span className="font-semibold text-sm">RUN AI INFERENCE</span>
          </>
        )}
      </button>
    </div>
  );
}
