'use client'

interface ProgressBarProps {
  currentQuestion: number
  totalQuestions: number
}

const ProgressBar: React.FC<ProgressBarProps> = ({ currentQuestion, totalQuestions }) => {
  const progress = (currentQuestion / totalQuestions) * 100

  return (
    <div className="mb-8">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>Progress</span>
        <span>{currentQuestion} of {totalQuestions} questions</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className="bg-gradient-to-r from-indigo-500 to-purple-600 h-3 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <div className="text-center mt-2">
        <span className="text-sm font-medium text-indigo-600">
          {Math.round(progress)}% Complete
        </span>
      </div>
    </div>
  )
}

export default ProgressBar