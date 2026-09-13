import { X, Cpu, Calendar, Clock, Database, Layers } from 'lucide-react';
import type { PredictionRecord } from '../types';

interface PredictionDetailModalProps {
  record: PredictionRecord | null;
  onClose: () => void;
}

export default function PredictionDetailModal({ record, onClose }: PredictionDetailModalProps) {
  if (!record) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
      <div className="bg-white border border-[#E2E8F0] rounded-2xl max-w-xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-[#64748B] hover:text-[#0F172A] p-1.5 rounded-lg hover:bg-[#F1F5F9] transition-colors cursor-pointer"
          aria-label="Close detail modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5 border-b border-[#E2E8F0] pb-4">
          <div className="w-10 h-10 rounded-xl bg-[#09262A] flex items-center justify-center text-[#10B981] font-mono font-bold text-sm">
            AI
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-extrabold text-[#09262A]">Prediction Detail Audit</h3>
              <span className={`text-[0.65rem] font-mono px-2 py-0.5 rounded-full font-bold uppercase ${
                record.status === 'success' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
              }`}>
                {record.status}
              </span>
            </div>
            <p className="text-xs text-[#64748B] font-mono">
              Prediction ID: <span className="text-[#09262A] font-semibold">{record.id}</span>
            </p>
          </div>
        </div>

        {/* Highlight Result Card */}
        <div className="bg-[#09262A] text-white p-4 rounded-xl mb-5 flex items-center justify-between shadow-xs">
          <div>
            <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#10B981] font-bold">
              RECOMMENDED FERTILIZER
            </span>
            <div className="text-2xl font-extrabold text-white tracking-tight mt-0.5">
              {record.recommendation}
            </div>
          </div>
          <div className="text-right">
            <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#94A3B8]">
              CONFIDENCE
            </span>
            <div className="text-2xl font-mono font-bold text-[#F59E0B]">
              {record.confidence}%
            </div>
          </div>
        </div>

        {/* Input Parameters Grid */}
        <div className="mb-5">
          <h4 className="text-xs font-mono uppercase tracking-wider text-[#64748B] font-bold mb-2.5">
            Soil Composition Parameters
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0]">
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Soil pH</span>
              <span className="text-sm font-mono font-bold text-[#09262A]">{record.soilPh} pH</span>
            </div>
            <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0]">
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Nitrogen (N)</span>
              <span className="text-sm font-mono font-bold text-[#09262A]">{record.nitrogen} mg/kg</span>
            </div>
            <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0]">
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Phosphorus (P)</span>
              <span className="text-sm font-mono font-bold text-[#09262A]">{record.phosphorus} mg/kg</span>
            </div>
            <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0]">
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Potassium (K)</span>
              <span className="text-sm font-mono font-bold text-[#09262A]">{record.potassium} mg/kg</span>
            </div>
          </div>
        </div>

        {/* Crop & Growth Metadata */}
        <div className="mb-5 grid grid-cols-2 gap-3">
          <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0] flex items-center gap-3">
            <Layers className="w-5 h-5 text-[#10B981]" />
            <div>
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Growth Stage</span>
              <span className="text-xs font-bold text-[#09262A]">{record.growthStage}</span>
            </div>
          </div>
          <div className="bg-[#F9F8F5] p-3 rounded-xl border border-[#E2E8F0] flex items-center gap-3">
            <Cpu className="w-5 h-5 text-[#3B82F6]" />
            <div>
              <span className="text-[0.65rem] font-mono text-[#64748B] block">Model Version</span>
              <span className="text-xs font-mono font-bold text-[#09262A]">{record.modelVersion}</span>
            </div>
          </div>
        </div>

        {/* Audit Metadata */}
        <div className="border-t border-[#E2E8F0] pt-4 space-y-2 text-xs text-[#64748B]">
          <div className="flex items-center justify-between font-mono">
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5" /> Date Logged:
            </span>
            <span className="font-semibold text-[#0F172A]">{record.date} at {record.capturedTime}</span>
          </div>
          {record.latencyMs !== undefined && (
            <div className="flex items-center justify-between font-mono">
              <span className="flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5" /> Inference Latency:
              </span>
              <span className="font-semibold text-[#10B981]">{record.latencyMs} ms</span>
            </div>
          )}
          <div className="flex items-center justify-between font-mono">
            <span className="flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5" /> Audit Verification:
            </span>
            <span className="font-semibold text-[#0F172A]">{record.auditStatus}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
