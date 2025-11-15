'use client'

import { useState, useEffect } from 'react'
import QuestionCard from './QuestionCard'
import ProgressBar from './ProgressBar'
import ResultsCard from './ResultsCard'

interface Question {
  id: number
  question_text: string
  options: {
    A: string
    B: string
    C: string
    D: string
  }
  difficulty: string
  question_number: number
}

interface QuizResults {
  session_id: string
  total_questions: number
  total_correct: number
  overall_accuracy: number
  easy_stats: {
    correct: number
    total: number
    accuracy: number
  }
  medium_stats: {
    correct: number
    total: number
    accuracy: number
  }
  difficult_stats: {
    correct: number
    total: number
    accuracy: number
  }
  final_competence_level: string
  is_completed: boolean
}

interface QuizInterfaceProps {
  onReset: () => void
}

const QuizInterface: React.FC<QuizInterfaceProps> = ({ onReset }) => {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null)
  const [totalQuestions, setTotalQuestions] = useState<number>(25) // Default value
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [results, setResults] = useState<QuizResults | null>(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [lastAnswerCorrect, setLastAnswerCorrect] = useState<boolean | null>(null)
  const [correctAnswer, setCorrectAnswer] = useState<string | null>(null)
  const API_BASE_URL: string = process.env.NEXT_PUBLIC_API_BASE_URL
  useEffect(() => {
    startQuiz()
  }, [])

  const startQuiz = async () => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await fetch(`${API_BASE_URL}/quiz/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      })

      if (!response.ok) {
        throw new Error('Failed to start quiz')
      }

      const data = await response.json()
      setSessionId(data.session_id)
      setCurrentQuestion(data.question)
      if (data.total_questions) {
        setTotalQuestions(data.total_questions)
      }
    } catch (err) {
      setError('Failed to start quiz. Please make sure the backend is running.')
    } finally {
      setIsLoading(false)
    }
  }

  const submitAnswer = async (questionId: number, answer: string) => {
    if (!sessionId) return

    try {
      setIsSubmitting(true)
      setError(null)

      const response = await fetch(`${API_BASE_URL}/quiz/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          question_id: questionId,
          user_answer: answer,
          time_taken: null
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit answer')
      }

      const data = await response.json()

      // Update total questions if provided
      if (data.total_questions) {
        setTotalQuestions(data.total_questions)
      }

      // Show feedback
      setLastAnswerCorrect(data.is_correct)
      setCorrectAnswer(data.correct_answer)
      setShowFeedback(true)

      // Wait 2 seconds then proceed
      setTimeout(() => {
        setShowFeedback(false)
        setLastAnswerCorrect(null)
        setCorrectAnswer(null)

        if (data.is_quiz_complete) {
          setResults(data.results)
          setCurrentQuestion(null)
        } else {
          setCurrentQuestion(data.next_question)
        }
      }, 2000)

    } catch (err) {
      setError('Failed to submit answer')
    } finally {
      setIsSubmitting(false)
    }
  }

  const resetQuiz = async () => {
    if (sessionId) {
      try {
        await fetch(`${API_BASE_URL}/quiz/${sessionId}`, {
          method: 'DELETE',
        })
      } catch (err) {
        console.error('Failed to reset quiz session:', err)
      }
    }
    onReset()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-700">Loading your quiz...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center px-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md mx-auto text-center">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={resetQuiz}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  if (results) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100">
        <ResultsCard results={results} onReset={resetQuiz} />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <ProgressBar
            currentQuestion={currentQuestion?.question_number || 1}
            totalQuestions={totalQuestions}
          />

          {showFeedback ? (
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
              <div className={`text-4xl mb-4 ${lastAnswerCorrect ? 'text-green-500' : 'text-red-500'}`}>
                {lastAnswerCorrect ? '✅' : '❌'}
              </div>
              <h2 className={`text-2xl font-bold mb-2 ${lastAnswerCorrect ? 'text-green-700' : 'text-red-700'}`}>
                {lastAnswerCorrect ? 'Correct!' : 'Incorrect'}
              </h2>
              {!lastAnswerCorrect && (
                <p className="text-gray-600">
                  The correct answer was: <strong>{correctAnswer}</strong>
                </p>
              )}
              <div className="mt-4">
                <div className="animate-pulse text-sm text-gray-500">
                  Loading next question...
                </div>
              </div>
            </div>
          ) : currentQuestion ? (
            <QuestionCard
              question={currentQuestion}
              onSubmit={submitAnswer}
              isSubmitting={isSubmitting}
            />
          ) : (
            <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading...</p>
            </div>
          )}

          <div className="mt-6 text-center">
            <button
              onClick={resetQuiz}
              className="text-gray-600 hover:text-gray-800 underline"
            >
              Exit Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default QuizInterface