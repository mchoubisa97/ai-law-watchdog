"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import { fetchAPI } from "@/services/api"

export default function AILawsPage() {
  const [laws, setLaws] = useState([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI("/ai-laws")
      .then(setLaws)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = laws.filter((law: any) =>
    law.law_name.toLowerCase().includes(search.toLowerCase()) ||
    law.category?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <DashboardLayout>
      <div className="max-w-4xl space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-[#1a1a1a]">AI Laws</h2>
            <p className="text-[#6B6860] text-sm mt-0.5">{laws.length} laws tracked</p>
          </div>
          <input
            type="text"
            placeholder="Search laws..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-[#E2E0D8] rounded-lg px-4 py-2 w-64 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#1C3F5E]/20"
          />
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl border border-[#E2E0D8] p-6 h-36 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map((law: any) => (
              <div key={law.id} className="bg-white border border-[#E2E0D8] rounded-2xl p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between gap-4">
                  <h3 className="text-base font-semibold text-[#1a1a1a]">{law.law_name}</h3>
                  <div className="flex gap-2 shrink-0">
                    <span className="bg-[#EBF0F5] text-[#1C3F5E] px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {law.category}
                    </span>
                    <span className="bg-[#EAFAF2] text-[#1A6B3C] px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {law.current_status}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-[#6B6860] mt-2 leading-relaxed">{law.summary}</p>
                <a
                  href={law.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block mt-4 text-xs font-mono text-[#1C3F5E] hover:underline"
                >
                  Official Source →
                </a>
              </div>
            ))}
            {filtered.length === 0 && (
              <div className="text-center py-16 text-[#6B6860] text-sm">No laws match your search.</div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
