import { useState } from 'react';
import { ChevronLeft, ChevronRight, RefreshCw, ClipboardList } from 'lucide-react';
import PredictionRow from './PredictionRow';
import type { PredictionRecord } from '../types';

interface PredictionHistoryProps {
  records: PredictionRecord[];
  totalCount: number;
}

const ITEMS_PER_PAGE = 10;

export default function PredictionHistory({ records, totalCount }: PredictionHistoryProps) {
  const [page, setPage] = useState(1);
  const totalPages = Math.max(1, Math.ceil(records.length / ITEMS_PER_PAGE));
  const displayTotalPages = Math.max(1, Math.ceil(totalCount / ITEMS_PER_PAGE));
  const startIdx = (page - 1) * ITEMS_PER_PAGE;
  const pageRecords = records.slice(startIdx, startIdx + ITEMS_PER_PAGE);

  return (
    <div className="bg-white rounded-2xl border border-[#DDD9CE]/60 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <span className="step-label text-[#4D947A]">Audit Trail</span>
        <div className="flex items-center gap-3">
          <span className="text-xs text-[#6E858B]">Total: <span className="font-semibold text-[#102D32]">{totalCount}</span></span>
          <button className="flex items-center gap-1.5 text-xs text-[#6E858B] hover:text-[#102D32] transition-colors cursor-pointer">
            <RefreshCw className="w-3 h-3" />
            Refresh
          </button>
        </div>
      </div>

      <div className="flex items-center gap-2 mb-5">
        <ClipboardList className="w-5 h-5 text-[#102D32]" />
        <h3 className="text-lg font-bold text-[#102D32]">Recent recommendations</h3>
      </div>

      {/* Column headers */}
      <div className="flex items-center gap-4 pb-3 border-b border-[#DDD9CE]/50 px-1">
        <div className="w-8 meta-label">#</div>
        <div className="flex-[2] meta-label">Recommendation Output</div>
        <div className="flex-1 meta-label hidden sm:block">Confidence</div>
        <div className="flex-1 meta-label hidden sm:block">Date Status</div>
        <div className="flex-1 meta-label hidden md:block">Latency</div>
        <div className="flex-1 meta-label hidden md:block">Timestamp</div>
        <div className="w-14 meta-label hidden lg:block">Audit</div>
        <div className="w-6" />
      </div>

      {/* Rows */}
      <div>
        {pageRecords.length > 0 ? (
          pageRecords.map((record, index) => (
            <PredictionRow key={record.id} record={record} index={startIdx + index + 1} />
          ))
        ) : (
          <div className="py-8 text-center text-sm text-[#6E858B]">
            No prediction records to display.
          </div>
        )}
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between mt-4 pt-3 border-t border-[#DDD9CE]/30">
        <span className="text-xs text-[#6E858B]">
          Page {page} of {displayTotalPages}
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="flex items-center gap-1 px-3 py-1.5 rounded-lg border border-[#DDD9CE] hover:bg-[#F7F5EF] disabled:opacity-30 text-xs text-[#6E858B] transition-colors cursor-pointer disabled:cursor-not-allowed"
            aria-label="Previous page"
          >
            <ChevronLeft className="w-3 h-3" />
            Previous
          </button>
          <span className="text-xs text-[#6E858B] font-mono">{page} / {displayTotalPages}</span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="flex items-center gap-1 px-3 py-1.5 rounded-lg border border-[#DDD9CE] hover:bg-[#F7F5EF] disabled:opacity-30 text-xs text-[#6E858B] transition-colors cursor-pointer disabled:cursor-not-allowed"
            aria-label="Next page"
          >
            Next
            <ChevronRight className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  );
}
