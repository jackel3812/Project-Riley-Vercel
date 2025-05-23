"use client"

import { useState, useRef, useEffect } from "react"
import Link from "next/link"
import { Button } from "../../components/ui/button"
import { Input } from "../../components/ui/input"
import { Tabs, TabsList, TabsTrigger } from "../../components/ui/tabs"
import { ArrowLeft, Brain, Mic, MicOff, Send, Settings, Sparkles, Calculator, Search, Github, Code } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "../../components/ui/avatar"
import { Card, CardContent } from "../../components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../../components/ui/tooltip"
import { useMobile } from "../hooks/use-mobile"

type Message = {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
  source?: string
  emotion?: string
  style?: string
}

type SpecialAction = {
  type: "invention" | "equation" | "search" | "github" | "repair"
  prompt: string
  result?: any
}

export default function ConsolePage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello, I am Riley. How can I assist you today?",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [currentMode, setCurrentMode] = useState("assistant")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const isMobile = useMobile()
  const [userId, setUserId] = useState("user-1") // In a real app, this would come from authentication

  // Special actions state
  const [specialAction, setSpecialAction] = useState<SpecialAction | null>(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

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
          setCurrentMode(settings.default_mode || "assistant")
          setVoiceEnabled(settings.voice_enabled || false)
        }
        */

        // Use default settings instead
        const defaultSettings = {
          default_mode: "assistant",
          voice_enabled: false,
          allow_self_editing: false,
          allowed_tools: ["invention", "web_search", "wiki"],
        }

        setCurrentMode(defaultSettings.default_mode)
        setVoiceEnabled(defaultSettings.voice_enabled)
      } catch (error) {
        console.error("Error loading settings:", error)
        // Use defaults on error
        setCurrentMode("assistant")
        setVoiceEnabled(false)
      }
    }

    loadSettings()
  }, [userId])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      // Detect if this is a special action
      const actionTypes = {
        invention: /^(create|invent|design|generate)\s+.*(invention|product|device|gadget)/i,
        equation: /^(solve|calculate|compute|equation)\s+.*(equation|formula|expression)/i,
        search: /^(search|find|lookup|research)\s+/i,
        github: /^(analyze|clone|learn from)\s+.*(github|repo|repository)/i,
        repair: /^(fix|repair|debug|improve)\s+.*(code|function|method)/i,
      }

      let actionType: SpecialAction["type"] | null = null

      for (const [type, regex] of Object.entries(actionTypes)) {
        if (regex.test(input)) {
          actionType = type as SpecialAction["type"]
          break
        }
      }

      let endpoint = "/api/chat"
      let payload: any = {
        user_id: userId,
        message: input,
        mode: currentMode,
      }

      if (actionType) {
        switch (actionType) {
          case "invention":
            endpoint = "/api/invent"
            payload = {
              user_id: userId,
              prompt: input,
              field: "general",
            }
            break
          case "equation":
            // This would be handled by the reasoning engine in chat
            break
          case "search":
            endpoint = "/api/search"
            payload = {
              user_id: userId,
              query: input.replace(/^(search|find|lookup|research)\s+/i, ""),
            }
            break
          case "github":
            endpoint = "/api/github"
            const repoUrlMatch = input.match(/(https:\/\/github\.com\/[^\s]+)/i)
            payload = {
              user_id: userId,
              repo_url: repoUrlMatch ? repoUrlMatch[1] : input,
            }
            break
          case "repair":
            endpoint = "/api/repair"
            // Extract code block if present
            const codeMatch = input.match(/```([\s\S]*?)```/m)
            payload = {
              user_id: userId,
              code: codeMatch ? codeMatch[1] : input,
            }
            break
        }

        setSpecialAction({
          type: actionType,
          prompt: input,
        })
      }

      // In a real app, this would call the actual API
      // For now, we'll simulate a response
      setTimeout(() => {
        let responseContent = ""
        let source = ""
        let emotion = "neutral"
        let style = "neutral"

        if (actionType) {
          switch (actionType) {
            case "invention":
              responseContent = `Here's an invention concept based on your request:

**Quantum Resonance Fabric (QRF)**

A smart textile material that uses quantum entanglement principles to:
1. Adapt its thermal properties based on body temperature and environmental conditions
2. Generate small amounts of electricity from movement and temperature differentials
3. Change color and pattern based on user preferences or environmental stimuli
4. Provide haptic feedback through microscopic vibrations

This could revolutionize clothing, medical textiles, and smart home furnishings.`
              source = "invention_engine"
              emotion = "enthusiastic"
              style = "enthusiastic"
              break
            case "search":
              responseContent = `Here's what I found about "${payload.query}":

According to recent sources, this topic has seen significant developments in the past year. The main points are:

1. New research published in Science journal shows promising results
2. Several companies have launched innovative products in this space
3. Experts predict continued growth and evolution in this field

Would you like me to explore any specific aspect in more detail?`
              source = "wiki_researcher"
              emotion = "analytical"
              style = "analytical"
              break
            case "github":
              responseContent = `I've analyzed the repository and found:

**Repository Structure:**
- 45 Python files
- 12 JavaScript files
- 3 main directories: src, tests, docs

**Key Patterns:**
1. Factory design pattern used extensively
2. Dependency injection for service components
3. Comprehensive test coverage (87%)

**Learning Opportunities:**
- The error handling approach is particularly elegant
- The project uses an interesting approach to configuration management
- CI/CD pipeline implementation is worth studying

Would you like me to focus on any specific aspect of the codebase?`
              source = "github_learning"
              emotion = "analytical"
              style = "analytical"
              break
            case "repair":
              responseContent = `I've analyzed and repaired the code:

\`\`\`python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0  # Return 0 for empty lists instead of raising an error
    
    total = sum(numbers)
    return total / len(numbers)
\`\`\`

Changes made:
1. Added proper docstring
2. Added handling for empty lists
3. Improved variable naming
4. Simplified the calculation logic

The code now handles edge cases properly and follows best practices.`
              source = "auto_repair"
              emotion = "analytical"
              style = "analytical"
              break
            default:
              responseContent = `I'm currently in ${currentMode} mode. Based on your question, I think I can help with that.

The approach I would recommend is to start by breaking down the problem into smaller components. This allows us to tackle each part systematically.

Is there a specific aspect you'd like me to elaborate on further?`
              source = "reasoning_engine"
              emotion = "neutral"
              style = "neutral"
          }
        } else {
          // Regular chat response
          responseContent = `I'm currently in ${currentMode} mode. Based on your question, I think I can help with that.

The approach I would recommend is to start by breaking down the problem into smaller components. This allows us to tackle each part systematically.

Is there a specific aspect you'd like me to elaborate on further?`
          source = "reasoning_engine"

          // Adjust emotion based on mode
          if (currentMode === "assistant" || currentMode === "teacher") {
            emotion = "empathetic"
            style = "empathetic"
          } else if (currentMode === "genius" || currentMode === "scientist") {
            emotion = "analytical"
            style = "analytical"
          } else if (currentMode === "inventor" || currentMode === "explorer") {
            emotion = "enthusiastic"
            style = "enthusiastic"
          } else if (currentMode === "storyteller") {
            emotion = "engaging"
            style = "engaging"
          }
        }

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: responseContent,
          timestamp: new Date(),
          source: source,
          emotion: emotion,
          style: style,
        }

        setMessages((prev) => [...prev, assistantMessage])
        setIsLoading(false)
        setSpecialAction(null)

        // Text-to-speech if voice is enabled
        if (voiceEnabled && "speechSynthesis" in window) {
          const speech = new SpeechSynthesisUtterance(responseContent)
          window.speechSynthesis.speak(speech)
        }
      }, 2000)
    } catch (error) {
      console.error("Error sending message:", error)

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I apologize, but I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, errorMessage])
      setIsLoading(false)
      setSpecialAction(null)
    }
  }

  const toggleVoice = () => {
    setVoiceEnabled(!voiceEnabled)

    if (!voiceEnabled && "webkitSpeechRecognition" in window) {
      // This is just a mock for the UI, actual implementation would use the Web Speech API
      alert("Voice recognition would be initialized here")
    } else if (voiceEnabled && "speechSynthesis" in window) {
      window.speechSynthesis.cancel()
    }

    // Save the voice setting - commented out since API is not implemented
    /*
    fetch(`/api/settings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        voice_enabled: !voiceEnabled,
      }),
    }).catch((error) => {
      console.error("Error saving voice setting:", error)
    })
    */
  }

  const toggleListening = () => {
    if (!voiceEnabled) return

    setIsListening(!isListening)

    if (!isListening) {
      // Mock voice recognition
      setTimeout(() => {
        setInput("What can you tell me about quantum computing?")
        setIsListening(false)
      }, 3000)
    }
  }

  const handleModeChange = (mode: string) => {
    setCurrentMode(mode)

    const modeMessage: Message = {
      id: Date.now().toString(),
      role: "assistant",
      content: `I've switched to ${mode} mode. How can I assist you?`,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, modeMessage])

    // Save the mode setting - commented out since API is not implemented
    /*
    fetch(`/api/settings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        default_mode: mode,
      }),
    }).catch((error) => {
      console.error("Error saving mode setting:", error)
    })
    */
  }

  // Function to get style class based on message style
  const getStyleClass = (style: string | undefined) => {
    switch (style) {
      case "empathetic":
        return "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
      case "calming":
        return "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800"
      case "enthusiastic":
        return "bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800"
      case "analytical":
        return "bg-gray-50 dark:bg-gray-800/40 border-gray-200 dark:border-gray-700"
      case "comforting":
        return "bg-pink-50 dark:bg-pink-900/20 border-pink-200 dark:border-pink-800"
      case "joyful":
        return "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800"
      case "engaging":
        return "bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800"
      default:
        return ""
    }
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
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={toggleVoice}
                    className={voiceEnabled ? "bg-primary text-primary-foreground hover:bg-primary/90" : ""}
                  >
                    {voiceEnabled ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>{voiceEnabled ? "Disable Voice" : "Enable Voice"}</TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <Link href="/settings">
              <Button variant="ghost" size="icon">
                <Settings className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                {isMobile ? "" : "Back to Home"}
              </Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-1 flex flex-col">
        <div className="container flex-1 flex flex-col">
          <Tabs defaultValue={currentMode} className="w-full mt-4" onValueChange={handleModeChange}>
            <TabsList className="grid grid-cols-4 md:grid-cols-8">
              <TabsTrigger value="assistant">Assistant</TabsTrigger>
              <TabsTrigger value="genius">Genius</TabsTrigger>
              <TabsTrigger value="inventor">Inventor</TabsTrigger>
              <TabsTrigger value="explorer">Explorer</TabsTrigger>
              {!isMobile && (
                <>
                  <TabsTrigger value="scientist">Scientist</TabsTrigger>
                  <TabsTrigger value="engineer">Engineer</TabsTrigger>
                  <TabsTrigger value="storyteller">Storyteller</TabsTrigger>
                  <TabsTrigger value="teacher">Teacher</TabsTrigger>
                </>
              )}
            </TabsList>
          </Tabs>

          <div className="flex-1 overflow-y-auto py-4 px-2 md:px-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"} message-appear`}
              >
                <div
                  className={`flex ${message.role === "user" ? "flex-row-reverse" : "flex-row"} max-w-[80%] md:max-w-[70%] gap-2`}
                >
                  {message.role === "assistant" && (
                    <Avatar className="h-8 w-8 mt-1">
                      <AvatarImage src="/placeholder.svg?height=32&width=32" alt="Riley" />
                      <AvatarFallback>RA</AvatarFallback>
                    </Avatar>
                  )}
                  <Card
                    className={`${message.role === "user" ? "bg-primary text-primary-foreground" : ""} 
                              ${message.role === "assistant" ? getStyleClass(message.style) : ""}`}
                  >
                    <CardContent className="p-3 text-sm md:text-base whitespace-pre-wrap">
                      {message.content}
                      {message.source && <div className="mt-2 text-xs opacity-70">Source: {message.source}</div>}
                      {message.emotion && message.role === "assistant" && (
                        <div className="mt-1 text-xs opacity-50 italic">Emotional tone: {message.emotion}</div>
                      )}
                    </CardContent>
                  </Card>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start message-appear">
                <div className="flex flex-row max-w-[80%] md:max-w-[70%] gap-2">
                  <Avatar className="h-8 w-8 mt-1">
                    <AvatarImage src="/placeholder.svg?height=32&width=32" alt="Riley" />
                    <AvatarFallback>RA</AvatarFallback>
                  </Avatar>
                  <Card>
                    <CardContent className="p-3">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}

            {specialAction && (
              <div className="flex justify-center message-appear">
                <Card className="w-full max-w-md bg-muted">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      {specialAction.type === "invention" && <Sparkles className="h-5 w-5 text-primary" />}
                      {specialAction.type === "equation" && <Calculator className="h-5 w-5 text-primary" />}
                      {specialAction.type === "search" && <Search className="h-5 w-5 text-primary" />}
                      {specialAction.type === "github" && <Github className="h-5 w-5 text-primary" />}
                      {specialAction.type === "repair" && <Code className="h-5 w-5 text-primary" />}
                      <span className="font-medium capitalize">{specialAction.type} Request</span>
                    </div>
                    <p className="text-sm text-muted-foreground">Processing your {specialAction.type} request...</p>
                  </CardContent>
                </Card>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="sticky bottom-0 py-4 bg-background">
            <div className="flex gap-2">
              {voiceEnabled && (
                <Button
                  variant={isListening ? "destructive" : "outline"}
                  size="icon"
                  onClick={toggleListening}
                  className={isListening ? "animate-pulse" : ""}
                >
                  <Mic className="h-4 w-4" />
                </Button>
              )}
              <Input
                placeholder="Type your message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                className="flex-1"
              />
              <Button onClick={handleSendMessage} disabled={!input.trim() || isLoading}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <div className="mt-2 text-xs text-center text-muted-foreground">
              Riley is in <span className="font-medium capitalize">{currentMode}</span> mode
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
