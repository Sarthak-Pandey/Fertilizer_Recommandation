import { Menu, RefreshCw, PlusCircle, Search } from 'lucide-react';

interface TopHeaderProps {
  onNewReading: () => void;
  onRefresh: () => void;
  onMenuToggle: () => void;
}

export default function TopHeader({ onNewReading, onRefresh, onMenuToggle }: TopHeaderProps) {
  return (
    <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-[#E2E8F0] px-4 lg:px-8 py-3 flex items-center justify-between shadow-2xs">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="p-2 rounded-xl text-[#09262A] hover:bg-[#F9F8F5] lg:hidden cursor-pointer"
          aria-label="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#F9F8F5] border border-[#E2E8F0] text-xs text-[#64748B] w-64 focus-within:border-[#10B981] transition-all">
          <Search className="w-3.5 h-3.5 text-[#94A3B8]" />
          <input
            type="text"
            placeholder="Search predictions, crops, models..."
            className="bg-transparent focus:outline-none w-full text-xs text-[#09262A] placeholder-[#94A3B8]"
          />
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[0.68rem] font-mono text-emerald-800 font-semibold">
          <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse" />
          <span>Gateway: Operational</span>
        </div>

        <button
          onClick={onRefresh}
          className="flex items-center gap-1.5 px-3 py-2 rounded-xl border border-[#E2E8F0] bg-white text-[#09262A] text-xs font-semibold hover:bg-[#F9F8F5] transition-colors cursor-pointer shadow-2xs"
          title="Refresh Data"
        >
          <RefreshCw className="w-3.5 h-3.5 text-[#64748B]" />
          <span className="hidden sm:inline">Refresh</span>
        </button>

        <button
          onClick={onNewReading}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#09262A] hover:bg-[#0E383C] text-white text-xs font-bold transition-all cursor-pointer shadow-xs"
        >
          <PlusCircle className="w-4 h-4 text-[#10B981]" />
          <span>New Soil Test</span>
        </button>
      </div>
    </header>
  );
}
