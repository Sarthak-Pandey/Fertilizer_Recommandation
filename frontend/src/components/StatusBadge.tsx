import type { ReactNode } from 'react';

interface StatusBadgeProps {
  variant: 'success' | 'warning' | 'info' | 'neutral';
  children: ReactNode;
  dot?: boolean;
}

const variantStyles = {
  success: 'bg-[#E5EFEA] text-[#4D947A]',
  warning: 'bg-[#F8EDCF] text-[#b8941f]',
  info: 'bg-[#E5EFEA] text-[#4D947A]',
  neutral: 'bg-[#F7F5EF] text-[#6E858B] border border-[#DDD9CE]',
};

const dotColors = {
  success: 'bg-[#4D947A]',
  warning: 'bg-[#F2C14E]',
  info: 'bg-[#4D947A]',
  neutral: 'bg-[#6E858B]',
};

export default function StatusBadge({ variant, children, dot = false }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${variantStyles[variant]}`}
    >
      {dot && (
        <span className={`w-1.5 h-1.5 rounded-full ${dotColors[variant]}`} />
      )}
      {children}
    </span>
  );
}
