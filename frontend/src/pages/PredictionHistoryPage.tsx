import { useState, useEffect } from 'react';
import PredictionHistory from '../components/PredictionHistory';
import { fetchPredictions } from '../services/recommendationService';
import { mockPredictionHistory } from '../data/mockData';
import type { PredictionRecord } from '../types';

export default function PredictionHistoryPage() {
  const [predictions, setPredictions] = useState<PredictionRecord[]>([...mockPredictionHistory]);
  const [total, setTotal] = useState<number>(mockPredictionHistory.length);

  const loadData = async () => {
    try {
      const res = await fetchPredictions(1, 50);
      if (res.records.length > 0) {
        setPredictions(res.records);
        setTotal(res.total);
      }
    } catch {
      // keep mock fallback
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-[#09262A] tracking-tight">Prediction Telemetry & History</h1>
        <p className="text-xs text-[#64748B]">
          Complete paginated audit log of historical soil composition analyses and model inference outputs.
        </p>
      </div>

      <PredictionHistory records={predictions} totalCount={total} onRefresh={loadData} />
    </div>
  );
}
