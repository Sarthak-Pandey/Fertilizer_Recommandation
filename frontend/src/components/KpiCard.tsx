import type { ReactNode } from 'react';

interface KpiCardProps {
  label: string;
  value: string | number;
  subtitle: string;
  icon: ReactNode;
  iconVariant?: 'emerald' | 'amber' | 'blue' | 'teal';
  trend?: string;
}

export default function KpiCard({
  label,
  value,
  subtitle,
  icon,
  iconVariant = 'emerald',
  trend,
}: KpiCardProps) {
  const variantStyles = {
    emerald: 'bg-emerald-50 text-[#10B981] border-emerald-200',
    amber: 'bg-amber-50 text-[#F59E0B] border-amber-200',
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    teal: 'bg-[#09262A] text-[#10B981] border-[#0E383C]',
  };

  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-2xs hover:border-[#CBD5E1] transition-all duration-150 flex flex-col justify-between">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[0.65rem] font-mono uppercase tracking-widest text-[#64748B] font-bold">
          {label}
        </span>
        <div className={`w-9 h-9 rounded-xl border flex items-center justify-center shadow-2xs ${variantStyles[iconVariant]}`}>
          {icon}
        </div>
      </div>

      <div>
        <div className="text-2xl font-extrabold text-[#09262A] tracking-tight mb-0.5 font-mono">
          {value}
        </div>
        <div className="flex items-center justify-between text-xs text-[#64748B]">
          <span>{subtitle}</span>
          {trend && (
            <span className="text-[0.65rem] font-mono text-[#10B981] font-semibold bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
              {trend}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
