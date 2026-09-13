import { Clock } from 'lucide-react';
import StatusBadge from './StatusBadge';
import type { ServiceStatus } from '../types';

interface ServicePulseProps {
  services: ServiceStatus[];
}

const statusColors = {
  healthy: 'bg-[#4D947A]',
  degraded: 'bg-[#F2C14E]',
  offline: 'bg-red-400',
};

export default function ServicePulse({ services }: ServicePulseProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <span className="meta-label">System Health</span>
        <StatusBadge variant="success" dot>Operational</StatusBadge>
      </div>

      <h4 className="text-base font-bold text-[#102D32] mb-4">Service pulse</h4>

      {/* Services */}
      <div className="space-y-3">
        {services.map((service) => (
          <div key={service.name} className="flex items-center gap-3">
            <span className={`w-2 h-2 rounded-full ${statusColors[service.status]}`} />
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium text-[#102D32]">{service.name}</div>
              <div className="text-[0.65rem] text-[#4D947A]">{service.status}</div>
            </div>
            <span className="text-[0.6rem] font-mono text-[#6E858B] uppercase tracking-wider">
              {service.type}
            </span>
          </div>
        ))}
      </div>

      {/* Last checked */}
      <div className="mt-4 pt-3 border-t border-[#DDD9CE]/30 flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-[0.65rem] text-[#6E858B]">
          <Clock className="w-3 h-3" />
          Last checked just now
        </div>
        <span className="text-[0.6rem] font-mono px-2 py-0.5 rounded-full bg-[#F7F5EF] text-[#6E858B] border border-[#DDD9CE]/50">
          auto
        </span>
      </div>
    </div>
  );
}
