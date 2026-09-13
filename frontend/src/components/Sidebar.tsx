import { Leaf, LayoutDashboard, History, ShieldCheck } from 'lucide-react';
import type { NavigationItem } from '../types';

interface SidebarProps {
  activeNav: NavigationItem;
  onNavChange: (item: NavigationItem) => void;
  isOpen: boolean;
  onClose: () => void;
}

const navItems: { id: NavigationItem; label: string; icon: typeof LayoutDashboard }[] = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'prediction-history', label: 'Prediction history', icon: History },
  { id: 'model-audit', label: 'Model audit', icon: ShieldCheck },
];

export default function Sidebar({ activeNav, onNavChange, isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onClose}
          aria-label="Close sidebar"
        />
      )}

      <aside
        className={`
          fixed top-0 left-0 h-full z-50
          w-[275px] bg-[#102D32] text-white
          flex flex-col
          transition-transform duration-300 ease-in-out
          lg:translate-x-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
        role="navigation"
        aria-label="Main navigation"
      >
        {/* Logo */}
        <div className="px-5 pt-6 pb-5 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-[#F2C14E] flex items-center justify-center">
            <Leaf className="w-4.5 h-4.5 text-[#102D32]" strokeWidth={2.5} />
          </div>
          <div>
            <div className="text-sm font-bold tracking-wide leading-tight">Fieldwise</div>
            <div className="text-[0.6rem] font-mono uppercase tracking-[0.16em] text-[#6E858B] leading-tight">
              Agronomy Console
            </div>
          </div>
        </div>

        {/* Workspace label */}
        <div className="px-5 pt-4 pb-2">
          <span className="text-[0.6rem] font-mono uppercase tracking-[0.18em] text-[#6E858B] font-medium">
            Workspace
          </span>
        </div>

        {/* Navigation */}
        <nav className="px-3 flex-1">
          <ul className="space-y-0.5">
            {navItems.map((item) => {
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
                      w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm
                      transition-all duration-150 cursor-pointer
                      ${isActive
                        ? 'bg-[#1a4a52] text-white font-medium'
                        : 'text-[#6E858B] hover:text-white hover:bg-[#163238]'
                      }
                    `}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    <Icon className="w-4 h-4 shrink-0" strokeWidth={isActive ? 2 : 1.5} />
                    <span className="flex-1 text-left">{item.label}</span>
                    {isActive && (
                      <span className="w-2 h-2 rounded-full bg-[#F2C14E]" />
                    )}
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Bottom system status */}
        <div className="px-4 pb-4">
          <div className="flex items-center gap-2 px-3 py-2.5">
            <span className="meta-label text-[#6E858B]">System</span>
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#4D947A]" />
              <span className="text-[0.65rem] text-[#4D947A] font-medium">FastAPI active</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
