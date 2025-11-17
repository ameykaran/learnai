# Profile-Based Intelligent Retrieval

## Overview

The Retriever Agent now intelligently adapts content retrieval based on the student's **UserProfile**, ensuring personalized learning experiences that match their competence level, strengths, and weaknesses.

## How It Works

### 1. **Profile Information Flow**

```
User Query + UserProfile
    ↓
Orchestrator.process_query()
    ↓
Orchestrator._execute_retriever()
    ↓
RAGChatAgent.chat(message, user_profile)
    ↓
Agent builds profile context
    ↓
Enhanced message with profile instructions
    ↓
LLM calls search_knowledge_base with appropriate difficulty_level
    ↓
Personalized content returned
```

### 2. **UserProfile Structure**

```python
class UserProfile:
    user_id: str
    competence_level: str           # 'beginner', 'intermediate', 'advanced'
    ability_score: float            # 0.0 to 1.0
    strengths: List[str]            # Topics student is strong in
    weaknesses: List[str]           # Topics needing improvement
    recommended_starting_level: str
```

### 3. **Profile Context Building**

When a user profile is provided, the RAG agent builds a context string like:

```
[User Profile Context for Personalized Content Retrieval]
Student Level: Intermediate (retrieve 'intermediate' difficulty content)
Ability Score: 0.65
Strong Topics: algebra, calculus, linear algebra
Areas for Improvement: probability, statistics, combinatorics
(Provide extra support and simpler explanations for these topics)

IMPORTANT: Use the search_knowledge_base tool with the appropriate 'difficulty_level' parameter.
For weak topics, consider retrieving prerequisite concepts first.

User Query: Explain conditional probability
```

## Intelligent Retrieval Strategies

### Strategy 1: Difficulty Adaptation

The agent automatically adjusts content difficulty based on:

| Student Level | Strong Topics | Weak Topics | New Topics |
|--------------|---------------|-------------|------------|
| **Beginner** | basic | basic | basic |
| **Intermediate** | intermediate-advanced | basic | intermediate |
| **Advanced** | advanced | intermediate | advanced |

**Implementation:**

```python
# For weak topics - go easier
if query_topic in user_profile.weaknesses:
    difficulty = lower_difficulty(user_profile.competence_level)
    # e.g., intermediate → basic

# For strong topics - challenge them
elif query_topic in user_profile.strengths:
    difficulty = higher_difficulty(user_profile.competence_level)
    # e.g., intermediate → advanced

# For new topics - match their level
else:
    difficulty = user_profile.competence_level
```

### Strategy 2: Prerequisite Checking

For weak topics, the agent proactively checks prerequisites:

```python
# User asks about "Bayes theorem" (a weak topic)
# Agent strategy:
1. Call get_prerequisites("Bayes theorem")
2. Check if prerequisites are in weaknesses
3. If yes, retrieve those first with 'basic' difficulty
4. Then retrieve main topic with 'intermediate' difficulty
```

### Strategy 3: Content Type Selection

Based on the profile, the agent selects appropriate content types:

**For Weak Topics:**
- ✅ Definition (clear, formal)
- ✅ Multiple examples (concrete cases)
- ✅ Analogies (relatable explanations)
- ✅ Visualizations (intuitive understanding)
- ✅ Misconceptions (common errors to avoid)
- ⚠️ Avoid: Advanced proofs, complex practice problems

**For Strong Topics:**
- ✅ Advanced explanations
- ✅ Proofs (mathematical rigor)
- ✅ Challenging practice problems
- ✅ Edge cases and extensions
- ⚠️ Less emphasis on basic definitions

## Example Scenarios

### Scenario 1: Weak Topic Query

**User Profile:**
```python
competence_level: "intermediate"
weaknesses: ["probability", "statistics"]
```

**Query:** "Explain conditional probability"

**Agent Behavior:**
1. Detects "probability" is a weakness
2. Calls `search_knowledge_base(query="conditional probability", difficulty_level="basic", chunk_type="definition")`
3. Calls `get_prerequisites("conditional probability")`
4. Retrieves simple examples: `search_knowledge_base(query="conditional probability examples", difficulty_level="basic", chunk_type="example", k=3)`
5. Retrieves analogies for easier understanding
6. Synthesizes with extra explanations and step-by-step breakdowns

**Result:** Student gets content below their overall level, with extra support materials.

---

### Scenario 2: Strong Topic Query

**User Profile:**
```python
competence_level: "intermediate"
strengths: ["algebra", "calculus"]
```

**Query:** "How do I solve this differential equation?"

**Agent Behavior:**
1. Detects "calculus" (differential equations) is a strength
2. Calls `search_knowledge_base(query="differential equations", difficulty_level="advanced", chunk_type="explanation")`
3. Retrieves challenging practice problems
4. Includes advanced techniques and edge cases
5. Minimal hand-holding, assumes strong foundation

**Result:** Student gets challenging content that pushes their abilities.

---

### Scenario 3: New Topic (Neither Strong nor Weak)

**User Profile:**
```python
competence_level: "advanced"
strengths: ["geometry"]
weaknesses: ["probability"]
```

**Query:** "What is topology?"

**Agent Behavior:**
1. "Topology" not in strengths or weaknesses (new topic)
2. Uses overall competence level: `difficulty_level="advanced"`
3. Provides comprehensive explanation appropriate for advanced student
4. Includes connections to geometry (student's strength)

**Result:** Student gets content matching their overall level, with connections to familiar topics.

---

### Scenario 4: Mixed Topics Query

**User Profile:**
```python
competence_level: "intermediate"
strengths: ["algebra"]
weaknesses: ["probability"]
```

**Query:** "How does probability relate to algebraic structures?"

**Agent Behavior:**
1. Detects mixed topics (strength + weakness)
2. Strategy: Build from strength to weakness
3. Retrieves `difficulty_level="intermediate"` for algebra part
4. Retrieves `difficulty_level="basic"` for probability part
5. Creates bridge between topics: "Since you're strong in algebra, think of probability distributions as functions..."

**Result:** Leverages student's strengths to teach weaknesses.

## Implementation Details

### Code Changes

**1. RAGChatAgent.chat() Method**

```python
def chat(self, message: str, user_profile=None, **kwargs) -> str:
    # Build profile context if available
    if user_profile:
        profile_context = self._build_profile_context(user_profile)
        enhanced_message = f"{profile_context}\n\nUser Query: {message}"
    else:
        enhanced_message = message
    
    response = self.agent(enhanced_message, **kwargs)
    return str(response)
```

**2. Profile Context Builder**

```python
def _build_profile_context(self, user_profile) -> str:
    context_parts = [
        "[User Profile Context for Personalized Content Retrieval]"
    ]
    
    # Map competence level to difficulty
    level_map = {
        'beginner': 'basic',
        'intermediate': 'intermediate',
        'advanced': 'advanced'
    }
    difficulty = level_map.get(user_profile.competence_level.lower(), 'intermediate')
    context_parts.append(f"Student Level: {user_profile.competence_level.title()} (retrieve '{difficulty}' difficulty content)")
    
    # Add strengths and weaknesses
    if user_profile.strengths:
        context_parts.append(f"Strong Topics: {', '.join(user_profile.strengths[:3])}")
    
    if user_profile.weaknesses:
        context_parts.append(f"Areas for Improvement: {', '.join(user_profile.weaknesses[:3])}")
        context_parts.append("(Provide extra support and simpler explanations for these topics)")
    
    # Add instructions for tool usage
    context_parts.append("\nIMPORTANT: Use the search_knowledge_base tool with the appropriate 'difficulty_level' parameter.")
    context_parts.append("For weak topics, consider retrieving prerequisite concepts first.")
    
    return "\n".join(context_parts)
```

**3. Orchestrator Integration**

```python
def _execute_retriever(self, query, context, user_profile, steps):
    retrieval_query = f"{context}\n{query}" if context else query
    
    # Pass user_profile to enable personalization
    retrieved = self.retriever.chat(
        message=retrieval_query,
        user_profile=user_profile  # ← Profile passed here
    )
    
    # ... rest of the method
```

### Agent Instructions Update

The system prompt now includes explicit instructions for profile-based retrieval:

```markdown
# User Profile Awareness

When a user profile is provided, you MUST:
1. Extract the student's level and use it in search_knowledge_base calls
2. Identify strong topics and build upon them
3. Identify weak topics and provide additional support
4. Adjust difficulty: Always pass the appropriate difficulty_level parameter

## Profile-Based Search Strategy

### For Strong Topics:
- Use difficulty_level matching or one level higher
- Focus on advanced applications
- Connect to related advanced topics

### For Weak Topics:
- Use difficulty_level one level lower
- Retrieve prerequisite concepts first
- Provide more examples and analogies
- Include misconception content
```

## Benefits

### 1. **Personalized Learning**
- Content difficulty matches student's actual level
- Prevents overwhelming advanced students with basics
- Prevents frustrating beginners with complex content

### 2. **Efficient Learning**
- Students spend time on content at the right difficulty
- Strong topics: Challenged and engaged
- Weak topics: Supported and scaffolded

### 3. **Reduced Frustration**
- Prerequisites identified and taught first
- Common misconceptions addressed proactively
- Step-by-step explanations for difficult topics

### 4. **Better Engagement**
- Content feels relevant and achievable
- Connections made to student's strengths
- Progress visible through appropriate challenges

### 5. **Data-Driven Adaptation**
- Uses actual assessment data (from onboarding)
- Continuously refined as student progresses
- Objective measure of competence (ability_score)

## Testing Profile-Based Retrieval

### Test Case 1: Beginner with Weak Probability

```python
from shared.models import UserProfile
from agents.retrieval.agent import create_rag_chat_agent

# Create profile
profile = UserProfile(
    user_id="test_001",
    session_id="session_001",
    competence_level="beginner",
    ability_score=0.25,
    final_score=0.30,
    strengths=[],
    weaknesses=["probability", "statistics"]
)

# Create agent
agent = create_rag_chat_agent()

# Query about weak topic
response = agent.chat(
    "Explain conditional probability",
    user_profile=profile
)

# Expected: Basic difficulty content with extra examples
print(response)
```

### Test Case 2: Advanced with Strong Calculus

```python
profile = UserProfile(
    user_id="test_002",
    session_id="session_002",
    competence_level="advanced",
    ability_score=0.85,
    final_score=0.90,
    strengths=["calculus", "linear algebra", "analysis"],
    weaknesses=[]
)

response = agent.chat(
    "Explain stochastic calculus",
    user_profile=profile
)

# Expected: Advanced difficulty content with proofs and applications
print(response)
```

### Test Case 3: No Profile (Default Behavior)

```python
response = agent.chat(
    "What is probability?"
    # No user_profile parameter
)

# Expected: Intermediate difficulty (default), no personalization
print(response)
```

## Monitoring & Analytics

Track these metrics to evaluate profile-based retrieval:

1. **Difficulty Match Rate**: % of retrievals using profile-adjusted difficulty
2. **Prerequisite Calls**: Frequency of get_prerequisites for weak topics
3. **Content Type Distribution**: Breakdown by student level
4. **Student Engagement**: Time spent, follow-up questions
5. **Learning Outcomes**: Improvement in weak topics over time

## Future Enhancements

### 1. **Dynamic Difficulty Adjustment**
- Update profile during conversation based on responses
- If student struggles, automatically lower difficulty
- If student excels, increase challenge level

### 2. **Topic-Specific Profiles**
- Track competence per topic, not just overall
- "Intermediate in probability, Advanced in statistics"
- More granular personalization

### 3. **Learning Style Adaptation**
- Visual learners: Prioritize visualizations
- Analytical learners: More proofs and formal explanations
- Practical learners: More examples and practice problems

### 4. **Collaborative Filtering**
- "Students with similar profiles found this helpful..."
- Recommend content based on peer success

### 5. **Prerequisite Graph**
- Build knowledge graph of prerequisites
- Optimal learning path based on current knowledge
- Identify gaps automatically

## Summary

The profile-based intelligent retrieval system:

✅ **Adapts content difficulty** to student's competence level  
✅ **Provides extra support** for weak topics  
✅ **Challenges students** in their strong areas  
✅ **Checks prerequisites** proactively  
✅ **Selects appropriate content types** based on needs  
✅ **Maintains consistency** with onboarding assessment  
✅ **Improves learning outcomes** through personalization  

This creates a truly adaptive learning experience where every student receives content optimized for their unique learning profile! 🎯
