"""
Test Profile-Based Intelligent Retrieval
Verifies that the RAG agent properly uses user profiles for personalization.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.retrieval.agent import create_rag_chat_agent
from shared.models import UserProfile


def test_beginner_weak_topic():
    """Test retrieval for beginner student on weak topic."""
    print("=" * 70)
    print("TEST 1: Beginner Student - Weak Topic (Probability)")
    print("=" * 70)
    
    # Create beginner profile with probability weakness
    profile = UserProfile(
        user_id="test_beginner",
        session_id="session_001",
        competence_level="beginner",
        ability_score=0.25,
        final_score=0.30,
        strengths=[],
        weaknesses=["probability", "statistics"]
    )
    
    agent = create_rag_chat_agent()
    
    query = "Explain conditional probability"
    print(f"\nUser Profile:")
    print(f"  Level: {profile.competence_level}")
    print(f"  Ability Score: {profile.ability_score}")
    print(f"  Weaknesses: {profile.weaknesses}")
    print(f"\nQuery: {query}")
    print(f"\nExpected Behavior:")
    print(f"  - Should use 'basic' difficulty level")
    print(f"  - Should provide extra examples and analogies")
    print(f"  - May check prerequisites")
    
    print(f"\n{'='*70}")
    print("Response:")
    print(f"{'='*70}\n")
    
    response = agent.chat(query, user_profile=profile)
    print(response)


def test_advanced_strong_topic():
    """Test retrieval for advanced student on strong topic."""
    print("\n" + "=" * 70)
    print("TEST 2: Advanced Student - Strong Topic (Calculus)")
    print("=" * 70)
    
    # Create advanced profile with calculus strength
    profile = UserProfile(
        user_id="test_advanced",
        session_id="session_002",
        competence_level="advanced",
        ability_score=0.88,
        final_score=0.92,
        strengths=["calculus", "linear algebra", "analysis"],
        weaknesses=[]
    )
    
    agent = create_rag_chat_agent()
    
    query = "Explain the relationship between probability and measure theory"
    print(f"\nUser Profile:")
    print(f"  Level: {profile.competence_level}")
    print(f"  Ability Score: {profile.ability_score}")
    print(f"  Strengths: {profile.strengths}")
    print(f"\nQuery: {query}")
    print(f"\nExpected Behavior:")
    print(f"  - Should use 'advanced' difficulty level")
    print(f"  - Should provide rigorous explanations")
    print(f"  - May include proofs and advanced applications")
    
    print(f"\n{'='*70}")
    print("Response:")
    print(f"{'='*70}\n")
    
    response = agent.chat(query, user_profile=profile)
    print(response)


def test_intermediate_mixed_topics():
    """Test retrieval for intermediate student with mixed strengths/weaknesses."""
    print("\n" + "=" * 70)
    print("TEST 3: Intermediate Student - Mixed Topics")
    print("=" * 70)
    
    # Create intermediate profile with mixed strengths/weaknesses
    profile = UserProfile(
        user_id="test_intermediate",
        session_id="session_003",
        competence_level="intermediate",
        ability_score=0.55,
        final_score=0.60,
        strengths=["algebra", "geometry"],
        weaknesses=["probability", "combinatorics"]
    )
    
    agent = create_rag_chat_agent()
    
    query = "How does probability relate to counting problems?"
    print(f"\nUser Profile:")
    print(f"  Level: {profile.competence_level}")
    print(f"  Ability Score: {profile.ability_score}")
    print(f"  Strengths: {profile.strengths}")
    print(f"  Weaknesses: {profile.weaknesses}")
    print(f"\nQuery: {query}")
    print(f"\nExpected Behavior:")
    print(f"  - Should bridge from algebra (strength) to probability (weakness)")
    print(f"  - Should use 'basic' difficulty for probability/combinatorics")
    print(f"  - Should provide connecting examples")
    
    print(f"\n{'='*70}")
    print("Response:")
    print(f"{'='*70}\n")
    
    response = agent.chat(query, user_profile=profile)
    print(response)


def test_no_profile():
    """Test retrieval without profile (default behavior)."""
    print("\n" + "=" * 70)
    print("TEST 4: No User Profile (Default Behavior)")
    print("=" * 70)
    
    agent = create_rag_chat_agent()
    
    query = "What is a random variable?"
    print(f"\nQuery: {query}")
    print(f"\nExpected Behavior:")
    print(f"  - Should use default/intermediate difficulty")
    print(f"  - No personalization applied")
    print(f"  - Standard educational content")
    
    print(f"\n{'='*70}")
    print("Response:")
    print(f"{'='*70}\n")
    
    response = agent.chat(query)  # No profile
    print(response)


def test_profile_context_building():
    """Test that profile context is built correctly."""
    print("\n" + "=" * 70)
    print("TEST 5: Profile Context Building")
    print("=" * 70)
    
    agent = create_rag_chat_agent()
    
    # Test various profile scenarios
    profiles = [
        UserProfile(
            user_id="test_1",
            session_id="s1",
            competence_level="beginner",
            ability_score=0.2,
            final_score=0.25,
            strengths=[],
            weaknesses=["probability"]
        ),
        UserProfile(
            user_id="test_2",
            session_id="s2",
            competence_level="intermediate",
            ability_score=0.6,
            final_score=0.65,
            strengths=["algebra", "calculus"],
            weaknesses=["statistics"]
        ),
        UserProfile(
            user_id="test_3",
            session_id="s3",
            competence_level="advanced",
            ability_score=0.9,
            final_score=0.92,
            strengths=["all topics"],
            weaknesses=[]
        ),
    ]
    
    for i, profile in enumerate(profiles, 1):
        print(f"\nProfile {i}:")
        print(f"  Level: {profile.competence_level}")
        print(f"  Ability: {profile.ability_score}")
        print(f"  Strengths: {profile.strengths}")
        print(f"  Weaknesses: {profile.weaknesses}")
        
        # Build context
        context = agent._build_profile_context(profile)
        print(f"\nGenerated Context:")
        print("-" * 50)
        print(context)
        print("-" * 50)


def run_all_tests():
    """Run all profile-based retrieval tests."""
    print("\n" + "=" * 70)
    print("PROFILE-BASED INTELLIGENT RETRIEVAL TESTS")
    print("=" * 70 + "\n")
    
    tests = [
        test_profile_context_building,
        test_beginner_weak_topic,
        test_intermediate_mixed_topics,
        test_advanced_strong_topic,
        test_no_profile,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n❌ Test {test.__name__} failed: {e}\n")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    import logging
    
    # Reduce noise from RAG system initialization
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set RAG agent logger to INFO to see important messages
    rag_logger = logging.getLogger('agents.retrieval.agent')
    rag_logger.setLevel(logging.INFO)
    
    run_all_tests()
