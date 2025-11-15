'use client'

import { useEffect, useState } from 'react'
import ChatInterface from '@/components/ChatInterface'
import WelcomeScreen from '@/components/WelcomeScreen'

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  const [mode, setMode] = useState<'orchestrator' | 'onboarding'>('orchestrator')

  return (
    <main className="h-screen w-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {!sessionId ? (
        <WelcomeScreen
          onStart={(userId, mode, sessionId) => {
            setUserId(userId)
            setMode(mode)
            setSessionId(sessionId)
          }}
        />
      ) : (
        <ChatInterface
          sessionId={sessionId}
          userId={userId!}
          initialMode={mode}
          onEndSession={() => {
            setSessionId(null)
            setUserId(null)
          }}
        />
      )}
    </main>
  )
}
