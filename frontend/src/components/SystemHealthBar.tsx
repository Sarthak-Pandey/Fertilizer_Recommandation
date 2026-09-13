import { Server, Activity, Cpu, Clock } from 'lucide-react';

export default function SystemHealthBar() {
  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-5">
      {/* Header row */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-[#E5EFEA] flex items-center justify-center">
            <Server className="w-4 h-4 text-[#102D32]" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-[#102D32]">System Service Health & Pipeline Metrics</h4>
            <div className="text-[0.6rem] font-mono text-[#6E858B]">
              Endpoint: <span className="text-[#4D947A]">GET /api/v1/health</span>
            </div>
          </div>
        </div>
      </div>

      {/* Status row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Backend Server */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#4D947A]" />
            <Activity className="w-3.5 h-3.5 text-[#4D947A]" />
          </div>
          <div>
            <div className="text-xs font-medium text-[#102D32]">Backend Server</div>
            <div className="flex items-center gap-1">
              <span className="w-1 h-1 rounded-full bg-[#4D947A]" />
              <span className="text-[0.6rem] text-[#4D947A] font-medium">healthy</span>
            </div>
          </div>
        </div>

        {/* ML Prediction */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#4D947A]" />
            <Cpu className="w-3.5 h-3.5 text-[#4D947A]" />
          </div>
          <div>
            <div className="text-xs font-medium text-[#102D32]">ML Prediction</div>
            <div className="flex items-center gap-1">
              <span className="w-1 h-1 rounded-full bg-[#4D947A]" />
              <span className="text-[0.6rem] text-[#4D947A] font-medium">healthy</span>
            </div>
          </div>
        </div>

        {/* Active Model */}
        <div>
          <div className="text-[0.6rem] font-mono uppercase tracking-[0.1em] text-[#6E858B] mb-0.5">Active Model</div>
          <div className="text-xs font-mono font-semibold text-[#102D32]">model-v1</div>
        </div>

        {/* Last Check */}
        <div className="flex items-center gap-2">
          <Clock className="w-3.5 h-3.5 text-[#6E858B]" />
          <div>
            <div className="text-[0.6rem] font-mono uppercase tracking-[0.1em] text-[#6E858B] mb-0.5">Last Check</div>
            <div className="text-xs font-mono font-semibold text-[#102D32]">
              {new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
