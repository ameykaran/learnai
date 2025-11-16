'use client'

import { useState, useEffect, useRef } from 'react'
import { Message, createWebSocket, sendWebSocketMessage, getSessionInfo } from '@/lib/api'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import Header from './Header'

interface ChatInterfaceProps {
  sessionId: string
  userId: string
  initialMode: 'orchestrator' | 'onboarding'
  onEndSession: () => void
}

export default function ChatInterface({
  sessionId,
  userId,
  initialMode,
  onEndSession,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [mode, setMode] = useState<'orchestrator' | 'onboarding'>(initialMode)
  const [isTyping, setIsTyping] = useState(false)
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionInfo, setSessionInfo] = useState<any>(null)
  
  const wsRef = useRef<WebSocket | null>(null)

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = createWebSocket(
      sessionId,
      handleWebSocketMessage,
      handleWebSocketError,
      handleWebSocketClose
    )

    wsRef.current = ws

    // Fetch session info
    fetchSessionInfo()

    // Cleanup on unmount
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [sessionId])

  const fetchSessionInfo = async () => {
    try {
      const info = await getSessionInfo(sessionId)
      setSessionInfo(info)
    } catch (err) {
      console.error('Failed to fetch session info:', err)
    }
  }

  const handleWebSocketMessage = (data: any) => {
    let parts = [];
    if (data.content) parts = data.content.split("---").filter(part => part.trim() !== "");
    console.log("Received parts:", parts);
    switch (data.type) {
      case 'connected':
        setConnected(true)
        setError(null)
        // Send initial greeting based on mode
        if (mode === 'onboarding') {
          addMessage('assistant', '👋 Welcome to your adaptive assessment! I\'ll ask you a series of questions to understand your current knowledge level. Ready to start?', {
            agent: 'OnboardingAgent'
          })
        } else {
          addMessage('assistant', '👋 Hello! I\'m your learning assistant. I can help you with probability and statistics. What would you like to learn today?', {
            agent: 'Orchestrator'
          })
        }
        break

      case 'message':
        setIsTyping(false)

        parts.forEach(part => {
          addMessage(data.role, part, data.metadata);
        });

        // Check if mode switched (onboarding complete)
        if (data.metadata?.mode_switched) {
          // Add a system message about mode switch
          addMessage('assistant', '---\n\n🎉 **Assessment Complete!** Your learning profile has been created.\n\nYou can now ask me questions about probability and statistics, and I\'ll personalize my responses based on your knowledge level.\n\n---', {
            agent: 'System',
            isSystemMessage: true,
            modeSwitch: true
          })
          setMode('orchestrator')
          fetchSessionInfo()
        }
        break

      case 'tool_message':
        // Intermediate message from tool execution
        // Typing state is managed by typing/typing_off messages
        
        parts.forEach(part => {
          addMessage(data.role, part, data.metadata);
        });

        // Check if mode switched (onboarding complete)
        if (data.metadata?.mode_switched) {
          // Add a system message about mode switch
          setTimeout(() => {
            addMessage('assistant', '---\n\n🎉 **Assessment Complete!** Your learning profile has been created.\n\nYou can now ask me questions about probability and statistics, and I\'ll personalize my responses based on your knowledge level.\n\n---', {
              agent: 'System',
              isSystemMessage: true,
              modeSwitch: true
            })
          }, 500)
          setMode('orchestrator')
          fetchSessionInfo()
        }
        break

      case 'done':
        // All tool messages sent, clear typing indicator
        setIsTyping(false)
        break

      case 'typing':
        setIsTyping(true)
        break

      case 'typing_off':
        setIsTyping(false)
        break

      case 'error':
        setIsTyping(false)
        setError(data.message)
        break

      default:
        console.log('Unknown message type:', data.type)
    }
  }

  const handleWebSocketError = (error: Event) => {
    setError('Connection error. Please try again.')
    setConnected(false)
  }

  const handleWebSocketClose = () => {
    setConnected(false)
  }

  const addMessage = (role: 'user' | 'assistant', content: string, metadata?: any) => {
    const message: Message = {
      role,
      content,
      timestamp: new Date().toISOString(),
      metadata,
    }
    setMessages((prev) => [...prev, message])
  }

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || !connected) return

    // Add user message immediately
    addMessage('user', text)

    // Send via WebSocket
    try {
      sendWebSocketMessage(wsRef.current!, text)
      setIsTyping(true)
      setError(null)
    } catch (err) {
      setError('Failed to send message. Please try again.')
      setIsTyping(false)
    }
  }

  const handleEndSession = () => {
    if (wsRef.current) {
      wsRef.current.close()
    }
    onEndSession()
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <Header
        mode={mode}
        userId={userId}
        connected={connected}
        sessionInfo={sessionInfo}
        onEndSession={handleEndSession}
      />

      {/* Error Banner */}
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mx-4 mt-4 rounded">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} isTyping={isTyping} mode={mode} />
      </div>

      {/* Input */}
      <MessageInput
        onSend={handleSendMessage}
        disabled={!connected || isTyping}
        mode={mode}
      />
    </div>
  )
}
