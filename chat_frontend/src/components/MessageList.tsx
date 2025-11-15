'use client'

import { useEffect, useRef } from 'react'
import { Message } from '@/lib/api'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

interface MessageListProps {
  messages: Message[]
  isTyping: boolean
  mode: 'orchestrator' | 'onboarding'
}

export default function MessageList({ messages, isTyping, mode }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  return (
    <div
      ref={containerRef}
      className="h-full overflow-y-auto px-4 py-6"
      style={{ scrollbarGutter: 'stable' }}
    >
      <div className="max-w-4xl mx-auto space-y-4">
        {messages.length === 0 && !isTyping && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">
              {mode === 'onboarding' ? '📝' : '💬'}
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {mode === 'onboarding' 
                ? 'Ready for Your Assessment?' 
                : 'Start a Conversation'}
            </h2>
            <p className="text-gray-600">
              {mode === 'onboarding'
                ? 'Type "start" to begin your adaptive assessment'
                : 'Ask me anything about probability and statistics!'}
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}

        {isTyping && <TypingIndicator />}

        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}
