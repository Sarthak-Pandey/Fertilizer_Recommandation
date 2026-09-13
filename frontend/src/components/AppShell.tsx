import { useState, useCallback, useRef } from 'react';
import Sidebar from '../components/Sidebar';
import TopHeader from '../components/TopHeader';
import Footer from '../components/Footer';
import type { NavigationItem } from '../types';

interface AppShellProps {
  children: React.ReactNode;
  onNewReading: () => void;
}

export default function AppShell({ children, onNewReading }: AppShellProps) {
  const [activeNav, setActiveNav] = useState<NavigationItem>('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const mainRef = useRef<HTMLDivElement>(null);

  const handleRefresh = useCallback(() => {
    if (mainRef.current) {
      mainRef.current.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, []);

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Sidebar
        activeNav={activeNav}
        onNavChange={setActiveNav}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main content area */}
      <div className="flex-1 lg:ml-[275px] flex flex-col min-h-screen">
        <TopHeader
          onNewReading={onNewReading}
          onRefresh={handleRefresh}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main
          ref={mainRef}
          className="flex-1 overflow-y-auto grid-background"
        >
          {children}
        </main>

        <Footer />
      </div>
    </div>
  );
}
