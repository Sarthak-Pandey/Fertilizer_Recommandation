import { Sprout } from 'lucide-react';
import SoilInput from './SoilInput';
import GrowthStageSelect from './GrowthStageSelect';
import type { SoilReading } from '../types';
import { defaultSoilReading } from '../data/mockData';

interface SoilReadingCardProps {
  reading: SoilReading;
  onChange: (reading: SoilReading) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

export default function SoilReadingCard({ reading, onChange, onGenerate, isLoading }: SoilReadingCardProps) {
  const handleLoadSample = () => {
    onChange({ ...defaultSoilReading });
  };

  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <span className="step-label text-[#6E858B]">Step 01 / Soil Reading</span>
        <div className="flex items-center gap-2">
          <span className="meta-label px-2.5 py-1 rounded-full border border-[#DDD9CE] bg-[#FCFBF7]">
            6 Inputs
          </span>
          <button
            onClick={handleLoadSample}
            className="meta-label px-2.5 py-1 rounded-full border border-[#4D947A]/30 bg-[#E5EFEA] text-[#4D947A] hover:bg-[#4D947A]/20 transition-colors cursor-pointer"
          >
            Load Sample
          </button>
        </div>
      </div>

      {/* Title */}
      <h3 className="text-lg font-bold text-[#102D32] mb-1">Describe the plot</h3>
      <p className="text-sm text-[#6E858B] mb-6">
        Enter the latest lab or probe values. The active model will assess nutrient balance against crop stage.
      </p>

      {/* pH & Growth Stage */}
      <div className="flex flex-col sm:flex-row gap-4 mb-4">
        <div className="flex-1">
          <label htmlFor="soil-ph" className="block text-xs font-semibold text-[#102D32] mb-1.5">
            Soil pH
          </label>
          <div className="relative">
            <input
              id="soil-ph"
              type="number"
              step="0.1"
              value={reading.soilPh}
              onChange={(e) => onChange({ ...reading, soilPh: parseFloat(e.target.value) || 0 })}
              className="w-full px-3 py-2.5 rounded-lg border border-[#DDD9CE] bg-white text-sm text-[#102D32] font-medium focus:outline-none focus:ring-2 focus:ring-[#4D947A]/30 focus:border-[#4D947A] transition-all duration-150 pr-10"
              aria-label="Soil pH value"
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[#6E858B] font-mono pointer-events-none">
              pH
            </span>
          </div>
        </div>
        <GrowthStageSelect
          value={reading.growthStage}
          onChange={(stage) => onChange({ ...reading, growthStage: stage })}
        />
      </div>

      {/* N P K */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
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

      {/* Generate button — green instead of yellow */}
      <button
        onClick={onGenerate}
        disabled={isLoading}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-[#102D32] hover:bg-[#163238] text-white text-sm font-semibold transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
        aria-label="Compute recommendation"
      >
        {isLoading ? (
          <div className="flex items-center gap-1.5">
            <div className="flex gap-1">
              <span className="loading-dot w-1.5 h-1.5 rounded-full bg-white" />
              <span className="loading-dot w-1.5 h-1.5 rounded-full bg-white" />
              <span className="loading-dot w-1.5 h-1.5 rounded-full bg-white" />
            </div>
            <span>Processing...</span>
          </div>
        ) : (
          <>
            <Sprout className="w-4 h-4" />
            Compute recommendation
          </>
        )}
      </button>
    </div>
  );
}
