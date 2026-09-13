import ModelIntelligenceCard from '../components/ModelIntelligenceCard';

export default function ModelIntelligencePage() {
  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-[#09262A] tracking-tight">Model Intelligence & Architecture</h1>
        <p className="text-xs text-[#64748B]">
          XGBoost + Random Forest ensemble performance telemetry, feature schemas, and circuit breaker health.
        </p>
      </div>

      <ModelIntelligenceCard modelVersion="model-v1" gatewayStatus="healthy" />
    </div>
  );
}
