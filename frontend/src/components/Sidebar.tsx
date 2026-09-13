import {
  Leaf,
  LayoutDashboard,
  Sprout,
  Sparkles,
  History,
  Cpu,
  Activity,
  Radio,
} from 'lucide-react';
import type { NavigationItem } from '../types';

interface SidebarProps {
  activeNav: NavigationItem;
  onNavChange: (item: NavigationItem) => void;
  isOpen: boolean;
  onClose: () => void;
}

const workspaceItems: { id: NavigationItem; label: string; icon: typeof LayoutDashboard }[] = [
  { id: 'overview', label: 'Overview Dashboard', icon: LayoutDashboard },
  { id: 'soil-intelligence', label: 'Soil Intelligence', icon: Sprout },
  { id: 'recommendations', label: 'Fertilizer Recommendations', icon: Sparkles },
];

const telemetryItems: { id: NavigationItem; label: string; icon: typeof History }[] = [
  { id: 'prediction-history', label: 'Prediction History', icon: History },
  { id: 'model-audit', label: 'Model Intelligence', icon: Cpu },
  { id: 'system-health', label: 'System Health', icon: Activity },
];

export default function Sidebar({ activeNav, onNavChange, isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-xs"
          onClick={onClose}
          aria-label="Close sidebar"
        />
      )}

      <aside
        className={`
          fixed top-0 left-0 h-full z-50
          w-[275px] bg-[#09262A] text-white
          flex flex-col border-r border-[#0E383C]
          transition-transform duration-300 ease-in-out
          lg:translate-x-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
        role="navigation"
        aria-label="Main navigation"
      >
        {/* Logo Branding */}
        <div className="px-6 pt-6 pb-5 flex items-center gap-3.5 border-b border-[#0E383C]">
          <div className="w-9 h-9 rounded-xl bg-[#10B981] flex items-center justify-center shadow-xs shrink-0">
            <Leaf className="w-5 h-5 text-[#09262A]" strokeWidth={2.5} />
          </div>
          <div>
            <div className="text-base font-extrabold tracking-tight text-white leading-tight">Fieldwise</div>
            <div className="text-[0.58rem] font-mono uppercase tracking-[0.2em] text-[#10B981] font-bold leading-tight">
              AGRONOMY CONSOLE
            </div>
          </div>
        </div>

        {/* Navigation Section */}
        <div className="flex-1 overflow-y-auto py-5 px-3.5 space-y-6">
          {/* WORKSPACE & INTELLIGENCE section */}
          <div>
            <div className="px-3 mb-2.5">
              <span className="text-[0.6rem] font-mono uppercase tracking-[0.2em] text-[#64748B] font-semibold">
                AGRONOMY WORKSPACE
              </span>
            </div>
            <ul className="space-y-1">
              {workspaceItems.map((item) => {
                const isActive = activeNav === item.id;
                const Icon = item.icon;
                return (
                  <li key={item.id}>
                    <button
                      onClick={() => {
                        onNavChange(item.id);
                        onClose();
                      }}
                      className={`
                        w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium
                        transition-all duration-150 cursor-pointer
                        ${isActive
                          ? 'bg-[#0E383C] text-white shadow-xs border border-[#184F55]/60'
                          : 'text-[#94A3B8] hover:text-white hover:bg-[#0E383C]/50'
                        }
                      `}
                      aria-current={isActive ? 'page' : undefined}
                    >
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-[#10B981]' : 'text-[#64748B]'}`} strokeWidth={isActive ? 2 : 1.5} />
                      <span className="flex-1 text-left font-medium">{item.label}</span>
                      {isActive && (
                        <span className="w-2 h-2 rounded-full bg-[#10B981] shadow-xs" />
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>

          {/* TELEMETRY & AUDIT section */}
          <div>
            <div className="px-3 mb-2.5">
              <span className="text-[0.6rem] font-mono uppercase tracking-[0.2em] text-[#64748B] font-semibold">
                TELEMETRY & AUDIT
              </span>
            </div>
            <ul className="space-y-1">
              {telemetryItems.map((item) => {
                const isActive = activeNav === item.id;
                const Icon = item.icon;
                return (
                  <li key={item.id}>
                    <button
                      onClick={() => {
                        onNavChange(item.id);
                        onClose();
                      }}
                      className={`
                        w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium
                        transition-all duration-150 cursor-pointer
                        ${isActive
                          ? 'bg-[#0E383C] text-white shadow-xs border border-[#184F55]/60'
                          : 'text-[#94A3B8] hover:text-white hover:bg-[#0E383C]/50'
                        }
                      `}
                      aria-current={isActive ? 'page' : undefined}
                    >
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-[#10B981]' : 'text-[#64748B]'}`} strokeWidth={isActive ? 2 : 1.5} />
                      <span className="flex-1 text-left font-medium">{item.label}</span>
                      {isActive && (
                        <span className="w-2 h-2 rounded-full bg-[#10B981] shadow-xs" />
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>

        {/* System Engine Status Footer */}
        <div className="p-4 border-t border-[#0E383C] bg-[#071E20]">
          <div className="px-2 mb-1">
            <span className="text-[0.58rem] font-mono uppercase tracking-[0.2em] text-[#64748B] font-semibold">
              SYSTEM ENGINE
            </span>
          </div>
          <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-[#09262A] border border-[#0E383C]">
            <div className="flex items-center gap-2">
              <Radio className="w-3.5 h-3.5 text-[#10B981] animate-pulse" />
              <span className="text-xs text-[#10B981] font-semibold">FastAPI Gateway</span>
            </div>
            <span className="text-[0.6rem] font-mono text-[#94A3B8]">v1.0.0</span>
          </div>
        </div>
      </aside>
    </>
  );
}
