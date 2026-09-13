import { Eye } from 'lucide-react';
import type { PredictionRecord } from '../types';

interface PredictionRowProps {
  record: PredictionRecord;
  onInspect: (record: PredictionRecord) => void;
}

export default function PredictionRow({ record, onInspect }: PredictionRowProps) {
  return (
    <tr
      onClick={() => onInspect(record)}
      className="hover:bg-[#F9F8F5] transition-colors border-b border-[#E2E8F0] cursor-pointer text-xs group"
    >
      {/* Date & Time */}
      <td className="py-3.5 px-4 font-mono font-medium text-[#09262A] whitespace-nowrap">
        {record.date}
        <span className="block text-[0.65rem] text-[#64748B]">{record.capturedTime}</span>
      </td>

      {/* Soil pH */}
      <td className="py-3.5 px-4 font-mono font-semibold text-[#09262A]">
        {record.soilPh} <span className="text-[0.65rem] text-[#64748B]">pH</span>
      </td>

      {/* NPK Values */}
      <td className="py-3.5 px-4 font-mono text-[#09262A] whitespace-nowrap">
        <span className="text-emerald-700 font-bold">{record.nitrogen}</span> /{' '}
        <span className="text-amber-700 font-bold">{record.phosphorus}</span> /{' '}
        <span className="text-blue-700 font-bold">{record.potassium}</span>
        <span className="block text-[0.65rem] text-[#64748B]">N / P / K (mg/kg)</span>
      </td>

      {/* Crop Growth Stage */}
      <td className="py-3.5 px-4">
        <span className="px-2.5 py-1 rounded-full text-[0.68rem] font-medium bg-[#F1F5F9] text-[#0F172A] border border-[#E2E8F0]">
          {record.growthStage}
        </span>
      </td>

      {/* Recommendation Output */}
      <td className="py-3.5 px-4 font-bold text-[#09262A]">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
          {record.recommendation}
        </span>
      </td>

      {/* Confidence */}
      <td className="py-3.5 px-4 font-mono font-bold text-[#F59E0B]">
        {record.confidence}%
      </td>

      {/* Latency */}
      <td className="py-3.5 px-4 font-mono text-[#64748B]">
        {record.latencyMs ? `${record.latencyMs} ms` : '—'}
      </td>

      {/* Actions */}
      <td className="py-3.5 px-4 text-right">
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onInspect(record);
          }}
          className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#F9F8F5] hover:bg-[#09262A] hover:text-white text-[#09262A] font-mono text-[0.65rem] font-bold border border-[#E2E8F0] transition-colors cursor-pointer"
        >
          <Eye className="w-3 h-3" />
          <span>INSPECT</span>
        </button>
      </td>
    </tr>
  );
}
