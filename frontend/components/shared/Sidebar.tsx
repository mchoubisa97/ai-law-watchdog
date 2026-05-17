"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  Clock3,
  Scale,
  Globe,
  Camera,
  Activity,
} from "lucide-react"

const navItems = [
  { name: "Dashboard",   href: "/dashboard",    icon: LayoutDashboard },
  { name: "Timeline",    href: "/timeline",     icon: Clock3 },
  { name: "AI Laws",     href: "/ai-laws",      icon: Scale },
  { name: "Jurisdictions", href: "/jurisdictions", icon: Globe },
  { name: "Snapshots",   href: "/snapshots",    icon: Camera },
  { name: "Monitoring",  href: "/monitoring",   icon: Activity },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-60 min-h-screen bg-[#1C3F5E] flex flex-col">
      <div className="px-6 py-6 border-b border-white/10">
        <div className="text-white font-bold text-lg leading-tight">AI Law</div>
        <div className="text-white/50 text-xs font-mono tracking-widest uppercase mt-0.5">Watchdog</div>
      </div>

      <nav className="p-3 space-y-0.5 flex-1 mt-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                active
                  ? "bg-white/15 text-white"
                  : "text-white/60 hover:text-white hover:bg-white/8"
              }`}
            >
              <Icon size={16} className={active ? "text-white" : "text-white/50"} />
              {item.name}
            </Link>
          )
        })}
      </nav>

      <div className="px-5 py-4 border-t border-white/10">
        <div className="text-white/30 text-xs font-mono">v1.0.0</div>
      </div>
    </aside>
  )
}
