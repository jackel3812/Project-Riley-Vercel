"use client"

import * as React from "react"

type ToastProps = {
  title: string
  description?: string
  type?: "default" | "success" | "error" | "warning"
  duration?: number
}

type Toast = ToastProps & {
  id: string
  visible: boolean
}

type ToastContextType = {
  toasts: Toast[]
  toast: (props: ToastProps) => void
  dismissToast: (id: string) => void
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<Toast[]>([])

  const toast = React.useCallback((props: ToastProps) => {
    const id = Math.random().toString(36).substring(2, 9)
    const newToast: Toast = {
      id,
      visible: true,
      duration: 5000,
      type: "default",
      ...props,
    }

    setToasts((prevToasts) => [...prevToasts, newToast])

    if (props.duration !== Number.POSITIVE_INFINITY) {
      setTimeout(() => {
        setToasts((prevToasts) => prevToasts.map((t) => (t.id === id ? { ...t, visible: false } : t)))

        // Remove from DOM after animation
        setTimeout(() => {
          setToasts((prevToasts) => prevToasts.filter((t) => t.id !== id))
        }, 300)
      }, props.duration || 5000)
    }
  }, [])

  const dismissToast = React.useCallback((id: string) => {
    setToasts((prevToasts) => prevToasts.map((t) => (t.id === id ? { ...t, visible: false } : t)))

    // Remove from DOM after animation
    setTimeout(() => {
      setToasts((prevToasts) => prevToasts.filter((t) => t.id !== id))
    }, 300)
  }, [])

  return <ToastContext.Provider value={{ toasts, toast, dismissToast }}>{children}</ToastContext.Provider>
}

export function useToast() {
  const context = React.useContext(ToastContext)
  if (context === undefined) {
    throw new Error("useToast must be used within a ToastProvider")
  }
  return context
}

// Export toast function directly for easier imports
export const toast = (props: ToastProps) => {
  // This is a simple implementation for direct usage
  // In a real app, this would use the context
  const toastContainer = document.getElementById("toast-container")
  if (!toastContainer) {
    const container = document.createElement("div")
    container.id = "toast-container"
    container.style.position = "fixed"
    container.style.top = "1rem"
    container.style.right = "1rem"
    container.style.zIndex = "9999"
    document.body.appendChild(container)
  }

  const id = Math.random().toString(36).substring(2, 9)
  const toast = document.createElement("div")
  toast.id = `toast-${id}`
  toast.style.backgroundColor = "white"
  toast.style.color = "black"
  toast.style.padding = "1rem"
  toast.style.borderRadius = "0.5rem"
  toast.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)"
  toast.style.marginBottom = "0.5rem"
  toast.style.transition = "all 0.3s ease"

  const title = document.createElement("div")
  title.style.fontWeight = "bold"
  title.textContent = props.title
  toast.appendChild(title)

  if (props.description) {
    const description = document.createElement("div")
    description.style.fontSize = "0.875rem"
    description.textContent = props.description
    toast.appendChild(description)
  }

  document.getElementById("toast-container")?.appendChild(toast)

  setTimeout(() => {
    toast.style.opacity = "0"
    setTimeout(() => {
      toast.remove()
    }, 300)
  }, props.duration || 5000)
}
