'use client'

import { useState, useRef, useEffect } from 'react'

interface MessageInputProps {
  onSend: (message: string) => void
  disabled: boolean
  mode: 'orchestrator' | 'onboarding'
}

export default function MessageInput({ onSend, disabled, mode }: MessageInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  // Placeholder text based on mode
  const placeholder = mode === 'onboarding'
    ? 'Type your answer or "start" to begin...'
    : 'Ask a question or request help...'

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex items-end space-x-4">
          {/* Text Input */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={disabled}
              rows={1}
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none max-h-40 disabled:bg-gray-100 disabled:cursor-not-allowed transition"
            />
            
            {/* Character Count */}
            {input.length > 0 && (
              <div className="absolute bottom-2 right-12 text-xs text-gray-400">
                {input.length}
              </div>
            )}
          </div>

          {/* Send Button */}
          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-2xl font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition flex items-center space-x-2"
          >
            <span>Send</span>
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </form>

        {/* Hints */}
        <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
          <div>
            {mode === 'onboarding' ? (
              <span>🔒 Assessment Mode • Answer honestly for best results</span>
            ) : (
              <span>💡 Tip: You can ask for explanations, examples, or practice problems</span>
            )}
          </div>
          <div>
            <kbd className="px-2 py-1 bg-gray-100 rounded">Enter</kbd> to send •{' '}
            <kbd className="px-2 py-1 bg-gray-100 rounded">Shift+Enter</kbd> for new line
          </div>
        </div>
      </div>
    </div>
  )
}
