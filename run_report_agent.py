#!/usr/bin/env python3
"""
Run Report Agent - Standalone test script for the Report Agent.

This script demonstrates how to use the Report Agent to generate
learning progress reports and analytics.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.report.agent import ReportAgent
from database.database import initialize_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to test the Report Agent."""
    
    print("=" * 80)
    print("REPORT AGENT - TEST SCRIPT")
    print("=" * 80)
    print()
    
    # Initialize database
    print("Initializing database...")
    initialize_database()
    print("✓ Database initialized")
    print()
    
    # Create Report Agent
    print("Creating Report Agent...")
    try:
        agent = ReportAgent()
        print("✓ Report Agent created successfully")
    except Exception as e:
        print(f"✗ Failed to create Report Agent: {e}")
        return
    print()
    
    # Get user session ID from input
    print("=" * 80)
    print("GENERATE LEARNING PROGRESS REPORT")
    print("=" * 80)
    print()
    
    user_session_id = input("Enter user session ID (or press Enter for demo): ").strip()
    
    if not user_session_id:
        user_session_id = "demo_user_123"
        print(f"Using demo session ID: {user_session_id}")
    
    print()
    print(f"User Session ID: {user_session_id}")
    print()
    
    # Menu for different report types
    print("Select report type:")
    print("1. Comprehensive Report (7 days)")
    print("2. Quick Summary (7 days)")
    print("3. Detailed Analysis (30 days)")
    print("4. Progress Trends (14 days)")
    print("5. Personalized Recommendations")
    print("6. Compare Time Periods")
    print()
    
    choice = input("Enter choice (1-6) or press Enter for comprehensive: ").strip()
    
    if not choice:
        choice = "1"
    
    print()
    print("=" * 80)
    print("GENERATING REPORT...")
    print("=" * 80)
    print()
    
    try:
        if choice == "1":
            # Comprehensive Report
            print("Report Type: Comprehensive Report (7 days)")
            print()
            result = agent.generate_report(
                user_session_id=user_session_id,
                days=7,
                report_type="comprehensive"
            )
            
        elif choice == "2":
            # Quick Summary
            print("Report Type: Quick Summary (7 days)")
            print()
            result = agent.generate_report(
                user_session_id=user_session_id,
                days=7,
                report_type="quick"
            )
            
        elif choice == "3":
            # Detailed Analysis
            print("Report Type: Detailed Analysis (30 days)")
            print()
            result = agent.generate_report(
                user_session_id=user_session_id,
                days=30,
                report_type="detailed"
            )
            
        elif choice == "4":
            # Progress Trends
            print("Report Type: Progress Trends (14 days)")
            print()
            result = agent.analyze_progress(
                user_session_id=user_session_id,
                days=14
            )
            
        elif choice == "5":
            # Recommendations
            print("Report Type: Personalized Recommendations")
            print()
            result = agent.get_recommendations(
                user_session_id=user_session_id
            )
            
        elif choice == "6":
            # Compare Periods
            print("Report Type: Time Period Comparison")
            print()
            result = agent.compare_periods(
                user_session_id=user_session_id,
                recent_days=7,
                previous_days=14
            )
            
        else:
            print("Invalid choice. Running comprehensive report...")
            result = agent.generate_report(
                user_session_id=user_session_id,
                days=7,
                report_type="comprehensive"
            )
        
        print()
        print("=" * 80)
        print("REPORT GENERATED")
        print("=" * 80)
        print()
        print(result)
        print()
        
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        print(f"\n✗ Error: {e}\n")
        return
    
    print()
    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
