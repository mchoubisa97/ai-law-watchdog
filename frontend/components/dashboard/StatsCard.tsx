type StatsCardProps = {
  title: string
  value: number
  icon?: string
  accent?: string
}

export default function StatsCard({ title, value, icon, accent = "#1C3F5E" }: StatsCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E0D8] p-6 shadow-sm hover:shadow-md transition-shadow">
      {icon && (
        <div className="text-2xl mb-3">{icon}</div>
      )}
      <p className="text-xs font-mono text-[#6B6860] uppercase tracking-widest">{title}</p>
      <p className="text-4xl font-bold mt-2" style={{ color: accent }}>
        {value.toLocaleString()}
      </p>
    </div>
  )
}
