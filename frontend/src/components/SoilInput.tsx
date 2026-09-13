interface SoilInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  unit: string;
  id: string;
}

export default function SoilInput({ label, value, onChange, unit, id }: SoilInputProps) {
  return (
    <div className="flex-1 min-w-[100px]">
      <label htmlFor={id} className="block text-[0.6rem] font-mono text-[#102D32] font-bold mb-1 truncate">
        {label}
      </label>
      <div className="relative">
        <input
          id={id}
          type="number"
          value={value}
          onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
          className="w-full px-3 py-2 rounded-xl border border-[#DDD9CE] bg-white text-xs text-[#102D32] font-semibold focus:outline-none focus:ring-2 focus:ring-[#4D947A]/30 focus:border-[#4D947A] transition-all duration-150 shadow-2xs pr-10"
          aria-label={`${label} in ${unit}`}
        />
        <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[0.6rem] text-[#6E858B] font-mono pointer-events-none">
          {unit}
        </span>
      </div>
    </div>
  );
}
