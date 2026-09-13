import { ArrowUpRight } from 'lucide-react';
import type { DailyVolume as DailyVolumeType } from '../types';

interface DailyVolumeCardProps {
  volume: DailyVolumeType;
}

export default function DailyVolumeCard({ volume }: DailyVolumeCardProps) {
  const maxVal = Math.max(...volume.data);

  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <span className="meta-label">Usage Rhythm</span>
        <ArrowUpRight className="w-3.5 h-3.5 text-[#6E858B]" />
      </div>

      <h4 className="text-base font-bold text-[#102D32] mb-4">Daily volume</h4>

      {/* Mini chart */}
      <div className="bg-[#20383D] rounded-xl p-4 mb-3">
        <div className="flex items-end gap-1.5 h-16">
          {volume.data.map((val, i) => (
            <div
              key={i}
              className="flex-1 bg-[#4D947A]/60 rounded-sm chart-bar transition-all duration-300 hover:bg-[#4D947A]"
              style={{ height: `${(val / maxVal) * 100}%` }}
              aria-label={`Day ${i + 1}: ${val} predictions`}
            />
          ))}
        </div>
      </div>

      {/* Value */}
      <div className="text-center">
        <div className="text-2xl font-bold text-[#102D32]">{volume.value}</div>
        <p className="text-[0.65rem] text-[#6E858B] mt-0.5 leading-relaxed">{volume.description}</p>
      </div>
    </div>
  );
}
