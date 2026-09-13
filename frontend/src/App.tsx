import { useState, useCallback } from 'react';
import AppShell from './components/AppShell';
import OverviewPage from './pages/OverviewPage';

export default function App() {
  const [resetKey, setResetKey] = useState(0);

  const handleNewReading = useCallback(() => {
    setResetKey((k) => k + 1);
  }, []);

  return (
    <AppShell onNewReading={handleNewReading}>
      <OverviewPage key={resetKey} />
    </AppShell>
  );
}
