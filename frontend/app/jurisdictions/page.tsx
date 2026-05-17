"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import { fetchAPI } from "@/services/api"

export default function JurisdictionsPage() {
  const [jurisdictions, setJurisdictions] = useState([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI("/jurisdictions")
      .then(setJurisdictions)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = jurisdictions.filter((j: any) =>
    j.name?.toLowerCase().includes(search.toLowerCase()) ||
    j.regulator?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <DashboardLayout>
      <div className="max-w-4xl space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-[#1a1a1a]">Jurisdictions</h2>
            <p className="text-[#6B6860] text-sm mt-0.5">{jurisdictions.length} regions monitored</p>
          </div>
          <input
            type="text"
            placeholder="Search jurisdictions..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-[#E2E0D8] rounded-lg px-4 py-2 w-64 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#1C3F5E]/20"
          />
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl border border-[#E2E0D8] p-6 h-28 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {filtered.map((j: any) => (
              <div key={j.id} className="bg-white border border-[#E2E0D8] rounded-2xl p-5 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-[#1a1a1a]">{j.name}</h3>
                <p className="text-sm text-[#6B6860] mt-1">{j.regulator}</p>
                {j.official_source && (
                  <a
                    href={j.official_source}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block mt-3 text-xs font-mono text-[#1C3F5E] hover:underline"
                  >
                    Official Source →
                  </a>
                )}
              </div>
            ))}
            {filtered.length === 0 && (
              <div className="col-span-2 text-center py-16 text-[#6B6860] text-sm">No jurisdictions found.</div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
