"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/shared/DashboardLayout"
import StatsCard from "@/components/dashboard/StatsCard"
import { fetchAPI } from "@/services/api"

export default function DashboardPage() {
  const [stats, setStats] = useState({ laws: 0, jurisdictions: 0, events: 0, snapshots: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [laws, jurisdictions, events, snapshots] = await Promise.all([
          fetchAPI("/ai-laws"),
          fetchAPI("/jurisdictions"),
          fetchAPI("/law-events"),
          fetchAPI("/snapshots"),
        ])
        setStats({
          laws: laws.length,
          jurisdictions: jurisdictions.length,
          events: events.length,
          snapshots: snapshots.length,
        })
      } catch (error) {
        console.error("Dashboard fetch failed:", error)
      } finally {
        setLoading(false)
      }
    }
    loadDashboard()
  }, [])

  return (
    <DashboardLayout>
      <div className="space-y-8 max-w-6xl">
        <div>
          <h2 className="text-2xl font-bold text-[#1a1a1a]">Overview</h2>
          <p className="text-[#6B6860] mt-1 text-sm">
            Real-time monitoring across {stats.jurisdictions} jurisdictions
          </p>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl border border-[#E2E0D8] p-6 h-32 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
            <StatsCard title="Total AI Laws"        value={stats.laws}          icon="⚖️" />
            <StatsCard title="Jurisdictions"        value={stats.jurisdictions} icon="🌍" accent="#1A6B3C" />
            <StatsCard title="Regulatory Events"    value={stats.events}        icon="📋" accent="#7A4F00" />
            <StatsCard title="Snapshots Archived"   value={stats.snapshots}     icon="📸" accent="#5A1A5E" />
          </div>
        )}

        <div className="bg-white rounded-2xl border border-[#E2E0D8] p-6">
          <h3 className="text-sm font-semibold text-[#1a1a1a] mb-1">About this platform</h3>
          <p className="text-sm text-[#6B6860] leading-relaxed">
            AI Law Watchdog monitors official regulatory sources across 9 global jurisdictions — including the EU, UK, US, China, Canada, Singapore, and India — and automatically detects content changes using SHA-256 hashing and intelligent diff analysis. When a meaningful regulatory update is detected, it's recorded as a law event and archived for full audit traceability.
          </p>
        </div>
      </div>
    </DashboardLayout>
  )
}
