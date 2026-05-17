"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import { fetchAPI } from "@/services/api"

function formatDate(raw: string) {
  if (!raw) return "—"
  return new Date(raw).toLocaleDateString("en-GB", {
    day: "numeric", month: "short", year: "numeric",
  })
}

function parseSummaryAndDiff(description: string) {
  if (!description) return { summary: "", diff: "" }

  const summaryMatch = description.match(/SUMMARY:\n([\s\S]*?)(?:\n\nDIFF:|$)/)
  const diffMatch = description.match(/DIFF:\n([\s\S]*)$/)

  return {
    summary: summaryMatch ? summaryMatch[1].trim() : description,
    diff: diffMatch ? diffMatch[1].trim() : "",
  }
}

function DiffViewer({ diff }: { diff: string }) {
  if (!diff) return null

  const lines = diff.split("\n")

  return (
    <div className="mt-4 rounded-xl border border-[#E2E0D8] overflow-hidden">
      <div className="bg-[#F5F4F0] border-b border-[#E2E0D8] px-4 py-2 flex items-center justify-between">
        <span className="text-xs font-mono font-semibold text-[#6B6860] uppercase tracking-wide">
          Diff
        </span>
        <div className="flex gap-3 text-xs font-mono">
          <span className="text-[#1A6B3C]">
            +{lines.filter(l => l.startsWith("+") && !l.startsWith("+++")).length} added
          </span>
          <span className="text-[#8B1A1A]">
            -{lines.filter(l => l.startsWith("-") && !l.startsWith("---")).length} removed
          </span>
        </div>
      </div>
      <div className="overflow-x-auto max-h-72 overflow-y-auto bg-[#FAFAF8]">
        <table className="w-full text-xs font-mono border-collapse">
          <tbody>
            {lines.map((line, i) => {
              let bg = ""
              let color = "text-[#6B6860]"
              let prefix = " "

              if (line.startsWith("+++") || line.startsWith("---")) {
                bg = "bg-[#F0F0EE]"
                color = "text-[#6B6860]"
              } else if (line.startsWith("+")) {
                bg = "bg-[#EAFAF2]"
                color = "text-[#1A6B3C]"
                prefix = "+"
              } else if (line.startsWith("-")) {
                bg = "bg-[#FDF0F0]"
                color = "text-[#8B1A1A]"
                prefix = "-"
              } else if (line.startsWith("@@")) {
                bg = "bg-[#EBF0F5]"
                color = "text-[#1C3F5E]"
              }

              return (
                <tr key={i} className={`${bg} leading-relaxed`}>
                  <td className="w-8 px-3 py-0.5 text-right text-[#C0BDB5] select-none border-r border-[#E2E0D8]">
                    {i + 1}
                  </td>
                  <td className={`px-4 py-0.5 whitespace-pre ${color}`}>
                    {line || " "}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function TimelinePage() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState<number | null>(null)

  useEffect(() => {
    fetchAPI("/law-events")
      .then(setEvents)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <DashboardLayout>
      <div className="max-w-3xl space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-[#1a1a1a]">Regulatory Timeline</h2>
          <p className="text-[#6B6860] text-sm mt-0.5">{events.length} events recorded</p>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl border border-[#E2E0D8] p-6 h-28 animate-pulse" />
            ))}
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-20 text-[#6B6860] text-sm">
            No regulatory events recorded yet. Events appear when crawlers detect meaningful changes.
          </div>
        ) : (
          <div className="relative">
            <div className="absolute left-4 top-0 bottom-0 w-px bg-[#E2E0D8]" />
            <div className="space-y-4 pl-12">
              {events.map((event: any) => {
                const { summary, diff } = parseSummaryAndDiff(event.description)
                const isExpanded = expanded === event.id
                const hasDiff = !!diff

                return (
                  <div key={event.id} className="relative">
                    <div className="absolute -left-8 top-5 w-2.5 h-2.5 rounded-full bg-[#1C3F5E] border-2 border-white shadow" />
                    <div className="bg-white border border-[#E2E0D8] rounded-2xl p-5 hover:shadow-md transition-shadow">

                      {/* Header */}
                      <div className="flex items-start justify-between gap-3">
                        <h3 className="text-sm font-semibold text-[#1a1a1a]">
                          {event.event_title || event.event_type}
                        </h3>
                        <span className="shrink-0 bg-[#EBF0F5] text-[#1C3F5E] px-2.5 py-0.5 rounded-full text-xs font-mono">
                          {formatDate(event.event_date)}
                        </span>
                      </div>

                      {/* Summary */}
                      <p className="text-sm text-[#6B6860] mt-2 leading-relaxed">
                        {summary}
                      </p>

                      {/* Footer row */}
                      <div className="flex items-center justify-between mt-3">
                        <div className="flex items-center gap-3">
                          {event.source_url && (
                            <a
                              href={event.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs font-mono text-[#1C3F5E] hover:underline"
                            >
                              Source →
                            </a>
                          )}
                        </div>

                        {hasDiff && (
                          <button
                            onClick={() => setExpanded(isExpanded ? null : event.id)}
                            className="text-xs font-mono text-[#1C3F5E] bg-[#EBF0F5] hover:bg-[#D8E3EE] px-3 py-1 rounded-full transition-colors"
                          >
                            {isExpanded ? "Hide diff ↑" : "View diff ↓"}
                          </button>
                        )}
                      </div>

                      {/* Diff viewer */}
                      {isExpanded && hasDiff && <DiffViewer diff={diff} />}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}