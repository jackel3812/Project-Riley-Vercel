import Link from "next/link"
import { Button } from "@/app/components/ui/button"
import { ArrowRight, Brain, Code, Database, GitBranch, Globe, Lightbulb, Mic, Sparkles } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <div className="mr-4 flex items-center space-x-2">
            <Link href="/">
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-primary" />
                <span className="font-bold">Riley AI</span>
              </div>
            </Link>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-4">
            <nav className="flex items-center space-x-2">
              <Link href="/about">
                <Button variant="ghost" size="sm">
                  About
                </Button>
              </Link>
              <Link href="/console">
                <Button variant="ghost" size="sm">
                  Console
                </Button>
              </Link>
              <Link href="/settings">
                <Button variant="ghost" size="sm">
                  Settings
                </Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                  Meet Riley, Your Modular AI Assistant
                </h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                  A voice-enabled, web-deployable intelligence engine with autonomous features and reasoning engines.
                </p>
              </div>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Link href="/console">
                  <Button size="lg" className="gap-2">
                    <Mic className="h-4 w-4" />
                    Try Riley Now
                  </Button>
                </Link>
                <Link href="/about">
                  <Button size="lg" variant="outline" className="gap-2">
                    <ArrowRight className="h-4 w-4" />
                    Learn More
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 bg-muted">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Key Features</h2>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                  Riley combines multiple AI capabilities into a single, modular platform.
                </p>
              </div>
              <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <Lightbulb className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">Invention Engine</h3>
                  <p className="text-muted-foreground">
                    Generates original scientific or consumer invention concepts with detailed specifications.
                  </p>
                </div>
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <Globe className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">Web Research</h3>
                  <p className="text-muted-foreground">
                    Pulls and summarizes real-time information from the web and Wikipedia.
                  </p>
                </div>
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <GitBranch className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">GitHub Learning</h3>
                  <p className="text-muted-foreground">
                    Clones public repositories, learns patterns, and evolves code.
                  </p>
                </div>
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <Database className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">Memory Engine</h3>
                  <p className="text-muted-foreground">
                    Stores and retrieves structured AI memory, facts, and user interactions.
                  </p>
                </div>
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <Sparkles className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">Multiple Modes</h3>
                  <p className="text-muted-foreground">
                    Switch between different intelligence modes like scientist, engineer, and storyteller.
                  </p>
                </div>
                <div className="flex flex-col items-center space-y-2 rounded-lg border p-4">
                  <div className="rounded-full bg-primary p-2 text-primary-foreground">
                    <Code className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold">Auto Repair</h3>
                  <p className="text-muted-foreground">Monitors and modifies faulty code autonomously when enabled.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full border-t py-6">
        <div className="container flex flex-col items-center justify-center gap-4 md:flex-row md:gap-8">
          <p className="text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} Riley AI. All rights reserved.
          </p>
          <div className="flex gap-4">
            <Link href="/terms" className="text-sm text-muted-foreground underline-offset-4 hover:underline">
              Terms
            </Link>
            <Link href="/privacy" className="text-sm text-muted-foreground underline-offset-4 hover:underline">
              Privacy
            </Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
