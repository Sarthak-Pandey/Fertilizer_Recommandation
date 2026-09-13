import { useState, useCallback, useRef } from 'react';
import Sidebar from '../components/Sidebar';
import TopHeader from '../components/TopHeader';
import Footer from '../components/Footer';
import OverviewPage from '../pages/OverviewPage';
import SoilIntelligencePage from '../pages/SoilIntelligencePage';
import FertilizerRecommendationsPage from '../pages/FertilizerRecommendationsPage';
import PredictionHistoryPage from '../pages/PredictionHistoryPage';
import ModelIntelligencePage from '../pages/ModelIntelligencePage';
import SystemHealthPage from '../pages/SystemHealthPage';
import type { NavigationItem } from '../types';

interface AppShellProps {
  onNewReading: () => void;
}

export default function AppShell({ onNewReading }: AppShellProps) {
  const [activeNav, setActiveNav] = useState<NavigationItem>('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const mainRef = useRef<HTMLDivElement>(null);

  const handleRefresh = useCallback(() => {
    if (mainRef.current) {
      mainRef.current.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, []);

  const handleNewReadingClick = useCallback(() => {
    setActiveNav('overview');
    onNewReading();
  }, [onNewReading]);

  const renderActivePage = () => {
    switch (activeNav) {
      case 'overview':
        return <OverviewPage />;
      case 'soil-intelligence':
        return <SoilIntelligencePage />;
      case 'recommendations':
        return <FertilizerRecommendationsPage />;
      case 'prediction-history':
        return <PredictionHistoryPage />;
      case 'model-audit':
        return <ModelIntelligencePage />;
      case 'system-health':
        return <SystemHealthPage />;
      default:
        return <OverviewPage />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#F9F8F5] text-[#0F172A] font-sans antialiased">
      {/* Sidebar */}
      <Sidebar
        activeNav={activeNav}
        onNavChange={setActiveNav}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 lg:ml-[275px] flex flex-col min-h-screen min-w-0">
        <TopHeader
          onNewReading={handleNewReadingClick}
          onRefresh={handleRefresh}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        <main ref={mainRef} className="flex-1 overflow-y-auto min-w-0">
          {renderActivePage()}
        </main>

        <Footer />
      </div>
    </div>
  );
}
