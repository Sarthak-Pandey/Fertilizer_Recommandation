import { RefreshCw, PenLine, Menu } from 'lucide-react';

interface TopHeaderProps {
  onNewReading: () => void;
  onRefresh: () => void;
  onMenuToggle: () => void;
}

export default function TopHeader({ onNewReading, onRefresh, onMenuToggle }: TopHeaderProps) {
  return (
    <header className="h-[90px] bg-white/80 backdrop-blur-sm border-b border-[#DDD9CE] flex items-center px-6 lg:px-8 gap-4">
      {/* Mobile hamburger */}
      <button
        onClick={onMenuToggle}
        className="lg:hidden p-2 rounded-lg hover:bg-[#F7F5EF] text-[#6E858B] transition-colors cursor-pointer"
        aria-label="Open menu"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Left side */}
      <div className="flex-1 min-w-0">
        <div className="meta-label mb-1">Recommendation Workspace / 01</div>
        <h1 className="text-xl font-bold text-[#102D32] tracking-tight">Fertilizer intelligence</h1>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Live indicator */}
        <div className="hidden sm:flex items-center gap-1.5 text-xs text-[#6E858B]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#4D947A]" />
          Live service connection
        </div>

        {/* New reading button */}
        <button
          onClick={() => {
            onRefresh();
            onNewReading();
          }}
          className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg border border-[#DDD9CE] bg-white hover:bg-[#F7F5EF] text-sm text-[#102D32] font-medium transition-all duration-150 cursor-pointer"
          aria-label="Start new reading"
        >
          <PenLine className="w-3.5 h-3.5" />
          New reading
        </button>

        {/* Refresh (mobile) */}
        <button
          onClick={onRefresh}
          className="sm:hidden p-2 rounded-lg border border-[#DDD9CE] bg-white hover:bg-[#F7F5EF] transition-colors cursor-pointer"
          aria-label="Refresh"
        >
          <RefreshCw className="w-4 h-4 text-[#6E858B]" />
        </button>

        {/* Avatar */}
        <div className="w-9 h-9 rounded-full bg-[#102D32] flex items-center justify-center text-xs font-bold text-white tracking-wide">
          AO
        </div>
      </div>
    </header>
  );
}
