"use client"

import { usePathname } from "next/navigation"

const titles: Record<string, string> = {
  "/dashboard":    "Dashboard",
  "/timeline":     "Regulatory Timeline",
  "/ai-laws":      "AI Laws",
  "/jurisdictions": "Jurisdictions",
  "/snapshots":    "Snapshots",
  "/monitoring":   "Crawler Monitoring",
}

export default function Navbar() {
  const pathname = usePathname()
  const title = titles[pathname] ?? "AI Law Watchdog"

  return (
    <header className="bg-white border-b border-[#E2E0D8] px-8 py-4 flex items-center justify-between">
      <h1 className="text-base font-semibold text-[#1a1a1a]">{title}</h1>
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        <span className="text-xs text-[#6B6860] font-mono">Live Monitoring</span>
      </div>
    </header>
  )
}
