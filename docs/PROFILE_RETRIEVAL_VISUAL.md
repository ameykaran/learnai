# Profile-Based Retrieval - Visual Guide

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER WITH PROFILE                            │
│  user_id: "student_123"                                         │
│  competence_level: "intermediate"                               │
│  strengths: ["algebra", "calculus"]                             │
│  weaknesses: ["probability", "statistics"]                      │
│  ability_score: 0.55                                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Query: "Explain conditional probability"
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                                  │
│  • Receives query + user_id                                     │
│  • Retrieves UserProfile from session manager                   │
│  • Routes to appropriate workflow                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Workflow: "concept_explanation"
                 │ Agents: ["retriever", "content_generation"]
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR._execute_retriever()                   │
│  retriever.chat(                                                │
│      message="Explain conditional probability",                 │
│      user_profile=profile  ← Profile passed here                │
│  )                                                              │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                  RAGChatAgent.chat()                            │
│  1. Check if user_profile provided                              │
│  2. If yes: Build profile context                               │
│  3. Enhance message with context                                │
│  4. Pass to underlying LLM agent                                │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ user_profile exists
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│         RAGChatAgent._build_profile_context()                   │
│                                                                 │
│  Input: UserProfile                                             │
│  ├─ competence_level: "intermediate"                           │
│  ├─ ability_score: 0.55                                        │
│  ├─ strengths: ["algebra", "calculus"]                         │
│  └─ weaknesses: ["probability", "statistics"]                  │
│                                                                 │
│  Processing:                                                    │
│  1. Map competence_level → difficulty_level                    │
│     "intermediate" → "intermediate"                            │
│                                                                 │
│  2. Detect query topic ("conditional probability")             │
│     → matches "probability" in weaknesses                      │
│     → lower difficulty to "basic"                              │
│                                                                 │
│  3. Build context string                                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PROFILE CONTEXT STRING                        │
│                                                                 │
│  [User Profile Context for Personalized Content Retrieval]     │
│  Student Level: Intermediate (retrieve 'intermediate' content) │
│  Ability Score: 0.55                                            │
│  Strong Topics: algebra, calculus                               │
│  Areas for Improvement: probability, statistics                 │
│  (Provide extra support and simpler explanations for these)     │
│                                                                 │
│  IMPORTANT: Use search_knowledge_base tool with appropriate     │
│  'difficulty_level' parameter based on student's level.         │
│  For weak topics, consider retrieving prerequisite concepts.    │
│                                                                 │
│  User Query: Explain conditional probability                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Enhanced message sent to LLM
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│              LLM AGENT (Claude/GPT) with Tools                  │
│                                                                 │
│  System Prompt includes:                                        │
│  • Output format requirements (Structured Markdown)             │
│  • User Profile Awareness section                               │
│  • Profile-Based Search Strategy                                │
│  • Tool usage guidelines                                        │
│                                                                 │
│  Agent Processing:                                              │
│  1. Reads profile context                                       │
│  2. Identifies "probability" as weak topic                      │
│  3. Decides to use lower difficulty + prerequisites             │
│  4. Plans tool calls                                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL CALL #1                                 │
│  get_prerequisites("conditional probability")                   │
│                                                                 │
│  Returns:                                                       │
│  • "probability basics"                                         │
│  • "sample space"                                               │
│  • "events and outcomes"                                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL CALL #2                                 │
│  search_knowledge_base(                                         │
│      query="conditional probability",                           │
│      chunk_type="definition",                                   │
│      difficulty_level="basic",  ← Lowered from intermediate!   │
│      k=3                                                        │
│  )                                                              │
│                                                                 │
│  RAG System Query:                                              │
│  ├─ Vector search: "conditional probability"                   │
│  ├─ Filter: chunk_type = "definition"                          │
│  ├─ Filter: difficulty_level = "basic"                         │
│  └─ Re-rank by relevance                                        │
│                                                                 │
│  Returns:                                                       │
│  [Chunk 1: Basic definition with simple language]              │
│  [Chunk 2: Basic notation and formula]                         │
│  [Chunk 3: Basic real-world context]                           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL CALL #3                                 │
│  search_knowledge_base(                                         │
│      query="conditional probability examples",                  │
│      chunk_type="example",                                      │
│      difficulty_level="basic",                                  │
│      k=5                        ← More examples for weak topic │
│  )                                                              │
│                                                                 │
│  Returns:                                                       │
│  [Chunk 1: Coin flip example]                                  │
│  [Chunk 2: Dice rolling example]                               │
│  [Chunk 3: Card drawing example]                               │
│  [Chunk 4: Weather probability example]                        │
│  [Chunk 5: Medical test example]                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL CALL #4                                 │
│  search_knowledge_base(                                         │
│      query="conditional probability",                           │
│      chunk_type="analogy",                                      │
│      difficulty_level="basic",                                  │
│      k=2                                                        │
│  )                                                              │
│                                                                 │
│  Returns:                                                       │
│  [Chunk 1: Filtering information analogy]                      │
│  [Chunk 2: Real-world scenario analogy]                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ All retrieval complete
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│              LLM SYNTHESIZES RESPONSE                           │
│                                                                 │
│  Using:                                                         │
│  • Prerequisites identified                                     │
│  • Basic definitions (3 chunks)                                 │
│  • Multiple examples (5 chunks)                                 │
│  • Helpful analogies (2 chunks)                                 │
│  • Student's profile (intermediate but weak in probability)     │
│  • Strong topics (algebra, calculus) for connections            │
│                                                                 │
│  Strategy:                                                      │
│  1. Start with prerequisites                                    │
│  2. Present definition simply                                   │
│  3. Use many concrete examples                                  │
│  4. Add analogies for intuition                                 │
│  5. Connect to algebra (student's strength)                     │
│  6. Avoid overwhelming with formalism                           │
│  7. Format in structured Markdown                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                FINAL PERSONALIZED RESPONSE                      │
│                                                                 │
│  # Conditional Probability Explained                            │
│                                                                 │
│  ## 1. Retrieved Content                                        │
│  ### 1.1 Prerequisites                                          │
│  Before diving into conditional probability, let's review:      │
│  - Probability basics: P(A) measures likelihood of event A      │
│  - Sample space: All possible outcomes                          │
│  - Events: Subsets of the sample space                          │
│                                                                 │
│  ### 1.2 Definitions                                            │
│  [Simple, clear definition from basic difficulty chunks]        │
│                                                                 │
│  ### 1.3 Examples                                               │
│  [5 concrete examples, progressively building understanding]    │
│  1. Coin flip example (very simple)                            │
│  2. Dice rolling (slightly more complex)                        │
│  ... [more examples]                                            │
│                                                                 │
│  ### 1.4 Analogies                                              │
│  [2 relatable analogies for intuition]                          │
│                                                                 │
│  ## 2. Expert Explanation                                       │
│  [LLM's own explanation, building from examples]                │
│  [Connections to algebra: "Like solving for x given y=5..."]   │
│  [Step-by-step breakdown]                                       │
│  [Visual description]                                           │
│                                                                 │
│  ## 3. Extensions                                               │
│  [Additional practice suggestions]                              │
│  [Connection to stronger topics: calculus integration]          │
│                                                                 │
│  ## 4. Next Steps                                               │
│  • Practice with simple examples first                          │
│  • Once comfortable, explore Bayes' theorem                     │
│  • Let me know if you want worked solutions!                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                  BACK TO ORCHESTRATOR                           │
│  • Receives personalized response from retriever                │
│  • May pass to content_generation agent if needed               │
│  • Synthesizes final response                                   │
│  • Logs execution trace                                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RETURN TO CLIENT                             │
│  {                                                              │
│    "query_type": "concept_explanation",                         │
│    "agents_used": ["retriever", "content_generation"],          │
│    "final_response": "# Conditional Probability...",            │
│    "metadata": {                                                │
│      "duration_ms": 2150,                                       │
│      "user_level": "intermediate",                              │
│      "content_difficulty": "basic",  ← Adjusted for weakness   │
│      "prerequisites_checked": true                              │
│    }                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Comparison: With vs Without Profile

### Without Profile (Default)

```
Query: "Explain conditional probability"
   ↓
Retriever: No profile context
   ↓
LLM: Use default intermediate difficulty
   ↓
search_knowledge_base(query="...", difficulty_level="intermediate")
   ↓
Returns: Standard intermediate content
   ↓
Response: Generic explanation
```

### With Profile (Personalized)

```
Query: "Explain conditional probability"
Profile: intermediate level, probability is a weakness
   ↓
Retriever: Builds profile context with weaknesses
   ↓
LLM: Recognizes probability is weak topic
   ↓
Strategy:
  1. Check prerequisites
  2. Use basic difficulty (one level down)
  3. Get multiple examples
  4. Include analogies
   ↓
search_knowledge_base(..., difficulty_level="basic", k=5)
get_prerequisites(...)
   ↓
Returns: Personalized content with extra support
   ↓
Response: Tailored explanation with scaffolding
```

## Difficulty Level Mapping

```
┌──────────────────────────────────────────────────────────────────┐
│               COMPETENCE → DIFFICULTY MAPPING                     │
└──────────────────────────────────────────────────────────────────┘

User Profile            Query Topic         Retrieval Difficulty
────────────────────────────────────────────────────────────────────
beginner                strong topic    →   intermediate (up 1)
beginner                weak topic      →   basic (no change)
beginner                new topic       →   basic (default)

intermediate            strong topic    →   advanced (up 1)
intermediate            weak topic      →   basic (down 1)
intermediate            new topic       →   intermediate (default)

advanced                strong topic    →   advanced (no change, max)
advanced                weak topic      →   intermediate (down 1)
advanced                new topic       →   advanced (default)
────────────────────────────────────────────────────────────────────

Legend:
• strong topic: In user_profile.strengths
• weak topic: In user_profile.weaknesses
• new topic: Not in strengths or weaknesses
```

## Key Decision Points

```
┌─────────────────────────────────────────────────────────────────┐
│         PROFILE-BASED DECISION TREE                             │
└─────────────────────────────────────────────────────────────────┘

Query received with user_profile
    │
    ├─ Has profile?
    │  ├─ Yes → Extract topics from query
    │  │       │
    │  │       ├─ Topic in weaknesses?
    │  │       │  ├─ Yes → Lower difficulty
    │  │       │  │       → Check prerequisites
    │  │       │  │       → Get more examples
    │  │       │  │       → Add analogies
    │  │       │  │
    │  │       │  └─ No → Topic in strengths?
    │  │       │         ├─ Yes → Raise difficulty
    │  │       │         │       → Advanced content
    │  │       │         │       → Less hand-holding
    │  │       │         │
    │  │       │         └─ No → Use default level
    │  │       │                → Standard content
    │  │
    │  └─ No → Use default intermediate difficulty
    │          → No personalization
    │
    └─ Retrieve and synthesize
```

This visual guide shows exactly how the profile-based retrieval system personalizes content for each student! 🎯
