import type { ReactNode } from 'react';

interface KpiCardProps {
  label: string;
  value: string | number;
  subtitle: string;
  icon: ReactNode;
  iconVariant: 'blue' | 'yellow' | 'pink';
}

const iconBg = {
  blue: 'bg-[#E5EFEA] text-[#163238]',
  yellow: 'bg-[#F8EDCF] text-[#b8941f]',
  pink: 'bg-[#F5E4E1] text-[#c47067]',
};

export default function KpiCard({ label, value, subtitle, icon, iconVariant }: KpiCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-5 flex items-start gap-4 hover:shadow-sm transition-shadow duration-200">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${iconBg[iconVariant]}`}>
        {icon}
      </div>
      <div className="min-w-0">
        <div className="meta-label mb-1">{label}</div>
        <div className="text-2xl font-bold text-[#102D32] tracking-tight">{value}</div>
        <div className="text-xs text-[#6E858B] mt-0.5">{subtitle}</div>
      </div>
    </div>
  );
}
