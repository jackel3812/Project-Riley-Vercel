import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Brain, Code, Database, GitBranch, Globe, Lightbulb, Mic, Sigma } from "lucide-react"

export default function AboutPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <div className="mr-4 flex items-center space-x-2">
            <Link href="/">
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-primary" />
                <span className="hidden font-bold sm:inline-block">Riley AI</span>
              </div>
            </Link>
          </div>
          <div className="flex flex-1 items-center justify-end space-x-4">
            <nav className="flex items-center space-x-2">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Home
                </Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl">About Riley AI</h1>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  A modular, voice-enabled, web-deployable intelligence engine inspired by J.A.R.V.I.S.
                </p>
              </div>
            </div>
            <div className="mx-auto max-w-3xl space-y-8 py-12">
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Vision & Purpose</h2>
                <p className="text-muted-foreground">
                  Riley is designed to be a self-evolving intelligence platform that generates original theories,
                  inventions, and scientific content. With modular reasoning and simulation capabilities, Riley learns
                  from GitHub, Wikipedia, and user data to continuously improve its knowledge and abilities.
                </p>
              </div>
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Core Modules</h2>
                <div className="grid gap-6 sm:grid-cols-2">
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <Lightbulb className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">Invention Engine</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Generates original scientific or consumer invention concepts with detailed specifications
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <Sigma className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">Equation Solver</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Builds and solves symbolic, physical, and mathematical equations
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <Globe className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">Wiki Researcher</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Pulls and summarizes real-time information from the web and Wikipedia
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <GitBranch className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">GitHub Learning</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Clones public repositories, learns patterns, and evolves code
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <Database className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">Memory Engine</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Stores and retrieves structured AI memory, facts, and user interactions
                    </p>
                  </div>
                  <div className="flex flex-col space-y-2 rounded-lg border p-4">
                    <div className="flex items-center space-x-2">
                      <Code className="h-5 w-5 text-primary" />
                      <h3 className="font-medium">Auto Repair</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Monitors and modifies faulty code autonomously when enabled
                    </p>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Technical Architecture</h2>
                <p className="text-muted-foreground">
                  Riley is built with a Python 3.11 backend using Flask API with a modular package structure. It
                  leverages OpenAI (with fallback to free LLMs like Mistral) for natural language processing. The
                  frontend is developed with Next.js, providing a clean, modern UI with real-time chat and voice
                  capabilities.
                </p>
                <p className="text-muted-foreground">
                  The system is designed for zero-downtime deployment on Vercel with persistent memory using serverless
                  databases or Vercel KV, integrated logs of all user queries, and secure routing via API tokens.
                </p>
              </div>
              <div className="flex justify-center">
                <Link href="/console">
                  <Button size="lg" className="gap-2">
                    <Mic className="h-4 w-4" />
                    Try Riley Now
                  </Button>
                </Link>
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
