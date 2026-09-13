export default function Footer() {
  return (
    <footer className="border-t border-[#DDD9CE]/60 py-5 px-6 lg:px-8 bg-[#F7F6F1] text-xs text-[#6E858B] flex flex-col sm:flex-row items-center justify-between gap-3">
      <div className="flex items-center gap-2 font-mono text-[0.68rem]">
        <span>System:</span>
        <span className="flex items-center gap-1.5 text-[#4D947A] font-bold">
          <span className="w-1.5 h-1.5 rounded-full bg-[#4D947A] animate-pulse" />
          FastAPI active
        </span>
      </div>

      <div className="text-center text-[0.68rem] font-medium">
        © 2026 Fieldwise Agronomy Console · Precision Nutrient Optimization
      </div>

      <div className="font-mono text-[0.65rem] text-[#6E858B] flex items-center gap-2">
        <span>FastAPI</span>
        <span>·</span>
        <span>PyTorch/XGBoost</span>
        <span>·</span>
        <span>ISO 14001 Standards</span>
      </div>
    </footer>
  );
}
