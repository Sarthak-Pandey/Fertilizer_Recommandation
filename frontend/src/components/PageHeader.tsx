import { ShieldCheck } from 'lucide-react';

export default function PageHeader() {
  return (
    <section className="mb-6">
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div>
          <div className="meta-label mb-2 text-[#4D947A]">
            Tuesday, 18 June 2024 · North Block
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#102D32] tracking-tight leading-tight mb-2">
            Make the next application count.
          </h2>
          <p className="text-sm text-[#6E858B] max-w-lg">
            A clear recommendation, with the evidence to stand behind it in the field.
          </p>
        </div>

        {/* Auditable badge */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-[#DDD9CE] bg-white text-xs text-[#6E858B] whitespace-nowrap self-start">
          <ShieldCheck className="w-3.5 h-3.5" />
          Auditable by default
        </div>
      </div>
    </section>
  );
}
