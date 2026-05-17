"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import { fetchAPI } from "@/services/api"

function formatDate(raw: string) {
  if (!raw) return "—"
  return new Date(raw).toLocaleString("en-GB", {
    day: "numeric", month: "short", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  })
}

export default function SnapshotsPage() {
  const [snapshots, setSnapshots] = useState([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI("/snapshots")
      .then(setSnapshots)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = snapshots.filter((s: any) =>
    s.source_url?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <DashboardLayout>
      <div className="max-w-4xl space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-[#1a1a1a]">Snapshots</h2>
            <p className="text-[#6B6860] text-sm mt-0.5">{snapshots.length} snapshots archived</p>
          </div>
          <input
            type="text"
            placeholder="Filter by URL..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-[#E2E0D8] rounded-lg px-4 py-2 w-64 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#1C3F5E]/20"
          />
        </div>

        {loading ? (
          <div className="space-y-3">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl border border-[#E2E0D8] p-5 h-24 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((s: any) => (
              <div key={s.id} className="bg-white border border-[#E2E0D8] rounded-xl p-5 hover:shadow-sm transition-shadow">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <a
                      href={s.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-medium text-[#1C3F5E] hover:underline truncate block"
                    >
                      {s.source_url}
                    </a>
                    <p className="text-xs font-mono text-[#6B6860] mt-1.5 truncate">
                      {s.content_hash}
                    </p>
                  </div>
                  <div className="shrink-0 text-right">
                    <span className="text-xs font-mono text-[#6B6860]">#{s.id}</span>
                    <p className="text-xs text-[#6B6860] mt-1">{formatDate(s.created_at)}</p>
                  </div>
                </div>
              </div>
            ))}
            {filtered.length === 0 && (
              <div className="text-center py-16 text-[#6B6860] text-sm">No snapshots match your filter.</div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
