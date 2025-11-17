'use client'

import { useState } from 'react'
import { createSession, getUserProfile } from '@/lib/api'

interface WelcomeScreenProps {
  onStart: (userId: string, mode: 'orchestrator' | 'onboarding', sessionId: string) => void
}

export default function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  const [userId, setUserId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleStart = async (mode: 'orchestrator' | 'onboarding') => {
    if (!userId.trim()) {
      setError('Please enter a user ID')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Check if user has profile
      const profile = await getUserProfile(userId)
      
      // If starting onboarding but user already has profile, force orchestrator
      let finalMode = mode
      if (mode === 'onboarding' && profile.has_profile) {
        finalMode = 'orchestrator'
        alert('You have already completed onboarding. Starting general chat.')
      }
      
      // Create session
      const session = await createSession(userId, finalMode)
      
      onStart(userId, finalMode, session.session_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start session')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mb-4">
            <span className="text-6xl">🎓</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Learning Assistant
          </h1>
          <p className="text-gray-600 text-lg">
            Your personalized AI tutor for probability and statistics
          </p>
        </div>

        {/* User ID Input */}
        <div className="mb-6">
          <label htmlFor="userId" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your User ID
          </label>
          <input
            id="userId"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="e.g., student123"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
            disabled={loading}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Mode Selection */}
        <div className="space-y-4 mb-6">
          <div className="text-sm font-medium text-gray-700 mb-2">
            Choose how to start:
          </div>

          {/* Onboarding Option */}
          <button
            onClick={() => handleStart('onboarding')}
            disabled={loading}
            className="w-full p-6 border-2 border-blue-200 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition disabled:opacity-50 disabled:cursor-not-allowed text-left"
          >
            <div className="flex items-start">
              <div className="text-3xl mr-4">📝</div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  Start with Assessment
                </h3>
                <p className="text-gray-600 text-sm">
                  Take a quick adaptive quiz to determine your current knowledge level.
                  We'll personalize your learning experience based on your results.
                </p>
                <div className="mt-2 text-xs text-blue-600 font-medium">
                  Recommended for new users • 5-10 minutes
                </div>
              </div>
            </div>
          </button>

          {/* Orchestrator Option */}
          <button
            onClick={() => handleStart('orchestrator')}
            disabled={loading}
            className="w-full p-6 border-2 border-gray-200 rounded-xl hover:border-gray-400 hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed text-left"
          >
            <div className="flex items-start">
              <div className="text-3xl mr-4">💬</div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  Start Chatting
                </h3>
                <p className="text-gray-600 text-sm">
                  Jump straight into conversation with the learning assistant.
                  Ask questions, get explanations, and explore topics.
                </p>
                <div className="mt-2 text-xs text-gray-600 font-medium">
                  For returning users or exploratory learning
                </div>
              </div>
            </div>
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-4">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Starting session...</p>
          </div>
        )}

        {/* Info Footer */}
        <div className="mt-8 pt-6 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>
            ✨ Powered by AI • Adaptive Learning • Personalized Content
          </p>
        </div>
      </div>
    </div>
  )
}
