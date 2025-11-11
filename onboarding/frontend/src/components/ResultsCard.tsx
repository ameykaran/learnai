'use client'

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

interface ResultsCardProps {
  results: QuizResults
  onReset: () => void
}

const ResultsCard: React.FC<ResultsCardProps> = ({ results, onReset }) => {
  const getCompetenceLevelInfo = (level: string) => {
    switch (level) {
      case 'easy':
        return {
          title: 'Beginner Level',
          description: 'You have a foundational understanding of basic probability concepts. Focus on strengthening your knowledge of simple probability calculations and basic terminology.',
          color: 'text-green-700',
          bgColor: 'bg-green-100',
          borderColor: 'border-green-300',
          icon: '🌱'
        }
      case 'medium':
        return {
          title: 'Intermediate Level',
          description: 'You have a solid grasp of probability concepts and can handle more complex problems. Continue practicing with compound events and conditional probability.',
          color: 'text-yellow-700',
          bgColor: 'bg-yellow-100',
          borderColor: 'border-yellow-300',
          icon: '🌿'
        }
      case 'difficult':
        return {
          title: 'Advanced Level',
          description: 'Excellent! You have mastered advanced probability concepts and can tackle challenging problems involving distributions, statistical inference, and complex probability models.',
          color: 'text-red-700',
          bgColor: 'bg-red-100',
          borderColor: 'border-red-300',
          icon: '🌳'
        }
      default:
        return {
          title: 'Unknown Level',
          description: 'Assessment completed.',
          color: 'text-gray-700',
          bgColor: 'bg-gray-100',
          borderColor: 'border-gray-300',
          icon: '❓'
        }
    }
  }

  const levelInfo = getCompetenceLevelInfo(results.final_competence_level)

  const StatCard = ({ title, correct, total, accuracy, difficulty }: { title: string, correct: number, total: number, accuracy: number, difficulty: string }) => {
    const getDifficultyColor = (diff: string) => {
      switch (diff) {
        case 'easy':
          return 'border-green-300 bg-green-50'
        case 'medium':
          return 'border-yellow-300 bg-yellow-50'
        case 'difficult':
          return 'border-red-300 bg-red-50'
        default:
          return 'border-gray-300 bg-gray-50'
      }
    }

    return (
      <div className={`border-2 rounded-lg p-4 ${getDifficultyColor(difficulty)}`}>
        <h4 className="font-semibold text-gray-900 mb-2">{title}</h4>
        <div className="space-y-1 text-sm">
          <p>Questions: {total}</p>
          <p>Correct: {correct}</p>
          <p>Accuracy: {total > 0 ? (accuracy * 100).toFixed(1) : 0}%</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🎉</div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Quiz Complete!
            </h1>
            <p className="text-lg text-gray-600">
              You answered {results.total_correct} out of {results.total_questions} questions correctly
            </p>
            <div className="text-2xl font-bold text-indigo-600 mt-2">
              Overall Score: {(results.overall_accuracy * 100).toFixed(1)}%
            </div>
          </div>

          <div className={`border-2 rounded-xl p-6 mb-8 ${levelInfo.borderColor} ${levelInfo.bgColor}`}>
            <div className="text-center">
              <div className="text-4xl mb-4">{levelInfo.icon}</div>
              <h2 className={`text-2xl font-bold mb-3 ${levelInfo.color}`}>
                Your Competence Level: {levelInfo.title}
              </h2>
              <p className={`text-base leading-relaxed ${levelInfo.color}`}>
                {levelInfo.description}
              </p>
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4 text-center">
              Performance by Difficulty
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <StatCard
                title="Easy Questions"
                correct={results.easy_stats.correct}
                total={results.easy_stats.total}
                accuracy={results.easy_stats.accuracy}
                difficulty="easy"
              />
              <StatCard
                title="Medium Questions"
                correct={results.medium_stats.correct}
                total={results.medium_stats.total}
                accuracy={results.medium_stats.accuracy}
                difficulty="medium"
              />
              <StatCard
                title="Difficult Questions"
                correct={results.difficult_stats.correct}
                total={results.difficult_stats.total}
                accuracy={results.difficult_stats.accuracy}
                difficulty="difficult"
              />
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              What happens next?
            </h3>
            <div className="text-gray-700 space-y-2">
              <p>• Your competence level will be used to personalize your learning experience</p>
              <p>• Learning modules will be tailored to your current understanding</p>
              <p>• You can retake this assessment at any time to track your progress</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <button
              onClick={onReset}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              Take Quiz Again
            </button>
            <button
              onClick={() => window.print()}
              className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              Print Results
            </button>
          </div>

          <div className="mt-8 text-center text-sm text-gray-500">
            Session ID: {results.session_id}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsCard