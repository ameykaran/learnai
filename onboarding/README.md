# Adaptive Probability Quiz Application

A self-adaptive quiz application built with Next.js frontend and FastAPI backend that classifies users into three competence levels (easy, medium, difficult) based on their probability knowledge.

## Features

- **Adaptive Algorithm**: Questions adjust based on user performance
- **100+ Questions**: Covering probability concepts from 7th to 12th grade
- **Three Difficulty Levels**: Easy, Medium, and Difficult classifications
- **Clean UI**: Modern, responsive design with Tailwind CSS
- **Real-time Feedback**: Immediate answer feedback and progress tracking
- **Quiz Reset**: Ability to retake the assessment
- **Detailed Results**: Comprehensive performance analysis

## Project Structure

```
├── frontend/          # Next.js React frontend
│   ├── src/
│   │   ├── app/       # App router pages
│   │   └── components/ # React components
├── backend/           # FastAPI backend
│   ├── main.py        # FastAPI application
│   ├── models.py      # Database models
│   ├── quiz_algorithm.py # Adaptive quiz logic
│   ├── questions_data.py # Question database
│   └── requirements.txt
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. (Optional) Configure quiz settings:
```bash
# ONBOARDING_TOTAL_QUESTIONS=25  # Default is 25, change as needed
```

3. Install dependencies (you may need --break-system-packages flag):
```bash
pip install -r requirements.txt --break-system-packages
```

3. Run the FastAPI server:
```bash
python main.py
```

Or use the run script:
```bash
python run.py --install  # First time only
python run.py
```

The backend will be available at http://localhost:8000

## Configuration

### Environment Variables

The quiz behavior can be customized using environment variables. Create a `.env` file in the `backend` directory:

- `ONBOARDING_TOTAL_QUESTIONS`: Total number of questions to assess (default: 25)
  - Example: `ONBOARDING_TOTAL_QUESTIONS=30` for a longer assessment
  - Example: `ONBOARDING_TOTAL_QUESTIONS=15` for a shorter assessment

**Note**: After changing `ONBOARDING_TOTAL_QUESTIONS`, you may need to delete the existing `quiz.db` file to ensure new quiz sessions use the updated value.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## How the Adaptive Algorithm Works

1. **Initial Phase**: Users start with easy questions (questions 1-5)
2. **Performance Tracking**: Algorithm tracks accuracy by difficulty level
3. **Level Progression**:
   - 80%+ accuracy in easy questions → Move to medium
   - 80%+ accuracy in medium questions → Move to difficult
   - <60% accuracy → Stay at current level or move down
4. **Final Classification**:
   - **Easy**: Basic understanding of probability concepts
   - **Medium**: Solid grasp with some advanced concepts
   - **Difficult**: Mastery of advanced probability and statistics

## API Endpoints

- `POST /quiz/start` - Start a new quiz session
- `GET /quiz/{session_id}/question` - Get current question
- `POST /quiz/submit` - Submit an answer
- `GET /quiz/{session_id}/results` - Get quiz results
- `DELETE /quiz/{session_id}` - Reset quiz session
- `GET /quiz/stats` - Get overall statistics

## Database

The application uses SQLite with the following models:
- **Questions**: MCQ questions with difficulty levels
- **Users**: Quiz participants
- **QuizSessions**: Individual quiz attempts
- **UserResponses**: Individual question responses

## Technologies Used

### Frontend
- Next.js 14 with App Router
- React 18
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Question Categories

- **Easy (7th-8th grade)**: Basic probability, simple calculations, fundamental concepts
- **Medium (9th-10th grade)**: Compound events, conditional probability, combinations
- **Difficult (11th-12th grade)**: Advanced distributions, statistical inference, complex probability models

## Development Notes

- Questions are automatically populated on first startup
- Sessions are identified by UUID
- Results include detailed breakdown by difficulty level
- Algorithm ensures 25 questions per assessment
- Adaptive logic prevents infinite loops in any difficulty level

## Future Enhancements

- User authentication and persistent profiles
- Question difficulty tuning based on response patterns
- Additional subjects beyond probability
- Advanced analytics and learning recommendations
- Integration with learning management systems