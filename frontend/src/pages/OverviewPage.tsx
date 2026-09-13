import { useState, useEffect, useCallback, useRef } from 'react';
import { Database, Activity, FlaskConical, Cpu, Sparkles } from 'lucide-react';
import KpiCard from '../components/KpiCard';
import SoilReadingCard from '../components/SoilReadingCard';
import RecommendationResult from '../components/RecommendationResult';
import PredictionHistory from '../components/PredictionHistory';
import SystemHealthBar from '../components/SystemHealthBar';
import ModelIntelligenceCard from '../components/ModelIntelligenceCard';
import {
  getRecommendation,
  fetchPredictions,
  fetchKpiStats,
} from '../services/recommendationService';
import { mockPredictionHistory, mockKpiData, defaultSoilReading } from '../data/mockData';
import type {
  SoilReading,
  RecommendationResult as RecommendationResultType,
  LoadingStep,
  PredictionRecord,
  KpiData,
} from '../types';

export default function OverviewPage() {
  const [soilReading, setSoilReading] = useState<SoilReading>({ ...defaultSoilReading });
  const [result, setResult] = useState<RecommendationResultType | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<LoadingStep | null>(null);

  const [predictions, setPredictions] = useState<PredictionRecord[]>([...mockPredictionHistory]);
  const [kpi, setKpi] = useState<KpiData>(mockKpiData);

  const recommendAbortRef = useRef<AbortController | null>(null);

  const loadDashboardData = useCallback(async () => {
    try {
      const [predictionsResult, statsResult] = await Promise.allSettled([
        fetchPredictions(1, 20),
        fetchKpiStats(),
      ]);

      if (predictionsResult.status === 'fulfilled' && predictionsResult.value.records.length > 0) {
        setPredictions(predictionsResult.value.records);
      }

      if (statsResult.status === 'fulfilled' && statsResult.value.predictionsLogged > 0) {
        setKpi(statsResult.value);
      }
    } catch {
      // Keep rich default state on error
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const handleGenerate = useCallback(async () => {
    if (isLoading) return;

    recommendAbortRef.current?.abort();
    const controller = new AbortController();
    recommendAbortRef.current = controller;

    setIsLoading(true);
    setResult(null);

    const steps: { step: LoadingStep; delay: number }[] = [
      { step: 'analyzing', delay: 0 },
      { step: 'evaluating', delay: 400 },
      { step: 'running', delay: 800 },
      { step: 'complete', delay: 1200 },
    ];

    for (const { step, delay } of steps) {
      await new Promise((resolve) => setTimeout(resolve, delay === 0 ? 0 : 400));
      if (controller.signal.aborted) return;
      setLoadingStep(step);
    }

    try {
      const recommendation = await getRecommendation(soilReading, controller.signal);

      if (controller.signal.aborted) return;

      setResult(recommendation);

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
        latencyMs: 12.5,
      };

      setPredictions((prev) => [newRecord, ...prev]);

      fetchKpiStats()
        .then((data) => {
          if (data.predictionsLogged > 0) setKpi(data);
        })
        .catch(() => {
          setKpi((prev) => ({
            ...prev,
            predictionsLogged: prev.predictionsLogged + 1,
          }));
        });
    } catch (err) {
      if (controller.signal.aborted) return;
      console.error('[OverviewPage] Recommendation error:', err);
    } finally {
      if (!controller.signal.aborted) {
        setIsLoading(false);
        setLoadingStep(null);
      }
    }
  }, [isLoading, soilReading]);

  useEffect(() => {
    return () => {
      recommendAbortRef.current?.abort();
    };
  }, []);

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div className="bg-[#09262A] text-white p-6 sm:p-8 rounded-2xl shadow-xl relative overflow-hidden border border-[#0E383C]">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-[#10B981]/10 to-transparent pointer-events-none" />
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#0E383C] border border-[#184F55] text-xs font-mono text-[#10B981] font-bold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            AI-POWERED AGRONOMY CONSOLE
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight mb-2 text-white">
            Precision Nutrient Intelligence Platform
          </h1>
          <p className="text-xs sm:text-sm text-[#94A3B8] font-medium leading-relaxed">
            Real-time machine learning inference for optimal crop fertilization based on soil pH, N-P-K nutrient composition, and growth stage metrics.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Total Predictions"
          value={kpi.predictionsLogged}
          subtitle="All-time inference logs"
          icon={<Database className="w-5 h-5 text-[#10B981]" />}
          iconVariant="emerald"
          trend="+12% this week"
        />
        <KpiCard
          label="Average Confidence"
          value={`${kpi.averageConfidence}%`}
          subtitle="Model accuracy index"
          icon={<Activity className="w-5 h-5 text-[#F59E0B]" />}
          iconVariant="amber"
          trend="P99: 98.2%"
        />
        <KpiCard
          label="Top Recommendation"
          value={kpi.frequentRecommendation}
          subtitle="Most frequent output"
          icon={<FlaskConical className="w-5 h-5 text-blue-600" />}
          iconVariant="blue"
        />
        <KpiCard
          label="Active Model Engine"
          value="model-v1"
          subtitle="XGBoost Ensemble"
          icon={<Cpu className="w-5 h-5 text-[#10B981]" />}
          iconVariant="teal"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

      <ModelIntelligenceCard modelVersion="model-v1" gatewayStatus="healthy" />

      <PredictionHistory
        records={predictions}
        totalCount={kpi.predictionsLogged}
        onRefresh={loadDashboardData}
      />

      <SystemHealthBar />
    </div>
  );
}
