interface SoilInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  unit: string;
  id: string;
}

export default function SoilInput({ label, value, onChange, unit, id }: SoilInputProps) {
  return (
    <div className="flex-1 min-w-[120px]">
      <label htmlFor={id} className="block text-xs font-medium text-[#102D32] mb-1.5">
        {label}
      </label>
      <div className="relative">
        <input
          id={id}
          type="number"
          value={value}
          onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
          className="w-full px-3 py-2.5 rounded-lg border border-[#DDD9CE] bg-white text-sm text-[#102D32] font-medium focus:outline-none focus:ring-2 focus:ring-[#4D947A]/30 focus:border-[#4D947A] transition-all duration-150"
          aria-label={`${label} in ${unit}`}
        />
        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[#6E858B] font-mono pointer-events-none">
          {unit}
        </span>
      </div>
    </div>
  );
}
