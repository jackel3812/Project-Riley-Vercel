"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "../../components/ui/button"
import { Input } from "../../components/ui/input"
import { Label } from "../../components/ui/label"
import { Switch } from "../../components/ui/switch"
import { Textarea } from "../../components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select"
import { ArrowLeft, Brain, Save } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"
import { Separator } from "../../components/ui/separator"
import { toast } from "../hooks/use-toast"

export default function SettingsPage() {
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [defaultMode, setDefaultMode] = useState("assistant")
  const [allowSelfEditing, setAllowSelfEditing] = useState(false)
  const [allowedTools, setAllowedTools] = useState({
    invention: true,
    web_search: true,
    wiki: true,
    github: false,
    equation: true,
    auto_repair: false,
  })
  const [apiKey, setApiKey] = useState("")
  const [databaseUrl, setDatabaseUrl] = useState("")
  const [personality, setPersonality] = useState(
    "Riley is helpful, creative, and knowledgeable. Riley maintains a friendly and professional tone while providing accurate information and assistance.",
  )
  const [userId, setUserId] = useState("user-1") // In a real app, this would come from authentication

  useEffect(() => {
    // Load user settings
    const loadSettings = async () => {
      try {
        // Since the API might not be implemented yet, we'll use default settings
        // In a real app, this would fetch from the API
        /* 
        const response = await fetch(`/api/settings?user_id=${userId}`)
        const settings = await response.json()

        if (settings) {
          setDefaultMode(settings.default_mode || "assistant")
          setVoiceEnabled(settings.voice_enabled || false)
          setAllowSelfEditing(settings.allow_self_editing || false)
          setAllowedTools(settings.allowed_tools || {
            invention: true,
            web_search: true,
            wiki: true,
            github: false,
            equation: true,
            auto_repair: false,
          })
        }
        */

        // Use default settings instead
        const defaultSettings = {
          default_mode: "assistant",
          voice_enabled: true,
          allow_self_editing: false,
          allowed_tools: {
            invention: true,
            web_search: true,
            wiki: true,
            github: false,
            equation: true,
            auto_repair: false,
          },
        }

        setDefaultMode(defaultSettings.default_mode)
        setVoiceEnabled(defaultSettings.voice_enabled)
        setAllowSelfEditing(defaultSettings.allow_self_editing)
        setAllowedTools(defaultSettings.allowed_tools)
      } catch (error) {
        console.error("Error loading settings:", error)
        // Use defaults on error
      }
    }

    loadSettings()
  }, [userId])

  const handleSaveSettings = () => {
    // In a real app, this would save to backend/localStorage
    // Since the API is not implemented, we'll just show a toast
    /*
    fetch(`/api/settings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        default_mode: defaultMode,
        voice_enabled: voiceEnabled,
        allow_self_editing: allowSelfEditing,
        allowed_tools: allowedTools,
        personality: personality,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        toast({
          title: "Settings saved",
          description: "Your preferences have been updated successfully.",
        })
      })
      .catch((error) => {
        console.error("Error saving settings:", error)
        toast({
          title: "Error saving settings",
          description: "There was an error saving your preferences. Please try again.",
        })
      })
    */

    // Just show a success toast for now
    toast({
      title: "Settings saved",
      description: "Your preferences have been updated successfully.",
    })
  }

  const handleToolToggle = (tool: keyof typeof allowedTools) => {
    setAllowedTools((prev) => ({
      ...prev,
      [tool]: !prev[tool],
    }))
  }

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
            <Link href="/console">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Console
              </Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-1 py-6">
        <div className="container">
          <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
            <aside className="lg:w-1/5">
              <div className="sticky top-24">
                <div className="space-y-4">
                  <div className="font-medium">Settings</div>
                  <ul className="space-y-2">
                    <li>
                      <Link href="#general" className="text-muted-foreground hover:text-foreground">
                        General
                      </Link>
                    </li>
                    <li>
                      <Link href="#api" className="text-muted-foreground hover:text-foreground">
                        API & Connections
                      </Link>
                    </li>
                    <li>
                      <Link href="#personality" className="text-muted-foreground hover:text-foreground">
                        Personality
                      </Link>
                    </li>
                    <li>
                      <Link href="#tools" className="text-muted-foreground hover:text-foreground">
                        Tools & Capabilities
                      </Link>
                    </li>
                  </ul>
                </div>
              </div>
            </aside>
            <div className="flex-1 lg:max-w-3xl">
              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-bold tracking-tight">Settings</h3>
                  <p className="text-muted-foreground">
                    Configure Riley AI to match your preferences and requirements.
                  </p>
                </div>
                <Separator />

                <div id="general" className="space-y-4">
                  <h4 className="text-xl font-semibold">General Settings</h4>

                  <Card>
                    <CardHeader>
                      <CardTitle>Voice Interaction</CardTitle>
                      <CardDescription>Enable or disable voice input and output capabilities.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="voice-toggle">Enable Voice</Label>
                        <Switch id="voice-toggle" checked={voiceEnabled} onCheckedChange={setVoiceEnabled} />
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Default Mode</CardTitle>
                      <CardDescription>Set the default operating mode for Riley.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Select value={defaultMode} onValueChange={setDefaultMode}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a mode" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="assistant">Assistant</SelectItem>
                          <SelectItem value="genius">Genius</SelectItem>
                          <SelectItem value="inventor">Inventor</SelectItem>
                          <SelectItem value="explorer">Explorer</SelectItem>
                          <SelectItem value="scientist">Scientist</SelectItem>
                          <SelectItem value="engineer">Engineer</SelectItem>
                          <SelectItem value="storyteller">Storyteller</SelectItem>
                          <SelectItem value="teacher">Teacher</SelectItem>
                        </SelectContent>
                      </Select>
                    </CardContent>
                  </Card>
                </div>

                <Separator />

                <div id="api" className="space-y-4">
                  <h4 className="text-xl font-semibold">API & Connections</h4>

                  <Card>
                    <CardHeader>
                      <CardTitle>API Keys</CardTitle>
                      <CardDescription>Configure API keys for external services.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="openai-key">OpenAI API Key</Label>
                        <Input
                          id="openai-key"
                          type="password"
                          placeholder="sk-..."
                          value={apiKey}
                          onChange={(e) => setApiKey(e.target.value)}
                        />
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Database Connection</CardTitle>
                      <CardDescription>Configure the database for Riley's memory.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <Label htmlFor="database-url">Database URL</Label>
                        <Input
                          id="database-url"
                          placeholder="sqlite:///riley_memory.db or postgres://..."
                          value={databaseUrl}
                          onChange={(e) => setDatabaseUrl(e.target.value)}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <Separator />

                <div id="personality" className="space-y-4">
                  <h4 className="text-xl font-semibold">Personality</h4>

                  <Card>
                    <CardHeader>
                      <CardTitle>Riley's Personality</CardTitle>
                      <CardDescription>Customize how Riley interacts with you.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <Label htmlFor="personality">Personality Description</Label>
                        <Textarea
                          id="personality"
                          placeholder="Describe Riley's personality..."
                          className="min-h-32"
                          value={personality}
                          onChange={(e) => setPersonality(e.target.value)}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <Separator />

                <div id="tools" className="space-y-4">
                  <h4 className="text-xl font-semibold">Tools & Capabilities</h4>

                  <Card>
                    <CardHeader>
                      <CardTitle>Allowed Tools</CardTitle>
                      <CardDescription>Control which tools Riley can access.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="invention-toggle">Invention Generator</Label>
                        <Switch
                          id="invention-toggle"
                          checked={allowedTools.invention}
                          onCheckedChange={() => handleToolToggle("invention")}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="web-search-toggle">Web Search</Label>
                        <Switch
                          id="web-search-toggle"
                          checked={allowedTools.web_search}
                          onCheckedChange={() => handleToolToggle("web_search")}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="wiki-toggle">Wikipedia Research</Label>
                        <Switch
                          id="wiki-toggle"
                          checked={allowedTools.wiki}
                          onCheckedChange={() => handleToolToggle("wiki")}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="github-toggle">GitHub Learning</Label>
                        <Switch
                          id="github-toggle"
                          checked={allowedTools.github}
                          onCheckedChange={() => handleToolToggle("github")}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="equation-toggle">Equation Solver</Label>
                        <Switch
                          id="equation-toggle"
                          checked={allowedTools.equation}
                          onCheckedChange={() => handleToolToggle("equation")}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label htmlFor="auto-repair-toggle">Auto Code Repair</Label>
                        <Switch
                          id="auto-repair-toggle"
                          checked={allowedTools.auto_repair}
                          onCheckedChange={() => handleToolToggle("auto_repair")}
                        />
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Self-Editing</CardTitle>
                      <CardDescription>Allow Riley to autonomously modify its own code.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <div>
                          <Label htmlFor="self-editing-toggle">Allow Self-Editing</Label>
                          <p className="text-sm text-muted-foreground">
                            This is an advanced feature that allows Riley to modify its own code.
                          </p>
                        </div>
                        <Switch
                          id="self-editing-toggle"
                          checked={allowSelfEditing}
                          onCheckedChange={setAllowSelfEditing}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <div className="flex justify-end">
                  <Button onClick={handleSaveSettings} className="gap-2">
                    <Save className="h-4 w-4" />
                    Save Settings
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
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
