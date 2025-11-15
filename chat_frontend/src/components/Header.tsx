'use client'

interface HeaderProps {
  mode: 'orchestrator' | 'onboarding'
  userId: string
  connected: boolean
  sessionInfo: any
  onEndSession: () => void
}

export default function Header({
  mode,
  userId,
  connected,
  sessionInfo,
  onEndSession,
}: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Left: Title and Mode */}
          <div className="flex items-center space-x-4">
            <div className="text-2xl">🎓</div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Learning Assistant
              </h1>
              <div className="flex items-center space-x-2 text-sm">
                <span className="text-gray-500">User: {userId}</span>
                <span className="text-gray-300">•</span>
                <span className={`font-medium ${
                  mode === 'onboarding' 
                    ? 'text-blue-600' 
                    : 'text-purple-600'
                }`}>
                  {mode === 'onboarding' ? '📝 Assessment Mode' : '💬 Chat Mode'}
                </span>
              </div>
            </div>
          </div>

          {/* Right: Status and Actions */}
          <div className="flex items-center space-x-4">
            {/* Connection Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                connected ? 'bg-green-500' : 'bg-red-500'
              }`} />
              <span className="text-sm text-gray-600">
                {connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>

            {/* Session Info */}
            {sessionInfo && (
              <div className="text-sm text-gray-600">
                {sessionInfo.has_profile && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full bg-green-100 text-green-800">
                    ✓ Profile Complete
                  </span>
                )}
              </div>
            )}

            {/* End Session Button */}
            <button
              onClick={onEndSession}
              className="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition"
            >
              End Session
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
