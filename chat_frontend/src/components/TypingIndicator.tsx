'use client'

export default function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-white px-4 py-3 rounded-2xl shadow-md border border-gray-100">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
        </div>
      </div>
    </div>
  )
}
