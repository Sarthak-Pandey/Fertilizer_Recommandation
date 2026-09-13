import { useState, useEffect } from 'react';
import { Activity, Server, Cpu, Database, RefreshCw, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';
import { fetchHealthStatus } from '../services/recommendationService';
import type { HealthStatus } from '../services/recommendationService';

export default function SystemHealthBar() {
  const [health, setHealth] = useState<HealthStatus>({
    backend: 'healthy',
    mlService: 'healthy',
    modelVersion: 'model-v1',
  });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadHealth = async () => {
    setIsRefreshing(true);
    try {
      const status = await fetchHealthStatus();
      setHealth(status);
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadHealth();
    const timer = setInterval(loadHealth, 30_000);
    return () => clearInterval(timer);
  }, []);

  const getStatusBadge = (status: 'healthy' | 'degraded' | 'offline') => {
    if (status === 'healthy') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[0.68rem] font-mono font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
          <CheckCircle2 className="w-3 h-3 text-[#10B981]" />
          ● Operational
        </span>
      );
    }
    if (status === 'degraded') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[0.68rem] font-mono font-bold bg-amber-50 text-amber-800 border border-amber-200">
          <AlertTriangle className="w-3 h-3 text-[#F59E0B]" />
          ● Degraded
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[0.68rem] font-mono font-bold bg-rose-50 text-rose-800 border border-rose-200">
        <XCircle className="w-3 h-3 text-rose-600" />
        ● Offline (Mock Active)
      </span>
    );
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-2xs">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-[#10B981]" />
          <h3 className="text-base font-extrabold text-[#09262A]">System Infrastructure Telemetry</h3>
        </div>

        <button
          type="button"
          onClick={loadHealth}
          disabled={isRefreshing}
          className="flex items-center gap-1.5 text-[0.68rem] font-mono px-3 py-1 rounded-full border border-[#E2E8F0] bg-[#F9F8F5] text-[#64748B] font-bold hover:bg-[#E2E8F0] transition-colors cursor-pointer"
        >
          <RefreshCw className={`w-3 h-3 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>Ping Health</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Server className="w-5 h-5 text-[#09262A]" />
            <div>
              <span className="text-xs font-bold text-[#09262A] block">FastAPI Gateway</span>
              <span className="text-[0.65rem] font-mono text-[#64748B]">Port :8000</span>
            </div>
          </div>
          {getStatusBadge(health.backend)}
        </div>

        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Cpu className="w-5 h-5 text-[#10B981]" />
            <div>
              <span className="text-xs font-bold text-[#09262A] block">ML Inference Engine</span>
              <span className="text-[0.65rem] font-mono text-[#64748B]">{health.modelVersion} (:8001)</span>
            </div>
          </div>
          {getStatusBadge(health.mlService)}
        </div>

        <div className="bg-[#F9F8F5] p-4 rounded-xl border border-[#E2E8F0] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="w-5 h-5 text-[#3B82F6]" />
            <div>
              <span className="text-xs font-bold text-[#09262A] block">SQLite Database</span>
              <span className="text-[0.65rem] font-mono text-[#64748B]">predictions.db</span>
            </div>
          </div>
          {getStatusBadge(health.backend === 'healthy' ? 'healthy' : 'offline')}
        </div>
      </div>
    </div>
  );
}
