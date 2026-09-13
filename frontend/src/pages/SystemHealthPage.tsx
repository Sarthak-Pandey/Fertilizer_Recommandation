import SystemHealthBar from '../components/SystemHealthBar';

export default function SystemHealthPage() {
  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-[#09262A] tracking-tight">Infrastructure & System Health</h1>
        <p className="text-xs text-[#64748B]">
          Live operational status monitoring for FastAPI Gateway, ML Inference Service, and SQLite Database.
        </p>
      </div>

      <SystemHealthBar />
    </div>
  );
}
