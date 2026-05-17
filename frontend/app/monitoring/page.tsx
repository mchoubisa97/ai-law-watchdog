"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import { getCrawlerRuns, triggerCrawlers } from "@/services/api"

function formatDate(raw: string) {
  if (!raw) return "—"
  return new Date(raw).toLocaleString("en-GB", {
    day: "numeric", month: "short",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  })
}

function duration(start: string, end: string) {
  if (!start || !end) return "—"
  const ms = new Date(end).getTime() - new Date(start).getTime()
  return `${(ms / 1000).toFixed(1)}s`
}

export default function MonitoringPage() {
  const [runs, setRuns] = useState([])
  const [filter, setFilter] = useState<"all" | "success" | "failed">("all")
  const [loading, setLoading] = useState(true)
  const [triggering, setTriggering] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const data = await getCrawlerRuns(filter === "all" ? undefined : filter)
      setRuns(data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [filter])

  async function handleTrigger() {
    setTriggering(true)
    try {
      await triggerCrawlers()
      setTimeout(load, 2000)
    } catch (e) {
      console.error(e)
    } finally {
      setTriggering(false)
    }
  }

  const successCount = runs.filter((r: any) => r.status === "success").length
  const failedCount = runs.filter((r: any) => r.status === "failed").length

  return (
    <DashboardLayout>
      <div className="max-w-5xl space-y-6">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-[#1a1a1a]">Crawler Monitoring</h2>
            <p className="text-[#6B6860] text-sm mt-0.5">
              {runs.length} runs — {successCount} succeeded, {failedCount} failed
            </p>
          </div>
          <button
            onClick={handleTrigger}
            disabled={triggering}
            className="bg-[#1C3F5E] text-white text-sm px-5 py-2 rounded-lg hover:bg-[#163352] transition disabled:opacity-50 font-medium"
          >
            {triggering ? "Triggering..." : "▶ Run Crawlers"}
          </button>
        </div>

        {/* Filter tabs */}
        <div className="flex gap-2">
          {(["all", "success", "failed"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-medium capitalize transition ${
                filter === f
                  ? "bg-[#1C3F5E] text-white"
                  : "bg-white border border-[#E2E0D8] text-[#6B6860] hover:border-[#1C3F5E]"
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl border border-[#E2E0D8] h-14 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="bg-white border border-[#E2E0D8] rounded-2xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[#E2E0D8] bg-[#F5F4F0]">
                  <th className="text-left px-5 py-3 text-xs font-mono text-[#6B6860] uppercase tracking-wide">Crawler</th>
                  <th className="text-left px-5 py-3 text-xs font-mono text-[#6B6860] uppercase tracking-wide">Status</th>
                  <th className="text-left px-5 py-3 text-xs font-mono text-[#6B6860] uppercase tracking-wide">Duration</th>
                  <th className="text-left px-5 py-3 text-xs font-mono text-[#6B6860] uppercase tracking-wide">Message</th>
                  <th className="text-left px-5 py-3 text-xs font-mono text-[#6B6860] uppercase tracking-wide">Started</th>
                </tr>
              </thead>
              <tbody>
                {runs.map((run: any, i: number) => (
                  <tr
                    key={run.id}
                    className={`border-b border-[#E2E0D8] last:border-0 hover:bg-[#F9F8F5] transition-colors ${i % 2 === 0 ? "" : "bg-[#FAFAF8]"}`}
                  >
                    <td className="px-5 py-3 font-medium text-[#1a1a1a]">{run.crawler_name}</td>
                    <td className="px-5 py-3">
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        run.status === "success"
                          ? "bg-[#EAFAF2] text-[#1A6B3C]"
                          : "bg-[#FDF0F0] text-[#8B1A1A]"
                      }`}>
                        {run.status}
                      </span>
                    </td>
                    <td className="px-5 py-3 font-mono text-xs text-[#6B6860]">
                      {duration(run.started_at, run.finished_at)}
                    </td>
                    <td className="px-5 py-3 text-xs text-[#6B6860] max-w-xs truncate">{run.message || "—"}</td>
                    <td className="px-5 py-3 text-xs font-mono text-[#6B6860]">{formatDate(run.started_at)}</td>
                  </tr>
                ))}
                {runs.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-5 py-16 text-center text-[#6B6860] text-sm">
                      No crawler runs recorded yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
