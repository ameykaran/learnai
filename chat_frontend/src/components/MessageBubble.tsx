'use client'

import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import { Message } from '@/lib/api'
import Image from 'next/image'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const agent = message.metadata?.agent
  const isSystemMessage = message.metadata?.isSystemMessage
  const isModeSwitch = message.metadata?.modeSwitch

  // Extract chart image URLs from message content and clean content
  const [chartUrls, setChartUrls] = useState<string[]>([])
  const [cleanedContent, setCleanedContent] = useState<string>(message.content)
  const [zoomedImageUrl, setZoomedImageUrl] = useState<string | null>(null)
  
  useEffect(() => {
    const urls: string[] = []
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    let content = message.content
    
    // Pattern 1: Extract URLs from markdown links [text](/generated/report_*.png)
    const markdownRegex = /\[.*?\]\((\/(?:generated|public)\/report_.*?\.png)\)/g
    let match
    while ((match = markdownRegex.exec(message.content)) !== null) {
      urls.push(`${apiUrl}${match[1]}`)
      // Remove the markdown link from content
      content = content.replace(match[0], '')
    }
    
    // Pattern 2: Extract standalone URLs /generated/report_*.png or /public/report_*.png
    const standaloneRegex = /^(\/(?:generated|public)\/report_.*?\.png)$/gm
    while ((match = standaloneRegex.exec(message.content)) !== null) {
      const fullUrl = `${apiUrl}${match[1]}`
      // Only add if not already in urls array
      if (!urls.includes(fullUrl)) {
        urls.push(fullUrl)
      }
      // Remove the standalone URL from content
      content = content.replace(match[0], '')
    }

    // Clean up extra blank lines
    content = content.replace(/\n{3,}/g, '\n\n').trim()

    console.log('Extracted chart URLs:', urls)
    console.log('Cleaned content:', content)
    
    setChartUrls(urls)
    setCleanedContent(content)
  }, [message.content])

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
              a({ node, children, href, ...props }) {
                // Check if it's a generated content link (PDF/slides)
                const isGeneratedContent = href?.includes('/generated/') || href?.includes('/public/')
                const isContentFile = href?.match(/\.(pdf|pptx?|docx?)$/i)
                
                // Replace localhost:3001 with localhost:8000 if present
                if (href) {
                  href = href.replace('localhost:3001', 'localhost:8000')
                }

                if (isGeneratedContent && isContentFile) {
                  return (
                    <a
                      href={href}
                      className={`inline-flex items-center gap-2 ${
                        isUser 
                          ? 'bg-blue-500 hover:bg-blue-400 text-white' 
                          : 'bg-blue-600 hover:bg-blue-700 text-white'
                      } px-4 py-2 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all my-2`}
                      target="_blank"
                      rel="noopener noreferrer"
                      {...props}
                    >
                      <span>🔗</span>
                      <span>{children}</span>
                      <span className="text-xs opacity-75">↗</span>
                    </a>
                  )
                }
                
                // Regular links
                return (
                  <a
                    href={href}
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
            {cleanedContent}
          </ReactMarkdown>
        </div>

        {/* Chart Images */}
        {chartUrls.length > 0 && (
          <div className="mt-4 space-y-4">
            <div className="text-xs font-semibold text-blue-600 mb-2 flex items-center gap-2">
              📊 Visual Analytics Dashboard
            </div>
            {chartUrls.map((url, index) => (
              <div 
                key={index} 
                className="relative w-full rounded-lg overflow-hidden border-2 border-blue-200 shadow-lg bg-white hover:shadow-xl transition-shadow cursor-pointer"
                onClick={() => setZoomedImageUrl(url)}
              >
                <img
                  src={url}
                  alt={`Progress Chart ${index + 1}`}
                  className="w-full h-auto"
                  style={{ maxWidth: '100%', height: 'auto' }}
                  onError={(e) => {
                    console.error('Failed to load chart:', url)
                    e.currentTarget.style.display = 'none'
                  }}
                />
                {/* Zoom hint overlay */}
                <div className="absolute inset-0 hover:bg-opacity-10 transition-all flex items-center justify-center">
                  <div className="opacity-80 hover:opacity-100 transition-opacity bg-white/90 px-3 py-1 rounded-full text-xs font-medium text-blue-600">
                    🔍 Click to zoom
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Zoomed Image Modal */}
        {zoomedImageUrl && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
            onClick={() => setZoomedImageUrl(null)}
          >
            <div className="relative max-w-7xl max-h-full">

              {/* Button bar (Close + Download) */}
              <div className="absolute -top-12 right-0 flex items-center gap-3">
                {/* Download button */}
                <a
                  href={zoomedImageUrl} target='_blank'
                  download="progress-dashboard.png"
                  className="bg-white hover:bg-gray-100 px-4 py-2 rounded-full text-sm font-medium text-blue-600 shadow-lg"
                  onClick={(e) => e.stopPropagation()}
                >
                  💾 Download
                </a>

                {/* Close button */}
                <button
                  className="bg-white hover:bg-gray-100 px-4 py-2 rounded-full text-sm font-medium text-blue-600 shadow-lg"
                  onClick={(e) => {
                    e.stopPropagation();
                    setZoomedImageUrl(null);
                  }}
                >
                  ❌ Close
                </button>
              </div>

              {/* Zoomed image */}
              <img
                src={zoomedImageUrl}
                alt="Zoomed Progress Chart"
                className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl"
                onClick={(e) => e.stopPropagation()}
              />
            </div>
          </div>
        )}

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
