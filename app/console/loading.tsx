import { Brain } from "lucide-react"

export default function Loading() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <div className="flex flex-col items-center justify-center gap-4">
        <div className="animate-pulse">
          <Brain className="h-16 w-16 text-primary" />
        </div>
        <h1 className="text-2xl font-bold">Loading Riley AI...</h1>
        <div className="h-2 w-40 rounded-full bg-muted">
          <div className="h-2 animate-progress rounded-full bg-primary"></div>
        </div>
      </div>
    </div>
  )
}
