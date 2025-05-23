import Link from "next/link"
import { Button } from "@/app/components/ui/button"
import { ArrowLeft, Brain, Code, Database, GitBranch, Globe, Lightbulb, Mic, Sparkles } from "lucide-react"

export default function AboutPage() {
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
            <Link href="/">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Home
              </Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">About Riley AI</h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                  A modular, autonomous intelligence platform designed to evolve and adapt.
                </p>
              </div>
            </div>
            <div className="mx-auto mt-12 max-w-3xl space-y-8">
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Vision & Mission</h2>
                <p>
                  Riley AI is designed as a modular, voice-enabled, web-deployable intelligence engine inspired by
                  fictional AI assistants like J.A.R.V.I.S. Our mission is to create an AI platform that can reason,
                  learn, and interact in real-time while maintaining a focus on user privacy and ethical AI development.
                </p>
              </div>
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Core Capabilities</h2>
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Lightbulb className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Invention Engine</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Generates original scientific or consumer invention concepts with detailed specifications and
                      feasibility analysis.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Database className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Memory System</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Stores and retrieves structured AI memory, facts, and user interactions for personalized
                      experiences.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Globe className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Web Research</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Pulls and summarizes real-time information from the web and Wikipedia to provide up-to-date
                      knowledge.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <GitBranch className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">GitHub Learning</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Clones public repositories, learns patterns, and evolves code to improve its own capabilities.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Multiple Modes</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Switch between different intelligence modes like scientist, engineer, and storyteller for
                      specialized assistance.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Code className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Auto Repair</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Monitors and modifies faulty code autonomously when enabled, improving system reliability.
                    </p>
                  </div>
                  <div className="rounded-lg border p-4">
                    <div className="flex items-center gap-2">
                      <Mic className="h-5 w-5 text-primary" />
                      <h3 className="font-semibold">Voice Interface</h3>
                    </div>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Enables natural voice conversations with Riley for a more intuitive interaction experience.
                    </p>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Technical Architecture</h2>
                <p>
                  Riley is built with a modular architecture that separates concerns and allows for easy extension. The
                  backend is powered by Python with a Flask API, while the frontend uses Next.js for a responsive and
                  modern user interface.
                </p>
                <div className="rounded-lg border p-4 bg-muted">
                  <h3 className="font-semibold mb-2">Backend Stack</h3>
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    <li>Python 3.11 with Flask API</li>
                    <li>Modular package structure for extensibility</li>
                    <li>OpenAI integration with fallback to open-source models</li>
                    <li>SQLite/PostgreSQL for persistent memory</li>
                    <li>RESTful endpoints for various capabilities</li>
                  </ul>
                </div>
                <div className="rounded-lg border p-4 bg-muted">
                  <h3 className="font-semibold mb-2">Frontend Stack</h3>
                  <ul className="list-disc list-inside space-y-1 text-sm">
                    <li>Next.js for server-side rendering and routing</li>
                    <li>React for component-based UI</li>
                    <li>Tailwind CSS for styling</li>
                    <li>Web Speech API for voice input/output</li>
                    <li>Responsive design for all devices</li>
                  </ul>
                </div>
              </div>
              <div className="space-y-4">
                <h2 className="text-2xl font-bold">Future Roadmap</h2>
                <p>
                  Riley is designed to evolve over time. Our roadmap includes expanding the capabilities to include:
                </p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Multimodal inputs (image, audio, video)</li>
                  <li>Advanced reasoning engines for complex problem-solving</li>
                  <li>Collaborative AI capabilities for team environments</li>
                  <li>Expanded autonomous learning from diverse sources</li>
                  <li>AR/VR integration for immersive experiences</li>
                </ul>
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
