'use client'

import { useState } from 'react'
import QuizInterface from '@/components/QuizInterface'

export default function Home() {
  const [quizStarted, setQuizStarted] = useState(false)

  const handleStartQuiz = () => {
    setQuizStarted(true)
  }

  const handleResetQuiz = () => {
    setQuizStarted(false)
  }

  if (quizStarted) {
    return <QuizInterface onReset={handleResetQuiz} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="max-w-2xl mx-auto text-center">
        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
          <div className="mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Probability Quiz
            </h1>
            <p className="text-lg text-gray-600 leading-relaxed">
              Welcome to the Adaptive Probability Assessment! This quiz will help determine your current level of understanding in probability concepts.
            </p>
          </div>

          <div className="bg-blue-50 rounded-lg p-6 mb-8">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">How it works:</h2>
            <div className="text-left space-y-3 text-blue-800">
              <div className="flex items-start">
                <span className="bg-blue-200 text-blue-900 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">1</span>
                <p>Answer 25 multiple-choice questions about probability</p>
              </div>
              <div className="flex items-start">
                <span className="bg-blue-200 text-blue-900 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">2</span>
                <p>Questions adapt to your performance (easy → medium → difficult)</p>
              </div>
              <div className="flex items-start">
                <span className="bg-blue-200 text-blue-900 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">3</span>
                <p>Get classified into Easy, Medium, or Difficult competence level</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <button
              onClick={handleStartQuiz}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 px-8 rounded-lg transition-colors duration-200 text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Start Quiz
            </button>

            <p className="text-sm text-gray-500">
              The quiz will take approximately 10-15 minutes to complete
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-gray-600">
            This assessment covers probability concepts from 7th grade to 12th grade level
          </p>
        </div>
      </div>
    </div>
  )
}
