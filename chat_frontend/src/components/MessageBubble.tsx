'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { Message } from '@/lib/api'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const agent = message.metadata?.agent
  const isSystemMessage = message.metadata?.isSystemMessage
  const isModeSwitch = message.metadata?.modeSwitch

  // Special styling for system/mode switch messages
  if (isSystemMessage || isModeSwitch) {
    return (
      <div className="flex justify-center my-6 message-enter">
        <div className="max-w-3xl w-full px-6 py-4 rounded-xl bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-200 shadow-lg">
          <div className="prose prose-sm max-w-none text-center">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex]}
              components={{
                hr: () => (
                  <hr className="border-t-2 border-green-300 my-3" />
                ),
                p: ({ children }) => (
                  <p className="text-gray-800 font-medium">{children}</p>
                ),
                strong: ({ children }) => (
                  <strong className="text-green-700 font-bold">{children}</strong>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} message-enter`}
    >
      <div
        className={`max-w-3xl px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-900 shadow-md border border-gray-100'
        }`}
      >
        {/* Agent Badge */}
        {!isUser && agent && (
          <div className="text-xs font-semibold text-blue-600 mb-1">
            {agent === 'OnboardingAgent' ? '📝 Assessment' : '💬 Assistant'}
          </div>
        )}

        {/* Message Content */}
        <div
          className={`prose prose-sm max-w-none ${
            isUser ? 'prose-invert' : ''
          }`}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
            components={{
              // Custom styling for code blocks
              code({ node, inline, className, children, ...props }) {
                return inline ? (
                  <code
                    className={`${
                      isUser ? 'bg-blue-700' : 'bg-gray-100'
                    } px-1 py-0.5 rounded text-sm`}
                    {...props}
                  >
                    {children}
                  </code>
                ) : (
                  <code
                    className={`block ${
                      isUser ? 'bg-blue-700' : 'bg-gray-100'
                    } p-3 rounded-lg text-sm overflow-x-auto`}
                    {...props}
                  >
                    {children}
                  </code>
                )
              },
              // Custom styling for links
              a({ node, children, ...props }) {
                return (
                  <a
                    className={`${
                      isUser ? 'text-blue-200' : 'text-blue-600'
                    } hover:underline`}
                    target="_blank"
                    rel="noopener noreferrer"
                    {...props}
                  >
                    {children}
                  </a>
                )
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Timestamp */}
        <div
          className={`text-xs mt-2 ${
            isUser ? 'text-blue-200' : 'text-gray-500'
          }`}
        >
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>

        {/* Metadata (if quiz question) */}
        {message.metadata?.quiz_active && (
          <div className="mt-2 text-xs text-blue-600 font-medium">
            Quiz in progress...
          </div>
        )}
        {message.metadata?.mode_switched && (
          <div className="mt-2 text-xs text-green-600 font-medium">
            ✓ Switching to general chat mode
          </div>
        )}
      </div>
    </div>
  )
}
