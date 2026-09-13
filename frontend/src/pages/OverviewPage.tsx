import { useState, useCallback } from 'react';
import { Database, Activity, FlaskConical } from 'lucide-react';
import PageHeader from '../components/PageHeader';
import KpiCard from '../components/KpiCard';
import SoilReadingCard from '../components/SoilReadingCard';
import RecommendationResult from '../components/RecommendationResult';
import PredictionHistory from '../components/PredictionHistory';
import SystemHealthBar from '../components/SystemHealthBar';
import { getRecommendation } from '../services/recommendationService';
import { mockPredictionHistory, mockKpiData, defaultSoilReading } from '../data/mockData';
import type { SoilReading, RecommendationResult as RecommendationResultType, LoadingStep, PredictionRecord } from '../types';

export default function OverviewPage() {
  const [soilReading, setSoilReading] = useState<SoilReading>({ ...defaultSoilReading });
  const [result, setResult] = useState<RecommendationResultType | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<LoadingStep | null>(null);
  const [predictions, setPredictions] = useState<PredictionRecord[]>([...mockPredictionHistory]);
  const [kpi, setKpi] = useState(mockKpiData);

  const handleGenerate = useCallback(async () => {
    if (isLoading) return;

    setIsLoading(true);
    setResult(null);

    // Simulate loading steps
    const steps: { step: LoadingStep; delay: number }[] = [
      { step: 'analyzing', delay: 0 },
      { step: 'evaluating', delay: 700 },
      { step: 'running', delay: 1400 },
      { step: 'complete', delay: 2100 },
    ];

    for (const { step, delay } of steps) {
      await new Promise((resolve) => setTimeout(resolve, delay === 0 ? 0 : 700));
      setLoadingStep(step);
    }

    try {
      const recommendation = await getRecommendation(soilReading);
      setResult(recommendation);

      // Add to prediction history
      const newRecord: PredictionRecord = {
        id: recommendation.predictionId,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        status: 'success',
        recommendation: recommendation.recommendation.product,
        confidence: recommendation.recommendation.confidence,
        capturedTime: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        soilPh: soilReading.soilPh,
        nitrogen: soilReading.nitrogen,
        phosphorus: soilReading.phosphorus,
        potassium: soilReading.potassium,
        growthStage: soilReading.growthStage,
        modelVersion: 'model-v1',
        auditStatus: 'Verified',
        fullTimestamp: new Date().toISOString(),
      };

      setPredictions((prev) => [newRecord, ...prev]);
      setKpi((prev) => ({
        ...prev,
        predictionsLogged: prev.predictionsLogged + 1,
      }));
    } finally {
      setIsLoading(false);
      setLoadingStep(null);
    }
  }, [isLoading, soilReading]);

  return (
    <div className="px-6 lg:px-8 py-6">
      {/* Page header */}
      <PageHeader />

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <KpiCard
          label="Predictions Logged"
          value={kpi.predictionsLogged}
          subtitle="All time"
          icon={<Database className="w-4.5 h-4.5" />}
          iconVariant="blue"
        />
        <KpiCard
          label="Average Confidence"
          value={`${kpi.averageConfidence}%`}
          subtitle="Across recent runs"
          icon={<Activity className="w-4.5 h-4.5" />}
          iconVariant="yellow"
        />
        <KpiCard
          label="Frequent Recommendation"
          value={kpi.frequentRecommendation}
          subtitle="Most selected output"
          icon={<FlaskConical className="w-4.5 h-4.5" />}
          iconVariant="pink"
        />
      </div>

      {/* Step 01 & Step 02 — two-column workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <SoilReadingCard
          reading={soilReading}
          onChange={setSoilReading}
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />
        <RecommendationResult
          result={result}
          isLoading={isLoading}
          loadingStep={loadingStep}
        />
      </div>

      {/* Recent recommendations — full width */}
      <div className="mb-6">
        <PredictionHistory records={predictions} totalCount={kpi.predictionsLogged} />
      </div>

      {/* System Health Bar — full width */}
      <div className="mb-6">
        <SystemHealthBar />
      </div>
    </div>
  );
}
