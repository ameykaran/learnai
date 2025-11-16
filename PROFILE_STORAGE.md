# User Profile Storage in Orchestrator

## Overview

The orchestrator (`api_server/main.py`) stores user profiles in memory after the onboarding quiz is completed. This allows other agents to access the user's competence level, strengths, weaknesses, and personalized learning recommendations.

## How It Works

### 1. Profile Generation

When a user completes the onboarding quiz:

1. The `OnboardingAgent` calls the `finalize_assessment` tool
2. The tool creates a `UserProfile` object from the quiz results
3. The profile contains:
   - Competence level (easy, medium, difficult)
   - Ability score (IRT-based, 0.0-1.0)
   - Performance breakdown by difficulty
   - Strengths and weaknesses
   - Recommended starting level
   - Learning pace

### 2. Automatic Storage via Callback

The profile is automatically stored in the orchestrator's memory through a callback mechanism:

```python
# In handle_onboarding():
def profile_callback(uid: str, profile: UserProfile):
    session_manager.store_profile(uid, profile)
    logger.info(f"✅ Profile stored for user {uid}")

agent.tools_instance.set_profile_callback(profile_callback)
```

When `finalize_assessment` is called, it triggers the callback which stores the profile.

### 3. Profile Retrieval

Any agent can retrieve a user's profile from the `SessionManager`:

```python
# Get a specific user's profile
profile = session_manager.get_profile(user_id)

# Check if profile exists
has_profile = session_manager.has_profile(user_id)

# Get all profiles (for analytics/admin)
all_profiles = session_manager.get_all_profiles()
```

## Using Profiles in Your Agents

### Example: Content Recommendation Agent

```python
async def handle_content_agent(user_id: str, message: str, session: dict) -> tuple:
    """Content agent that uses profile for personalization."""
    
    # Get user profile
    profile = session_manager.get_profile(user_id)
    
    if not profile:
        return "Please complete onboarding first.", {}
    
    # Use profile data
    difficulty = profile.recommended_starting_level
    pace = profile.learning_pace
    
    # Recommend content based on profile
    if difficulty == "fundamentals":
        content = get_basic_content(pace)
    elif difficulty == "intermediate":
        content = get_intermediate_content(pace)
    else:
        content = get_advanced_content(pace)
    
    # Focus on weaknesses
    if profile.weaknesses:
        content += get_targeted_content(profile.weaknesses)
    
    return content, {"profile_used": True}
```

### Example: Quiz Agent with Adaptive Difficulty

```python
async def handle_quiz_agent(user_id: str, message: str, session: dict) -> tuple:
    """Quiz agent that adapts to user's competence."""
    
    profile = session_manager.get_profile(user_id)
    
    # Select question difficulty based on profile
    if profile:
        starting_difficulty = profile.competence_level
        ability = profile.ability_score
    else:
        starting_difficulty = "medium"
        ability = 0.5
    
    question = select_adaptive_question(starting_difficulty, ability)
    
    return question, {"difficulty": starting_difficulty}
```

## Profile Data Structure

The `UserProfile` class contains:

```python
@dataclass
class UserProfile:
    # Identification
    user_id: str
    session_id: str
    
    # Assessment Results
    competence_level: str  # "easy" | "medium" | "difficult"
    ability_score: float  # 0.0 - 1.0
    final_score: float  # Percentage correct
    
    # Performance by Difficulty
    easy_accuracy: float
    medium_accuracy: float
    difficult_accuracy: float
    overall_accuracy: float
    
    # Analysis
    strengths: List[str]  # e.g., ["basic_probability_concepts"]
    weaknesses: List[str]
    
    # Recommendations
    recommended_starting_level: str  # Where to start curriculum
    suggested_topics: List[str]
    learning_pace: str  # "slow" | "normal" | "fast"
    
    # Metadata
    onboarding_completed: bool
    onboarding_started_at: datetime
    onboarding_completed_at: datetime
```

## API Endpoints

### Check Profile Status

```bash
GET /api/users/{user_id}/profile
```

Response:
```json
{
  "user_id": "user123",
  "has_profile": true,
  "profile": {
    "competence_level": "medium",
    "ability_score": 0.65,
    "overall_accuracy": 72.5,
    "strengths": ["basic_probability_concepts"],
    "weaknesses": ["advanced_probability"],
    "recommended_starting_level": "intermediate",
    "learning_pace": "normal"
  }
}
```

### Session Info (includes profile status)

```bash
GET /api/sessions/{session_id}
```

Response includes `has_profile` field.

## Best Practices

1. **Always check for profile existence** before accessing profile data
2. **Handle missing profiles gracefully** - redirect to onboarding if needed
3. **Use profile data for personalization**:
   - Adjust content difficulty
   - Recommend appropriate topics
   - Set learning pace
   - Focus on weaknesses
4. **Update profile data** if your agent gathers new insights about the user
5. **Respect privacy** - profiles are session-based and not persisted to disk by default

## Storage Mechanism

Currently, profiles are stored **in-memory** in the `SessionManager`:

- ✅ **Pros**: Fast access, simple implementation
- ⚠️ **Cons**: Lost on server restart, not persistent

### Future: Database Storage

For production, consider persisting profiles to a database:

```python
# Add to SessionManager
def persist_profile(self, user_id: str, profile: UserProfile):
    """Save profile to database."""
    db.save_user_profile(user_id, profile.to_dict())

def load_profile(self, user_id: str) -> Optional[UserProfile]:
    """Load profile from database."""
    data = db.get_user_profile(user_id)
    return UserProfile.from_dict(data) if data else None
```

## Testing Profile Storage

Test the profile storage flow:

1. Start the API server: `./start-api-server.sh`
2. Create onboarding session:
   ```bash
   curl -X POST http://localhost:8000/api/sessions \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user", "mode": "onboarding"}'
   ```
3. Complete quiz (via chat interface or WebSocket)
4. Check profile:
   ```bash
   curl http://localhost:8000/api/users/test_user/profile
   ```
5. Switch to orchestrator mode and see profile data in responses

## Summary

The orchestrator now automatically stores user profiles after onboarding completion. All agents can access this profile data through the `session_manager` to provide personalized learning experiences. The callback mechanism ensures profiles are captured without manual intervention.
