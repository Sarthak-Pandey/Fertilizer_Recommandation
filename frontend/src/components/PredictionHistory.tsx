import { useState, useMemo } from 'react';
import { History, Search, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react';
import PredictionRow from './PredictionRow';
import PredictionDetailModal from './PredictionDetailModal';
import type { PredictionRecord } from '../types';

interface PredictionHistoryProps {
  records: PredictionRecord[];
  totalCount?: number;
  onRefresh?: () => void;
}

export default function PredictionHistory({
  records,
  totalCount,
  onRefresh,
}: PredictionHistoryProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [stageFilter, setStageFilter] = useState<string>('ALL');
  const [fertilizerFilter, setFertilizerFilter] = useState<string>('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRecord, setSelectedRecord] = useState<PredictionRecord | null>(null);

  const pageSize = 8;

  const filteredRecords = useMemo(() => {
    return records.filter((r) => {
      const matchesSearch =
        r.recommendation.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.growthStage.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesStage = stageFilter === 'ALL' || r.growthStage === stageFilter;
      const matchesFertilizer = fertilizerFilter === 'ALL' || r.recommendation === fertilizerFilter;

      return matchesSearch && matchesStage && matchesFertilizer;
    });
  }, [records, searchTerm, stageFilter, fertilizerFilter]);

  const totalPages = Math.ceil(filteredRecords.length / pageSize) || 1;
  const paginatedRecords = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredRecords.slice(start, start + pageSize);
  }, [filteredRecords, currentPage, pageSize]);

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-2xs">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <History className="w-4 h-4 text-[#10B981]" />
            <h3 className="text-lg font-extrabold text-[#09262A] tracking-tight">Prediction Telemetry History</h3>
          </div>
          <p className="text-xs text-[#64748B]">
            Logged inference audit trail across soil probe analyses. Total entries: {totalCount ?? records.length}
          </p>
        </div>

        {onRefresh && (
          <button
            type="button"
            onClick={onRefresh}
            className="self-start md:self-auto flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#E2E8F0] bg-[#F9F8F5] text-[#09262A] text-xs font-semibold hover:bg-[#E2E8F0] transition-colors cursor-pointer"
          >
            <RefreshCw className="w-3.5 h-3.5 text-[#64748B]" />
            <span>Sync History</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            placeholder="Search by ID, recommendation..."
            className="w-full pl-9 pr-3 py-2 rounded-xl border border-[#CBD5E1] text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#10B981]/30 focus:border-[#10B981]"
          />
        </div>

        <div className="relative">
          <select
            value={stageFilter}
            onChange={(e) => {
              setStageFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full px-3 py-2 rounded-xl border border-[#CBD5E1] text-xs font-medium bg-white focus:outline-none focus:ring-2 focus:ring-[#10B981]/30 focus:border-[#10B981]"
          >
            <option value="ALL">All Growth Stages</option>
            <option value="Sowing">Sowing</option>
            <option value="Vegetative">Vegetative</option>
            <option value="Flowering">Flowering</option>
            <option value="Harvest">Harvest</option>
          </select>
        </div>

        <div className="relative">
          <select
            value={fertilizerFilter}
            onChange={(e) => {
              setFertilizerFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full px-3 py-2 rounded-xl border border-[#CBD5E1] text-xs font-medium bg-white focus:outline-none focus:ring-2 focus:ring-[#10B981]/30 focus:border-[#10B981]"
          >
            <option value="ALL">All Fertilizer Outputs</option>
            <option value="Urea">Urea</option>
            <option value="DAP">DAP</option>
            <option value="MOP">MOP</option>
            <option value="14-35-14">14-35-14</option>
            <option value="28-28-0">28-28-0</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-[#E2E8F0]">
        <table className="w-full text-left border-collapse min-w-[700px]">
          <thead>
            <tr className="bg-[#F9F8F5] border-b border-[#E2E8F0] text-[0.65rem] font-mono uppercase text-[#64748B] tracking-wider">
              <th className="py-3 px-4 font-bold">Timestamp</th>
              <th className="py-3 px-4 font-bold">Soil pH</th>
              <th className="py-3 px-4 font-bold">N / P / K</th>
              <th className="py-3 px-4 font-bold">Growth Stage</th>
              <th className="py-3 px-4 font-bold">AI Output</th>
              <th className="py-3 px-4 font-bold">Confidence</th>
              <th className="py-3 px-4 font-bold">Latency</th>
              <th className="py-3 px-4 font-bold text-right">Audit</th>
            </tr>
          </thead>
          <tbody>
            {paginatedRecords.length > 0 ? (
              paginatedRecords.map((rec) => (
                <PredictionRow key={rec.id} record={rec} onInspect={(r) => setSelectedRecord(r)} />
              ))
            ) : (
              <tr>
                <td colSpan={8} className="py-8 text-center text-xs text-[#64748B]">
                  No prediction records match the selected filter parameters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between pt-4 mt-2 text-xs text-[#64748B]">
        <span>
          Showing {paginatedRecords.length > 0 ? (currentPage - 1) * pageSize + 1 : 0} to{' '}
          {Math.min(currentPage * pageSize, filteredRecords.length)} of {filteredRecords.length} entries
        </span>

        <div className="flex items-center gap-2">
          <button
            type="button"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            className="p-1.5 rounded-lg border border-[#E2E8F0] hover:bg-[#F9F8F5] disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="font-mono text-xs font-bold text-[#09262A]">
            Page {currentPage} of {totalPages}
          </span>
          <button
            type="button"
            disabled={currentPage >= totalPages}
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            className="p-1.5 rounded-lg border border-[#E2E8F0] hover:bg-[#F9F8F5] disabled:opacity-40 cursor-pointer"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      <PredictionDetailModal record={selectedRecord} onClose={() => setSelectedRecord(null)} />
    </div>
  );
}
