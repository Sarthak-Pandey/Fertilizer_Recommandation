import { ShieldCheck, Calendar } from 'lucide-react';

export default function PageHeader() {
  return (
    <section className="mb-6">
      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div>
          {/* Subheader tag */}
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="w-3.5 h-3.5 text-[#4D947A]" />
            <span className="text-[0.65rem] font-mono uppercase tracking-[0.16em] text-[#4D947A] font-bold">
              TUESDAY, 18 JUNE 2026 · NORTH BLOCK
            </span>
          </div>

          {/* Main Title */}
          <h2 className="text-3xl sm:text-4xl font-extrabold text-[#102D32] tracking-tight leading-tight mb-2">
            Make the next application count.
          </h2>

          {/* Subtitle */}
          <p className="text-sm text-[#6E858B] max-w-xl font-medium">
            A clear recommendation, with the evidence to stand behind it in the field.
          </p>
        </div>

        {/* Auditable badge */}
        <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-[#DDD9CE]/80 bg-white shadow-xs text-xs font-semibold text-[#102D32] whitespace-nowrap self-start">
          <ShieldCheck className="w-4 h-4 text-[#4D947A]" />
          <span>Auditable by default</span>
        </div>
      </div>
    </section>
  );
}
