# 🎓 Onboarding Agent - Adaptive Assessment Service

A Strands-based agentic service that administers adaptive probability assessments for student onboarding in the Learning System.

## Overview

The Onboarding Agent is a **prerequisite assessment module** that determines a student's competence level before they begin the main learning experience. It uses an adaptive quiz algorithm (IRT-based) and generates a comprehensive `UserProfile` that can be stored in the orchestrator's memory for use by other agents.

## Architecture

```
┌─────────────────────────────────────────┐
│     Orchestrator (Main Workflow)        │
│   - Manages shared memory               │
│   - Coordinates agents                  │
└─────────────────┬───────────────────────┘
                  │
                  │ calls as tool
                  ▼
┌─────────────────────────────────────────┐
│      Onboarding Agent (This Service)    │
│   - Adaptive quiz administration        │
│   - Competence level classification     │
│   - UserProfile generation              │
└─────────────────┬───────────────────────┘
                  │
                  │ uses
                  ▼
┌─────────────────────────────────────────┐
│    Existing Adaptive Quiz Backend       │
│   - adaptive_algorithm.py               │
│   - SQLite database                     │
│   - Question bank (73+ questions)       │
└─────────────────────────────────────────┘
```

## Features

- ✅ **Adaptive Assessment**: Questions adapt based on real-time performance
- ✅ **IRT-Based Ability Estimation**: Uses Item Response Theory for accurate ability scoring
- ✅ **Conversational Interface**: Natural language interaction via Strands Agent
- ✅ **AWS Bedrock Integration**: Uses Claude Sonnet 4 model
- ✅ **Comprehensive Profiling**: Generates detailed UserProfile for orchestrator
- ✅ **Mandatory Onboarding**: Ensures all users are properly assessed
- ✅ **Separate Service**: Can run independently or be called by orchestrator

## Project Structure

```
agents/
└── onboarding/
    ├── __init__.py
    ├── agent.py          # Main OnboardingAgent class
    ├── tools.py          # Strands tools (start_assessment, submit_answer, etc.)
    ├── config.py         # Bedrock and agent configuration
    └── prompts.py        # Agent instructions and prompts

shared/
└── models.py             # UserProfile dataclass for orchestrator memory

onboarding/               # Existing backend (reused)
└── backend/
    ├── adaptive_algorithm.py
    ├── models.py
    ├── database.py
    └── questions_data.py

run_onboarding_agent.py   # CLI for testing
requirements-agent.txt     # Dependencies
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements-agent.txt
```

### 2. Configure AWS Credentials

The agent uses AWS Bedrock. Ensure your AWS credentials are configured:

```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"  # or your preferred region

# Alternatively, use AWS CLI
aws configure
```

### 3. Enable Bedrock Model Access

Ensure Claude Sonnet 4 model is enabled in your AWS Bedrock console:
- Go to AWS Bedrock console
- Navigate to "Model access"
- Enable: `anthropic.claude-sonnet-4-*`

### 4. Configuration (Optional)

Create a `.env` file in the project root:

```bash
# AWS Configuration
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us-east-1.anthropic.claude-sonnet-4-20250514-v1:0

# Quiz Configuration
TOTAL_QUESTIONS=25

# Agent Configuration
AGENT_VERBOSE=true
```

## Usage

### Option 1: CLI Interface (Testing)

Run the agent interactively:

```bash
python run_onboarding_agent.py --user-id student_123
```

With custom settings:

```bash
python run_onboarding_agent.py \
    --user-id student_456 \
    --questions 15 \
    --region us-west-2
```

Run automated demo:

```bash
python run_onboarding_agent.py --user-id demo_user --demo
```

### Option 2: As a Tool in Orchestrator

```python
from agents.onboarding import OnboardingAgent
from shared.models import UserProfile

# Create agent
onboarding = OnboardingAgent()

# Run assessment
profile = onboarding.assess_user(user_id="student_123")

# Store in orchestrator memory
orchestrator_memory.store_user_profile(profile)

# Now other agents can use this profile
learning_agent.start(user_id="student_123", profile=profile)
```

### Option 3: Programmatic Usage

```python
from agents.onboarding.agent import create_onboarding_agent

# Create agent
agent = create_onboarding_agent(user_id="student_789")

# Start conversation
response = agent.chat("I'm ready to start the assessment")
print(response)

# Continue assessment
response = agent.chat("A")  # Submit answer
print(response)

# Async usage
import asyncio

async def run_assessment():
    response = await agent.chat_async("Start my assessment")
    print(response)

asyncio.run(run_assessment())
```

## Agent Tools

The agent has access to 5 tools:

### 1. `start_assessment`
```python
start_assessment(user_id: str, total_questions: Optional[int] = None)
```
- Initializes a new quiz session
- Returns session_id and first question
- Configurable number of questions

### 2. `get_next_question`
```python
get_next_question(session_id: str)
```
- Retrieves next adaptive question
- Difficulty adapts based on performance

### 3. `submit_answer`
```python
submit_answer(session_id: str, question_id: int, user_answer: str)
```
- Submits user's answer (A, B, C, or D)
- Provides immediate feedback
- Updates ability estimate

### 4. `get_progress`
```python
get_progress(session_id: str)
```
- Returns current progress
- Shows questions answered and remaining
- Current ability score

### 5. `finalize_assessment`
```python
finalize_assessment(session_id: str, user_id: str)
```
- Generates final UserProfile
- Returns competence level and recommendations
- Ready for orchestrator memory

## UserProfile Structure

The agent generates a `UserProfile` object with:

```python
@dataclass
class UserProfile:
    # Identification
    user_id: str
    session_id: str
    
    # Results
    competence_level: str  # "easy" | "medium" | "difficult"
    ability_score: float   # 0.0 - 1.0
    final_score: float     # Percentage
    
    # Performance Breakdown
    easy_accuracy: float
    medium_accuracy: float
    difficult_accuracy: float
    
    # Analysis
    strengths: List[str]
    weaknesses: List[str]
    
    # Recommendations
    recommended_starting_level: str
    suggested_topics: List[str]
    learning_pace: str  # "slow" | "normal" | "fast"
    
    # Metadata
    onboarding_completed: bool
    onboarding_completed_at: datetime
```

## Integration with Orchestrator

### As a Mandatory Prerequisite

```python
# In your orchestrator
def onboard_new_student(user_id: str):
    # Check if already onboarded
    profile = memory.get_user_profile(user_id)
    
    if not profile:
        # Run onboarding (mandatory)
        onboarding_agent = OnboardingAgent()
        profile = onboarding_agent.assess_user(user_id)
        
        # Store in shared memory
        memory.store_user_profile(profile)
        
        print(f"✅ Onboarding complete: {profile.competence_level}")
    
    # Proceed with main workflow
    return profile
```

### As a Tool for Main Agent

```python
from strands import Agent, tool
from agents.onboarding import OnboardingAgent

@tool
def run_onboarding_assessment(user_id: str) -> dict:
    """Run prerequisite assessment for new user."""
    onboarding = OnboardingAgent()
    profile = onboarding.assess_user(user_id)
    return profile.to_dict()

# Main orchestrator agent
orchestrator = Agent(
    name="LearningOrchestrator",
    tools=[run_onboarding_assessment, ...],
    instructions="""
    For new users, first run the onboarding assessment.
    Then use their competence level to personalize the experience.
    """
)
```

## Testing

### Run Tests

```bash
# Interactive test
python run_onboarding_agent.py --user-id test_001

# Demo mode
python run_onboarding_agent.py --demo

# Custom quiz length
python run_onboarding_agent.py --user-id test_002 --questions 10
```

### Expected Flow

1. **Welcome** → Agent introduces assessment
2. **Start** → User indicates readiness
3. **Question Loop** → 25 questions with adaptive difficulty
4. **Feedback** → Immediate feedback after each answer
5. **Completion** → Final profile generation
6. **Report** → Competence level and recommendations

## Troubleshooting

### "Unable to import strands"
```bash
pip install strands-agents
```

### "AWS credentials not configured"
```bash
aws configure
# or
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### "Bedrock model not available"
- Check AWS region matches model availability
- Ensure model access is enabled in Bedrock console
- Verify model ID format: `{region}.anthropic.claude-sonnet-4-*`

### "Database errors"
- Ensure `onboarding/backend/quiz.db` is writable
- Check SQLite is installed
- Verify backend dependencies are installed

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | `us-east-1` |
| `BEDROCK_MODEL_ID` | Bedrock model identifier | `us-east-1.anthropic.claude-sonnet-4-*` |
| `TOTAL_QUESTIONS` | Number of quiz questions | `25` |
| `AGENT_VERBOSE` | Enable verbose logging | `true` |

### Custom Configuration

```python
from agents.onboarding.config import OnboardingConfig
from agents.onboarding.agent import OnboardingAgent

# Custom config
config = OnboardingConfig()
config.MODEL_ID = "us-west-2.anthropic.claude-sonnet-4-20250514-v1:0"
config.DEFAULT_TOTAL_QUESTIONS = 15

# Create agent with custom config
agent = OnboardingAgent(config=config)
```

## Next Steps

After implementing the onboarding agent:

1. **Test Standalone** → Verify agent works independently
2. **Create Orchestrator** → Build main workflow coordinator
3. **Integrate Memory** → Set up shared state management
4. **Add Other Agents** → Learning path, content generation, etc.
5. **Deploy as Service** → Run as separate microservice

## License

Part of the LMA Major Project - Learning Assistant

## Support

For issues or questions, please refer to the main project documentation.
