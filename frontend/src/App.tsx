import { useState, useCallback } from 'react';
import AppShell from './components/AppShell';

export default function App() {
  const [resetKey, setResetKey] = useState(0);

  const handleNewReading = useCallback(() => {
    setResetKey((k) => k + 1);
  }, []);

  return <AppShell key={resetKey} onNewReading={handleNewReading} />;
}
