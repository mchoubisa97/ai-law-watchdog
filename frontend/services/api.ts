const BASE_URL = "http://localhost:8000"

export async function fetchAPI(path: string) {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) throw new Error(`API error: ${res.status} ${path}`)
  return res.json()
}

export async function getCrawlerRuns(status?: string) {
  const url = status
    ? `/crawler-runs?status=${status}`
    : `/crawler-runs`
  return fetchAPI(url)
}

export async function triggerCrawlers() {
  const res = await fetch(`${BASE_URL}/run-crawlers`, { method: "POST" })
  if (!res.ok) throw new Error(`Failed to trigger crawlers: ${res.status}`)
  return res.json()
}
