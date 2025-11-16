"""
Example Orchestrator - Shows how to integrate the Onboarding Agent

This is a simplified example showing how the onboarding agent
fits into your larger agentic workflow as a mandatory prerequisite.
"""

from typing import Dict, Optional
from strands import Agent, tool
from agents.onboarding import OnboardingAgent
from shared.models import UserProfile


class LearningOrchestrator:
    """
    Main orchestrator that coordinates multiple agents.
    
    Architecture:
    1. Onboarding Agent (mandatory first step)
    2. Learning Path Agent (uses profile)
    3. Content Generation Agent (uses profile)
    4. Assessment Agent (uses profile)
    
    The orchestrator maintains shared memory (user profiles) that
    all agents can access.
    """
    
    def __init__(self):
        """Initialize orchestrator with shared memory and agents."""
        # Shared memory - stores user profiles
        self.user_profiles: Dict[str, UserProfile] = {}
        
        # Initialize agents
        self.onboarding_agent = OnboardingAgent()
        
        # The orchestrator agent coordinates everything
        self.agent = self._create_orchestrator_agent()
    
    def _create_orchestrator_agent(self) -> Agent:
        """Create the main orchestrator agent with all tools."""
        
        @tool
        def check_user_profile(user_id: str) -> dict:
            """
            Check if user has completed onboarding.
            
            Args:
                user_id: User identifier
            
            Returns:
                Profile status and data if available
            """
            if user_id in self.user_profiles:
                profile = self.user_profiles[user_id]
                return {
                    "status": "exists",
                    "profile": profile.to_dict(),
                    "message": f"User has completed onboarding. Competence: {profile.competence_level}"
                }
            else:
                return {
                    "status": "not_found",
                    "message": "User needs to complete onboarding assessment first."
                }
        
        @tool
        def run_onboarding(user_id: str, total_questions: Optional[int] = None) -> dict:
            """
            Run mandatory onboarding assessment for new user.
            
            This is the FIRST mandatory step for all new users.
            It generates a UserProfile that other agents will use.
            
            Args:
                user_id: User identifier
                total_questions: Optional override for quiz length
            
            Returns:
                Assessment results and generated profile
            """
            try:
                # Check if already completed
                if user_id in self.user_profiles:
                    return {
                        "status": "already_completed",
                        "message": "User has already completed onboarding.",
                        "profile": self.user_profiles[user_id].to_dict()
                    }
                
                # Run onboarding assessment
                # Note: In practice, this would be interactive
                # For now, we'll simulate it
                profile = self._simulate_onboarding(user_id, total_questions)
                
                # Store in shared memory
                self.user_profiles[user_id] = profile
                
                return {
                    "status": "completed",
                    "message": "Onboarding assessment completed successfully!",
                    "profile": profile.to_dict(),
                    "competence_level": profile.competence_level,
                    "recommendations": {
                        "starting_level": profile.recommended_starting_level,
                        "learning_pace": profile.learning_pace,
                        "focus_topics": profile.suggested_topics[:3]
                    }
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Onboarding failed: {str(e)}"
                }
        
        @tool
        def get_learning_path(user_id: str) -> dict:
            """
            Generate personalized learning path based on user profile.
            
            This tool represents a "Learning Path Agent" that uses
            the profile from onboarding to customize the curriculum.
            
            Args:
                user_id: User identifier
            
            Returns:
                Personalized learning path
            """
            # Check profile exists
            if user_id not in self.user_profiles:
                return {
                    "status": "error",
                    "message": "User profile not found. Complete onboarding first."
                }
            
            profile = self.user_profiles[user_id]
            
            # Generate path based on competence
            if profile.competence_level == "easy":
                path = [
                    "Basic Probability Concepts",
                    "Sample Spaces and Events",
                    "Basic Probability Rules",
                    "Simple Combinations"
                ]
            elif profile.competence_level == "medium":
                path = [
                    "Review: Basic Concepts",
                    "Conditional Probability",
                    "Independence",
                    "Bayes' Theorem (intro)",
                    "Advanced Combinations"
                ]
            else:  # difficult
                path = [
                    "Review: Conditional Probability",
                    "Advanced Bayes' Theorem",
                    "Probability Distributions",
                    "Expected Value and Variance",
                    "Continuous Probability"
                ]
            
            # Add topics from weaknesses
            if profile.weaknesses:
                path.insert(0, f"Focus Area: {profile.weaknesses[0]}")
            
            return {
                "status": "success",
                "user_id": user_id,
                "competence_level": profile.competence_level,
                "learning_path": path,
                "recommended_pace": profile.learning_pace,
                "estimated_duration": f"{len(path) * 2} weeks"
            }
        
        @tool
        def generate_content(user_id: str, topic: str) -> dict:
            """
            Generate personalized content for a topic.
            
            This tool represents a "Content Generation Agent" that
            adapts content difficulty based on user profile.
            
            Args:
                user_id: User identifier
                topic: Topic to generate content for
            
            Returns:
                Personalized content
            """
            if user_id not in self.user_profiles:
                return {
                    "status": "error",
                    "message": "User profile not found."
                }
            
            profile = self.user_profiles[user_id]
            
            # Adjust content based on competence
            difficulty_level = {
                "easy": "beginner-friendly with lots of examples",
                "medium": "intermediate with some challenges",
                "difficult": "advanced with complex problems"
            }[profile.competence_level]
            
            return {
                "status": "success",
                "topic": topic,
                "difficulty": difficulty_level,
                "content_sample": f"Content for '{topic}' tailored to {profile.competence_level} level...",
                "includes_examples": True,
                "includes_practice": True
            }
        
        # Create orchestrator agent
        return Agent(
            name="LearningOrchestrator",
            instructions="""
            You are the main orchestrator for a learning management system.
            You coordinate multiple specialized agents to provide personalized learning.
            
            WORKFLOW FOR NEW USERS:
            1. Check if user has profile (use check_user_profile)
            2. If NO profile: Run onboarding assessment (use run_onboarding) - MANDATORY
            3. Once profile exists: 
               - Generate learning path (use get_learning_path)
               - Generate content as needed (use generate_content)
            
            WORKFLOW FOR EXISTING USERS:
            1. Retrieve profile (use check_user_profile)
            2. Continue with learning path or content generation
            
            Always be helpful and guide users through their learning journey!
            """,
            tools=[
                check_user_profile,
                run_onboarding,
                get_learning_path,
                generate_content
            ],
            description="Main orchestrator coordinating learning agents"
        )
    
    def _simulate_onboarding(self, user_id: str, total_questions: Optional[int]) -> UserProfile:
        """
        Simulate onboarding assessment.
        
        In production, this would be interactive with the onboarding agent.
        For this example, we'll create a sample profile.
        """
        # In real implementation, you would:
        # return self.onboarding_agent.assess_user(user_id, total_questions)
        
        # For now, create a sample profile
        from datetime import datetime
        
        return UserProfile(
            user_id=user_id,
            session_id="sample_session",
            competence_level="medium",
            ability_score=0.58,
            final_score=72.0,
            easy_correct=5,
            easy_total=6,
            medium_correct=10,
            medium_total=13,
            difficult_correct=3,
            difficult_total=6,
            easy_accuracy=83.3,
            medium_accuracy=76.9,
            difficult_accuracy=50.0,
            overall_accuracy=72.0,
            strengths=["basic_probability_concepts", "combinations"],
            weaknesses=["conditional_probability", "bayes_theorem"],
            recommended_starting_level="intermediate",
            suggested_topics=["conditional_probability", "bayes_theorem", "independence"],
            learning_pace="normal",
            total_questions=total_questions or 25,
            questions_answered=25,
            onboarding_completed=True,
            onboarding_completed_at=datetime.utcnow()
        )
    
    def handle_new_student(self, user_id: str) -> str:
        """
        Entry point for new students.
        
        Args:
            user_id: Student identifier
        
        Returns:
            Orchestrator's response
        """
        message = f"New student '{user_id}' has joined. Please help them get started."
        return self.agent(message)
    
    def handle_existing_student(self, user_id: str, request: str) -> str:
        """
        Handle request from existing student.
        
        Args:
            user_id: Student identifier
            request: Student's request
        
        Returns:
            Orchestrator's response
        """
        message = f"Student '{user_id}' asks: {request}"
        return self.agent(message)
    
    def __call__(self, message: str) -> str:
        """Make orchestrator callable."""
        return self.agent(message)


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("  Example Orchestrator with Onboarding Agent")
    print("=" * 70)
    print()
    
    # Create orchestrator
    orchestrator = LearningOrchestrator()
    
    # Scenario 1: New student
    print("📝 Scenario 1: New Student")
    print("-" * 70)
    response = orchestrator.handle_new_student("student_alice")
    print(f"Response: {response}")
    print()
    
    # Scenario 2: Get learning path
    print("📚 Scenario 2: Generate Learning Path")
    print("-" * 70)
    response = orchestrator.handle_existing_student(
        "student_alice",
        "What should I learn next?"
    )
    print(f"Response: {response}")
    print()
    
    # Scenario 3: Generate content
    print("📖 Scenario 3: Generate Content")
    print("-" * 70)
    response = orchestrator.handle_existing_student(
        "student_alice",
        "Can you explain conditional probability?"
    )
    print(f"Response: {response}")
    print()
    
    print("=" * 70)
    print("  Example Complete!")
    print("=" * 70)
    print()
    print("This shows how the onboarding agent integrates with your orchestrator.")
    print("In production, replace _simulate_onboarding with real agent interaction.")
