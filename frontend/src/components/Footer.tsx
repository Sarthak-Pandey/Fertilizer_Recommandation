export default function Footer() {
  return (
    <footer className="border-t border-[#DDD9CE]/50 py-4 px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
      {/* Left: system status */}
      <div className="flex items-center gap-2">
        <span className="meta-label text-[#6E858B]">System</span>
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#4D947A]" />
          <span className="text-[0.65rem] text-[#4D947A] font-medium">FastAPI active</span>
        </div>
      </div>

      {/* Center: copyright */}
      <span className="text-[0.65rem] text-[#6E858B] text-center">
        © 2024 Fieldwise Agronomy Console · Precision Nutrient Optimization
      </span>

      {/* Right: tech stack */}
      <span className="text-[0.6rem] text-[#6E858B] font-mono">
        FastAPI · PyTorch/Scikit · ISO 14001 Agronomy Standards
      </span>
    </footer>
  );
}
