import { Cpu } from 'lucide-react';

interface ModelIntelligenceCardProps {
  modelVersion?: string;
  gatewayStatus?: string;
}

export default function ModelIntelligenceCard({
  modelVersion = 'model-v1',
}: ModelIntelligenceCardProps) {
  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 shadow-2xs">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#09262A] flex items-center justify-center text-[#10B981]">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-extrabold text-[#09262A] tracking-tight">Model Intelligence & Architecture</h3>
            <p className="text-xs text-[#64748B]">Hierarchical Machine Learning Ensemble Engine</p>
          </div>
        </div>
        <span className="text-[0.65rem] font-mono font-bold uppercase px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
          Active Engine
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0]">
          <span className="text-[0.65rem] font-mono uppercase text-[#64748B] block font-semibold mb-1">
            CLASSIFIER ALGORITHMS
          </span>
          <div className="text-sm font-bold text-[#09262A]">XGBoost + Random Forest</div>
          <span className="text-[0.65rem] text-[#64748B] block mt-1">Hierarchical multi-class ensemble</span>
        </div>

        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0]">
          <span className="text-[0.65rem] font-mono uppercase text-[#64748B] block font-semibold mb-1">
            ACTIVE MODEL VERSION
          </span>
          <div className="text-sm font-mono font-bold text-[#10B981]">{modelVersion}</div>
          <span className="text-[0.65rem] text-[#64748B] block mt-1">Production trained pipeline</span>
        </div>

        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0]">
          <span className="text-[0.65rem] font-mono uppercase text-[#64748B] block font-semibold mb-1">
            AVG INFERENCE LATENCY
          </span>
          <div className="text-sm font-mono font-bold text-[#F59E0B]">~12.4 ms</div>
          <span className="text-[0.65rem] text-[#64748B] block mt-1">Sub-20ms P99 target</span>
        </div>
      </div>

      {/* Feature Schema Table */}
      <div className="border-t border-[#E2E8F0] pt-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-mono uppercase tracking-wider text-[#09262A] font-bold">
            Input Feature Schema Parameters
          </span>
          <span className="text-[0.65rem] font-mono text-[#64748B]">v1.0.0 schema contract</span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
          <div className="bg-[#F1F5F9] p-2.5 rounded-lg border border-[#E2E8F0]">
            <span className="font-mono font-bold text-[#09262A] block">Soil_pH</span>
            <span className="text-[0.65rem] text-[#64748B]">Float (0.0 - 14.0)</span>
          </div>
          <div className="bg-[#F1F5F9] p-2.5 rounded-lg border border-[#E2E8F0]">
            <span className="font-mono font-bold text-[#09262A] block">Nitrogen_Level</span>
            <span className="text-[0.65rem] text-[#64748B]">Float (mg/kg)</span>
          </div>
          <div className="bg-[#F1F5F9] p-2.5 rounded-lg border border-[#E2E8F0]">
            <span className="font-mono font-bold text-[#09262A] block">Phosphorus_Level</span>
            <span className="text-[0.65rem] text-[#64748B]">Float (mg/kg)</span>
          </div>
          <div className="bg-[#F1F5F9] p-2.5 rounded-lg border border-[#E2E8F0]">
            <span className="font-mono font-bold text-[#09262A] block">Potassium_Level</span>
            <span className="text-[0.65rem] text-[#64748B]">Float (mg/kg)</span>
          </div>
          <div className="bg-[#F1F5F9] p-2.5 rounded-lg border border-[#E2E8F0]">
            <span className="font-mono font-bold text-[#09262A] block">Growth_Stage</span>
            <span className="text-[0.65rem] text-[#64748B]">Categorical Enum</span>
          </div>
        </div>
      </div>
    </div>
  );
}
