"""
Report Agent - Main agent implementation.
Generates comprehensive learning progress reports and analytics.
"""

from strands import Agent
from strands.models import BedrockModel
from typing import Optional
import logging
from pathlib import Path

from agents.report.config import ReportConfig
from agents.report.prompts import AGENT_INSTRUCTIONS
from agents.report.tools import report_agent_tools
from database.database import initialize_database

logger = logging.getLogger(__name__)


class ReportAgent:
    """
    Report Agent for generating learning progress analytics and reports.
    
    This agent analyzes student performance data over time, identifies trends,
    and provides actionable insights and recommendations for improvement.
    """
    
    def __init__(self, config: Optional[ReportConfig] = None):
        """
        Initialize the Report Agent.
        
        Args:
            config: Optional configuration object. Uses default if not provided.
        """
        self.config = config or ReportConfig()
        self.agent = self._create_agent()
        
        # Initialize the database (ensure tables exist)
        initialize_database()
    
    def _create_agent(self) -> Agent:
        """Create and configure the Strands agent."""
        # Create a configured Bedrock model
        model = BedrockModel(
            model_id=self.config.MODEL_ID,
            streaming=False,
        )
        
        try:
            agent = Agent(
                name=self.config.AGENT_NAME,
                model=model,
                system_prompt=AGENT_INSTRUCTIONS,
                tools=report_agent_tools,
                description=self.config.AGENT_DESCRIPTION,
            )
            logger.info(f"✅ {self.config.AGENT_NAME} created successfully with {len(report_agent_tools)} tools")
        except Exception as e:
            logger.error(f"❌ Failed to create {self.config.AGENT_NAME}: {e}")
            raise
        
        return agent
    
    def generate_report(
        self,
        user_session_id: str,
        days: int = None,
        report_type: str = "comprehensive"
    ) -> str:
        """
        Generate a learning progress report for a user.
        
        Args:
            user_session_id: User's session ID
            days: Number of days to include in report (default: from config)
            report_type: Type of report ("comprehensive", "quick", "detailed")
            
        Returns:
            Generated report as a string
        """
        days = days or self.config.DEFAULT_PERIOD_DAYS
        
        logger.info(f"Generating {report_type} report for user {user_session_id}, period: {days} days")
        
        if report_type == "comprehensive":
            prompt = f"""Generate a comprehensive learning progress report for user with session ID: {user_session_id}

The report should cover the last {days} days and include:
1. Overall performance summary
2. Quiz performance trends
3. Topic mastery analysis
4. Learning time and engagement statistics
5. Visual charts and graphs (use render_progress_charts tool with chart_type="dashboard")
6. Specific recommendations for improvement

IMPORTANT VISUALIZATION INSTRUCTIONS:
- Use the render_progress_charts tool to create chart images for the frontend
- DO NOT include markdown links like [View Dashboard](url) in your response
- DO NOT include image syntax like ![Chart](url) in your response  
- OnNLY mention the file path or URL at the end of the report
- The frontend will automatically detect and display the charts

Use all available tools to gather complete data and provide insightful analysis.
Make the report encouraging, data-driven, and actionable."""

        elif report_type == "quick":
            prompt = f"""Generate a quick progress summary for user with session ID: {user_session_id}

Cover the last {days} days with:
- Current accuracy and ability score
- Recent quiz performance
- Key strengths and areas to improve
- 2-3 specific recommendations

Keep it concise but informative."""

        elif report_type == "detailed":
            prompt = f"""Generate a detailed analytical report for user with session ID: {user_session_id}

Analyze the last {days} days in depth:
1. Progress history with time-series analysis
2. Detailed quiz performance breakdown
3. Topic-by-topic mastery assessment
4. Learning time patterns and engagement
5. Performance comparisons across time periods
6. Comprehensive recommendations with reasoning

Provide deep insights backed by data."""

        else:
            prompt = f"Generate a learning progress report for user {user_session_id} covering the last {days} days."
        
        try:
            # Call the agent
            response = self.agent(prompt)
            logger.info("Report generated successfully")
            return str(response)
        
        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            return f"Error generating report: {str(e)}"
    
    def analyze_progress(
        self,
        user_session_id: str,
        days: int = None
    ) -> str:
        """
        Analyze progress trends for a user.
        
        Args:
            user_session_id: User's session ID
            days: Number of days to analyze
            
        Returns:
            Progress analysis as a string
        """
        days = days or self.config.DEFAULT_PERIOD_DAYS
        
        prompt = f"""Analyze the learning progress and trends for user with session ID: {user_session_id}

Focus on the last {days} days and identify:
1. Overall trend (improving, declining, or stable)
2. Performance consistency
3. Areas of improvement
4. Areas of concern
5. Pattern recognition (e.g., better performance on certain days, topics, etc.)

Provide specific insights with supporting data."""
        
        try:
            response = self.agent(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"Error analyzing progress: {e}", exc_info=True)
            return f"Error analyzing progress: {str(e)}"
    
    def get_recommendations(
        self,
        user_session_id: str
    ) -> str:
        """
        Get personalized learning recommendations for a user.
        
        Args:
            user_session_id: User's session ID
            
        Returns:
            Recommendations as a string
        """
        prompt = f"""Based on the learning progress data for user with session ID: {user_session_id}, 
provide personalized recommendations including:

1. Topics that need immediate attention (prioritized)
2. Suggested learning strategies
3. Practice activity recommendations
4. Study schedule suggestions
5. Motivational guidance

Make recommendations specific, actionable, and encouraging."""
        
        try:
            response = self.agent(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            return f"Error generating recommendations: {str(e)}"
    
    def compare_periods(
        self,
        user_session_id: str,
        recent_days: int = 7,
        previous_days: int = 14
    ) -> str:
        """
        Compare performance between two time periods.
        
        Args:
            user_session_id: User's session ID
            recent_days: Days for recent period
            previous_days: Days for previous period
            
        Returns:
            Comparison analysis as a string
        """
        prompt = f"""Compare the learning performance for user with session ID: {user_session_id}
between two time periods:
- Recent period: last {recent_days} days
- Previous period: {previous_days-recent_days} days before that

Analyze:
1. Performance changes (improvement or decline)
2. What changed between the periods
3. Possible reasons for the changes
4. Recommendations based on the comparison

Provide clear insights about the user's learning trajectory."""
        
        try:
            response = self.agent(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"Error comparing periods: {e}", exc_info=True)
            return f"Error comparing periods: {str(e)}"
    
    def get_visualizations(
        self,
        user_session_id: str,
        days: int = None,
        format: str = "markdown"
    ) -> str:
        """
        Generate visualization data for charts and graphs.
        
        Args:
            user_session_id: User's session ID
            days: Number of days to include (default: from config)
            format: "json" for chart.js compatible data, "markdown" for text visualization
            
        Returns:
            Visualization data as JSON or formatted text
        """
        days = days or self.config.DEFAULT_PERIOD_DAYS
        
        prompt = f"""Generate visualizations for user with session ID: {user_session_id}

Create visual representations of:
1. Progress over time (line chart)
2. Performance by difficulty (bar chart)
3. Topic mastery levels (horizontal bar chart)
4. Quiz performance trends (line chart with moving average)
5. Learning time distribution (bar chart)
6. Topic distribution (pie chart)
7. Consistency score (gauge)

Use the generate_progress_visualizations tool with format="{format}" and days={days}.
After getting the data, provide a brief interpretation of what the visualizations show."""
        
        try:
            response = self.agent(prompt)
            return str(response)
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}", exc_info=True)
            return f"Error generating visualizations: {str(e)}"
    
    def chat(
        self,
        message: str,
        user_session_id: Optional[str] = None
    ) -> str:
        """
        General chat interface for report-related queries.
        
        Args:
            message: User's message/query
            user_session_id: Optional user session ID for context
            
        Returns:
            Agent response as a string
        """
        if user_session_id:
            context = f"[User Session ID: {user_session_id}]\n\n"
            message = context + message
        
        try:
            response = self.agent(message)
            return str(response)
        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            return f"Error processing request: {str(e)}"


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_report_agent(config: Optional[ReportConfig] = None) -> ReportAgent:
    """
    Factory function to create ReportAgent instance.
    
    Args:
        config: Optional configuration
        
    Returns:
        Configured ReportAgent
    """
    return ReportAgent(config=config)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 70)
    print("Testing ReportAgent")
    print("=" * 70)
    
    # Create agent
    agent = create_report_agent()
    
    # Test with a sample session ID (would need real data)
    test_session_id = "test_user_123"
    
    print("\n" + "=" * 70)
    print("Test 1: Generate Comprehensive Report")
    print("=" * 70)
    
    report = agent.generate_report(
        user_session_id=test_session_id,
        days=7,
        report_type="comprehensive"
    )
    print(report)
    
    print("\n" + "=" * 70)
    print("Test 2: Get Recommendations")
    print("=" * 70)
    
    recommendations = agent.get_recommendations(user_session_id=test_session_id)
    print(recommendations)
