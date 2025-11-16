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
              // Custom styling for headers
              h1: ({ node, children, ...props }) => (
                <h1 className={`text-2xl font-bold mb-2 mt-3 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h1>
              ),
              h2: ({ node, children, ...props }) => (
                <h2 className={`text-xl font-bold mb-2 mt-3 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h2>
              ),
              h3: ({ node, children, ...props }) => (
                <h3 className={`text-lg font-bold mb-2 mt-2 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h3>
              ),
              h4: ({ node, children, ...props }) => (
                <h4 className={`text-base font-bold mb-1 mt-2 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h4>
              ),
              h5: ({ node, children, ...props }) => (
                <h5 className={`text-sm font-bold mb-1 mt-2 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h5>
              ),
              h6: ({ node, children, ...props }) => (
                <h6 className={`text-xs font-bold mb-1 mt-2 ${isUser ? 'text-white' : 'text-gray-900'}`} {...props}>
                  {children}
                </h6>
              ),
              // Custom styling for paragraphs
              p: ({ node, children, ...props }) => (
                <p className="mb-2 last:mb-0" {...props}>
                  {children}
                </p>
              ),
              // Custom styling for lists
              ul: ({ node, children, ...props }) => (
                <ul className="list-disc pl-5 mb-2 space-y-1" {...props}>
                  {children}
                </ul>
              ),
              ol: ({ node, children, ...props }) => (
                <ol className="list-decimal pl-5 mb-2 space-y-1" {...props}>
                  {children}
                </ol>
              ),
              // Custom styling for blockquotes
              blockquote: ({ node, children, ...props }) => (
                <blockquote 
                  className={`border-l-4 pl-4 italic my-2 ${
                    isUser ? 'border-blue-300' : 'border-gray-300'
                  }`} 
                  {...props}
                >
                  {children}
                </blockquote>
              ),
              // Custom styling for code blocks
              code({ node, className, children, ...props }: any) {
                const inline = !className?.includes('language-')
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
              // Custom styling for strong/bold
              strong: ({ node, children, ...props }) => (
                <strong className="font-bold" {...props}>
                  {children}
                </strong>
              ),
              // Custom styling for emphasis/italic
              em: ({ node, children, ...props }) => (
                <em className="italic" {...props}>
                  {children}
                </em>
              ),
              // Custom styling for horizontal rules
              hr: ({ node, ...props }) => (
                <hr className={`my-3 ${isUser ? 'border-blue-400' : 'border-gray-300'}`} {...props} />
              ),
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
