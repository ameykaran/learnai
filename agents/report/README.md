# Report Agent - Learning Progress Analytics

## Overview

The **Report Agent** is a sophisticated analytics agent that generates comprehensive learning progress reports for students in the adaptive probability learning platform. It tracks performance over time, identifies trends, analyzes topic mastery, and provides personalized recommendations for improvement.

## Architecture

### Components

1. **ReportAgent** (`agents/report/agent.py`)
   - Main agent class using Strands framework
   - Integrates with LLM for intelligent analysis
   - Provides multiple report generation methods

2. **Analytics Backend** (`agents/report/backend/analytics.py`)
   - `ProgressAnalyzer`: Core analytics engine
   - `create_learning_report()`: Report generation function
   - Trend calculation and pattern recognition

3. **Tools** (`agents/report/tools.py`)
   - 6 specialized tools for data retrieval and analysis
   - Database integration for time-series queries
   - Data transformation and formatting

4. **Database Models** (`agents/onboarding/backend/models.py`)
   - `ProgressSnapshot`: Periodic performance snapshots
   - `QuizAttemptHistory`: Historical quiz data
   - `TopicMastery`: Topic-level mastery tracking
   - `LearningSession`: Session activity tracking

5. **Shared Models** (`shared/models.py`)
   - `ProgressSnapshot`: Progress data model
   - `QuizAttempt`: Quiz attempt model
   - `TopicMasteryRecord`: Topic mastery model
   - `LearningReport`: Comprehensive report model

## Features

### 1. Progress Tracking
- **Time-Series Analysis**: Track performance over days, weeks, months
- **Accuracy Metrics**: Overall, easy, medium, difficult
- **Ability Scores**: IRT-based ability estimation
- **Competence Levels**: Classification of student level

### 2. Quiz Performance Analytics
- Historical quiz attempt tracking
- Score trends and improvement rates
- Difficulty distribution analysis
- Topic-specific performance

### 3. Topic Mastery Analysis
- Per-topic mastery levels (0-1 scale)
- Confidence scores
- Mastery history over time
- Status tracking (learning, mastered, needs_review)

### 4. Learning Activity Metrics
- Total learning time
- Session frequency and duration
- Engagement patterns
- Activity distribution

### 5. Trend Identification
- Performance trends (improving, declining, stable)
- Consistency scoring
- Pattern recognition
- Anomaly detection

### 6. Personalized Recommendations
- Focus area identification
- Study strategy suggestions
- Topic prioritization
- Motivational guidance

## Tools Available

### 1. `get_user_progress_history`
Retrieves progress snapshots over a time period.

```python
get_user_progress_history(
    user_session_id="user_123",
    days=7
)
```

**Returns**: JSON with timestamped snapshots, accuracy, ability scores

### 2. `get_quiz_performance_trends`
Analyzes quiz performance trends.

```python
get_quiz_performance_trends(
    user_session_id="user_123",
    days=30
)
```

**Returns**: Quiz history, scores, trends, improvement metrics

### 3. `get_topic_mastery_analysis`
Detailed topic-by-topic mastery analysis.

```python
get_topic_mastery_analysis(
    user_session_id="user_123"
)
```

**Returns**: Mastery levels, strongest/weakest topics, status

### 4. `get_learning_time_stats`
Learning time and engagement statistics.

```python
get_learning_time_stats(
    user_session_id="user_123",
    days=7
)
```

**Returns**: Total time, session counts, averages

### 5. `generate_comprehensive_report`
Generates a full report with all metrics.

```python
generate_comprehensive_report(
    user_session_id="user_123",
    days=7
)
```

**Returns**: Formatted comprehensive report

### 6. `compare_time_periods`
Compares performance between two periods.

```python
compare_time_periods(
    user_session_id="user_123",
    period1_days=7,
    period2_days=14
)
```

**Returns**: Comparison metrics and trend analysis

## Usage

### Basic Usage

```python
from agents.report.agent import ReportAgent

# Create agent
agent = ReportAgent()

# Generate comprehensive report
report = agent.generate_report(
    user_session_id="user_123",
    days=7,
    report_type="comprehensive"
)
print(report)
```

### Report Types

#### 1. Comprehensive Report
Complete analysis with all metrics and recommendations.

```python
report = agent.generate_report(
    user_session_id="user_123",
    days=7,
    report_type="comprehensive"
)
```

#### 2. Quick Summary
Concise overview with key metrics.

```python
report = agent.generate_report(
    user_session_id="user_123",
    days=7,
    report_type="quick"
)
```

#### 3. Detailed Analysis
In-depth analysis with extensive data.

```python
report = agent.generate_report(
    user_session_id="user_123",
    days=30,
    report_type="detailed"
)
```

### Specific Analyses

#### Progress Analysis
```python
analysis = agent.analyze_progress(
    user_session_id="user_123",
    days=14
)
```

#### Get Recommendations
```python
recommendations = agent.get_recommendations(
    user_session_id="user_123"
)
```

#### Compare Periods
```python
comparison = agent.compare_periods(
    user_session_id="user_123",
    recent_days=7,
    previous_days=14
)
```

### Chat Interface
```python
response = agent.chat(
    message="What topics should I focus on?",
    user_session_id="user_123"
)
```

## Integration with Orchestrator

The Report Agent is integrated into the main orchestrator:

```python
# Orchestrator automatically routes report requests
result = orchestrator.process_query(
    query="Show me my learning progress report",
    user_id="user_123"
)
```

Query types that trigger the report agent:
- "show my progress report"
- "how am I doing"
- "generate performance report"
- "what should I improve"
- "track my learning"

## Data Flow

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Orchestrator   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Report Agent   │ ◄── Uses Tools
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Database Query  │
│   (Time Series) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Analytics    │
│   Processing    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Analysis   │
│  & Generation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Formatted Report│
└─────────────────┘
```

## Database Schema

### Progress Snapshots
```sql
CREATE TABLE progress_snapshots (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    snapshot_date DATETIME,
    overall_accuracy FLOAT,
    ability_score FLOAT,
    competence_level VARCHAR(20),
    easy_accuracy FLOAT,
    medium_accuracy FLOAT,
    difficult_accuracy FLOAT,
    total_questions_attempted INTEGER,
    total_questions_correct INTEGER,
    topic_scores JSON,
    total_learning_time_minutes FLOAT,
    quiz_attempts_count INTEGER,
    snapshot_type VARCHAR(20)
);
```

### Quiz Attempt History
```sql
CREATE TABLE quiz_attempt_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    quiz_session_id INTEGER,
    attempted_at DATETIME,
    duration_minutes FLOAT,
    score FLOAT,
    total_questions INTEGER,
    correct_answers INTEGER,
    topics JSON,
    topic_scores JSON,
    quiz_type VARCHAR(50)
);
```

### Topic Mastery
```sql
CREATE TABLE topic_mastery (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    topic VARCHAR(100),
    mastery_level FLOAT,
    confidence_score FLOAT,
    attempts INTEGER,
    correct_count INTEGER,
    total_count INTEGER,
    first_attempted DATETIME,
    last_attempted DATETIME,
    mastery_history JSON,
    status VARCHAR(20)
);
```

### Learning Sessions
```sql
CREATE TABLE learning_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    started_at DATETIME,
    ended_at DATETIME,
    duration_minutes FLOAT,
    activities JSON,
    topics_covered JSON,
    questions_attempted INTEGER,
    questions_correct INTEGER,
    session_type VARCHAR(50)
);
```

## Configuration

Edit `agents/report/config.py`:

```python
@dataclass
class ReportConfig:
    # Model Configuration
    MODEL_ID: str = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    
    # Report Settings
    DEFAULT_PERIOD_DAYS: int = 7
    MIN_DATA_POINTS: int = 2
    
    # Thresholds
    MASTERY_THRESHOLD: float = 0.80
    WEAK_TOPIC_THRESHOLD: float = 0.60
    IMPROVEMENT_THRESHOLD: float = 0.05
```

## Testing

### Run Standalone Test
```bash
python run_report_agent.py
```

### Run with Sample Data
```bash
python test_report_agent.py
```

This creates sample data and generates all report types.

## Examples

### Example Report Output

```
Learning Progress Report
========================
User ID: user_123
Period: 2025-11-09 to 2025-11-16 (7 days)
Generated: 2025-11-16 10:30

OVERALL PERFORMANCE
-------------------
Accuracy: 78.5%
Ability Score: 0.785
Improvement: +12.3%
Trend: IMPROVING
Consistency: 0.82

ACTIVITY SUMMARY
---------------
Learning Time: 315 minutes
Quizzes Taken: 8
Questions Attempted: 200
Questions Correct: 157

PERFORMANCE BY DIFFICULTY
------------------------
Easy: 92.3%
Medium: 78.5%
Difficult: 65.2%

TOPIC MASTERY
------------
Mastered (2): probability, statistics
In Progress (3): combinatorics, distributions, conditional_probability
Strongest: probability, statistics, combinatorics
Needs Focus: conditional_probability, distributions

RECOMMENDATIONS
--------------
• Focus on strengthening: conditional_probability, distributions
• Great progress on probability and statistics - maintain momentum
• Performance is consistent - keep regular study schedule
• Consider tackling more challenging problems in mastered topics
```

## API Reference

### ReportAgent Class

#### Methods

**`__init__(config: Optional[ReportConfig] = None)`**
Initialize the agent.

**`generate_report(user_session_id: str, days: int = None, report_type: str = "comprehensive") -> str`**
Generate a learning progress report.

**`analyze_progress(user_session_id: str, days: int = None) -> str`**
Analyze progress trends.

**`get_recommendations(user_session_id: str) -> str`**
Get personalized recommendations.

**`compare_periods(user_session_id: str, recent_days: int = 7, previous_days: int = 14) -> str`**
Compare performance between periods.

**`chat(message: str, user_session_id: Optional[str] = None) -> str`**
General chat interface for report queries.

## Best Practices

1. **Regular Snapshots**: Create progress snapshots daily or after each quiz
2. **Data Quality**: Ensure quiz data includes topic information
3. **Time Periods**: Use appropriate time windows (7 days for recent, 30 for trends)
4. **User Context**: Always provide user_session_id for personalized reports
5. **Error Handling**: Handle cases with insufficient data gracefully

## Future Enhancements

- [ ] Visualization data generation (charts, graphs)
- [ ] PDF report export
- [ ] Email report delivery
- [ ] Parent/teacher dashboard integration
- [ ] Predictive analytics (future performance prediction)
- [ ] Peer comparison (anonymized)
- [ ] Achievement badges and milestones
- [ ] Weekly automated reports

## Troubleshooting

### No Data Available
**Problem**: "No progress data found"
**Solution**: Ensure user has completed quizzes and snapshots are created

### Missing Topic Mastery
**Problem**: Topic mastery data not available
**Solution**: Update topic mastery after each quiz completion

### Slow Report Generation
**Problem**: Report takes too long
**Solution**: Optimize time period or use quick summary mode

## Support

For issues or questions:
- Check logs in console output
- Review database for data availability
- Verify user_session_id is correct
- Check database connection

## License

Part of the LMA Adaptive Learning Platform
