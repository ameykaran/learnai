'use client'

import { useState } from 'react'

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

interface QuestionCardProps {
  question: Question
  onSubmit: (questionId: number, answer: string) => void
  isSubmitting: boolean
}

const QuestionCard: React.FC<QuestionCardProps> = ({ question, onSubmit, isSubmitting }) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)

  const handleSubmit = () => {
    if (selectedAnswer) {
      onSubmit(question.id, selectedAnswer)
      setSelectedAnswer(null) // Reset for next question
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'difficult':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
              Question {question.question_number}/{process.env.NEXT_PUBLIC_ONBOARDING_QUESTIONS}
            </span>
            {/* <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getDifficultyColor(question.difficulty)}`}>
              {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
            </span> */}
          </div>
        </div>

        <h2 className="text-xl md:text-2xl font-semibold text-gray-900 leading-relaxed">
          {question.question_text}
        </h2>
      </div>

      <div className="space-y-3 mb-8">
        {Object.entries(question.options).map(([key, value]) => (
          <button
            key={key}
            onClick={() => setSelectedAnswer(key)}
            className={`w-full text-left p-4 rounded-lg border-2 transition-all duration-200 ${
              selectedAnswer === key
                ? 'border-indigo-500 bg-indigo-50 text-indigo-900'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            } ${isSubmitting ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
            disabled={isSubmitting}
          >
            <div className="flex items-start">
              <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full border-2 text-sm font-semibold mr-3 ${
                selectedAnswer === key
                  ? 'border-indigo-500 bg-indigo-500 text-white'
                  : 'border-gray-300 text-gray-600'
              }`}>
                {key}
              </span>
              <span className={`flex-1 pt-1 ${selectedAnswer === key ? 'text-indigo-900' : 'text-gray-700'}`}>
                {value}
              </span>
            </div>
          </button>
        ))}
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleSubmit}
          disabled={!selectedAnswer || isSubmitting}
          className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
            selectedAnswer && !isSubmitting
              ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {isSubmitting ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Submitting...
            </div>
          ) : (
            'Submit Answer'
          )}
        </button>
      </div>

      {!selectedAnswer && (
        <p className="text-center text-gray-500 text-sm mt-4">
          Please select an answer to continue
        </p>
      )}
    </div>
  )
}

export default QuestionCard