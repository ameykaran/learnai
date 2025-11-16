"""
Visualization utilities for the Report Agent.
Generates data structures for charts and graphs.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json


def generate_progress_chart_data(snapshots: List[Dict]) -> Dict[str, Any]:
    """
    Generate data for a line chart showing progress over time.
    
    Returns:
        Chart data with labels, datasets, and configuration
    """
    if not snapshots:
        return {
            "type": "line",
            "labels": [],
            "datasets": []
        }
    
    # Sort by timestamp
    sorted_snapshots = sorted(snapshots, key=lambda x: x['timestamp'])
    
    labels = [
        datetime.fromisoformat(s['timestamp']).strftime('%Y-%m-%d') 
        for s in sorted_snapshots
    ]
    
    return {
        "type": "line",
        "title": "Learning Progress Over Time",
        "labels": labels,
        "datasets": [
            {
                "label": "Overall Accuracy",
                "data": [s['overall_accuracy'] for s in sorted_snapshots],
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "tension": 0.1
            },
            {
                "label": "Ability Score (x100)",
                "data": [s['ability_score'] * 100 for s in sorted_snapshots],
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "tension": 0.1
            }
        ],
        "options": {
            "responsive": True,
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 100,
                    "title": {"display": True, "text": "Score (%)"}
                },
                "x": {
                    "title": {"display": True, "text": "Date"}
                }
            }
        }
    }


def generate_difficulty_breakdown_chart(snapshots: List[Dict]) -> Dict[str, Any]:
    """
    Generate data for a bar chart showing performance by difficulty.
    Uses the most recent snapshot.
    """
    if not snapshots:
        return {"type": "bar", "labels": [], "datasets": []}
    
    latest = sorted(snapshots, key=lambda x: x['timestamp'])[-1]
    
    return {
        "type": "bar",
        "title": "Performance by Difficulty Level",
        "labels": ["Easy", "Medium", "Difficult"],
        "datasets": [
            {
                "label": "Accuracy (%)",
                "data": [
                    latest.get('easy_accuracy', 0),
                    latest.get('medium_accuracy', 0),
                    latest.get('difficult_accuracy', 0)
                ],
                "backgroundColor": [
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(255, 206, 86, 0.6)",
                    "rgba(255, 99, 132, 0.6)"
                ],
                "borderColor": [
                    "rgb(75, 192, 192)",
                    "rgb(255, 206, 86)",
                    "rgb(255, 99, 132)"
                ],
                "borderWidth": 1
            }
        ],
        "options": {
            "responsive": True,
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 100,
                    "title": {"display": True, "text": "Accuracy (%)"}
                }
            }
        }
    }


def generate_topic_mastery_chart(topic_mastery: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Generate data for a horizontal bar chart showing topic mastery levels.
    """
    if not topic_mastery:
        return {"type": "horizontalBar", "labels": [], "datasets": []}
    
    # Sort by mastery level
    sorted_topics = sorted(
        topic_mastery.items(),
        key=lambda x: x[1].get('mastery_level', 0),
        reverse=True
    )
    
    topics = [item[0] for item in sorted_topics]
    mastery_levels = [item[1].get('mastery_level', 0) * 100 for item in sorted_topics]
    accuracies = [
        (item[1].get('correct_count', 0) / item[1].get('total_count', 1) * 100) 
        if item[1].get('total_count', 0) > 0 else 0
        for item in sorted_topics
    ]
    
    return {
        "type": "horizontalBar",
        "title": "Topic Mastery Levels",
        "labels": topics,
        "datasets": [
            {
                "label": "Mastery Level",
                "data": mastery_levels,
                "backgroundColor": "rgba(54, 162, 235, 0.6)",
                "borderColor": "rgb(54, 162, 235)",
                "borderWidth": 1
            },
            {
                "label": "Accuracy",
                "data": accuracies,
                "backgroundColor": "rgba(75, 192, 192, 0.6)",
                "borderColor": "rgb(75, 192, 192)",
                "borderWidth": 1
            }
        ],
        "options": {
            "indexAxis": "y",
            "responsive": True,
            "scales": {
                "x": {
                    "beginAtZero": True,
                    "max": 100,
                    "title": {"display": True, "text": "Score (%)"}
                }
            }
        }
    }


def generate_quiz_performance_trend_chart(quiz_history: List[Dict]) -> Dict[str, Any]:
    """
    Generate data for a line chart showing quiz scores over time.
    """
    if not quiz_history:
        return {"type": "line", "labels": [], "datasets": []}
    
    # Sort by attempt date
    sorted_quizzes = sorted(quiz_history, key=lambda x: x['attempted_at'])
    
    labels = [
        datetime.fromisoformat(q['attempted_at']).strftime('%m/%d')
        for q in sorted_quizzes
    ]
    
    scores = [q['score'] for q in sorted_quizzes]
    
    # Calculate moving average
    window_size = min(3, len(scores))
    moving_avg = []
    for i in range(len(scores)):
        start = max(0, i - window_size + 1)
        moving_avg.append(sum(scores[start:i+1]) / (i - start + 1))
    
    return {
        "type": "line",
        "title": "Quiz Performance Trend",
        "labels": labels,
        "datasets": [
            {
                "label": "Quiz Score",
                "data": scores,
                "borderColor": "rgb(75, 192, 192)",
                "backgroundColor": "rgba(75, 192, 192, 0.1)",
                "tension": 0.1,
                "pointRadius": 5,
                "pointHoverRadius": 7
            },
            {
                "label": "Moving Average",
                "data": moving_avg,
                "borderColor": "rgb(255, 99, 132)",
                "backgroundColor": "rgba(255, 99, 132, 0.1)",
                "tension": 0.3,
                "borderDash": [5, 5],
                "pointRadius": 0
            }
        ],
        "options": {
            "responsive": True,
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 100,
                    "title": {"display": True, "text": "Score (%)"}
                },
                "x": {
                    "title": {"display": True, "text": "Date"}
                }
            }
        }
    }


def generate_learning_time_chart(snapshots: List[Dict]) -> Dict[str, Any]:
    """
    Generate data for a bar chart showing learning time over days.
    """
    if not snapshots:
        return {"type": "bar", "labels": [], "datasets": []}
    
    # Sort by timestamp
    sorted_snapshots = sorted(snapshots, key=lambda x: x['timestamp'])
    
    # Calculate daily learning time (difference between consecutive snapshots)
    labels = []
    times = []
    
    for i, snapshot in enumerate(sorted_snapshots):
        date_str = datetime.fromisoformat(snapshot['timestamp']).strftime('%m/%d')
        labels.append(date_str)
        
        if i == 0:
            times.append(snapshot.get('learning_time_minutes', 0))
        else:
            prev_time = sorted_snapshots[i-1].get('learning_time_minutes', 0)
            curr_time = snapshot.get('learning_time_minutes', 0)
            daily_time = max(0, curr_time - prev_time)
            times.append(daily_time)
    
    return {
        "type": "bar",
        "title": "Daily Learning Time",
        "labels": labels,
        "datasets": [
            {
                "label": "Minutes",
                "data": times,
                "backgroundColor": "rgba(153, 102, 255, 0.6)",
                "borderColor": "rgb(153, 102, 255)",
                "borderWidth": 1
            }
        ],
        "options": {
            "responsive": True,
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {"display": True, "text": "Minutes"}
                },
                "x": {
                    "title": {"display": True, "text": "Date"}
                }
            }
        }
    }


def generate_topic_distribution_pie_chart(topic_mastery: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Generate data for a pie chart showing question distribution by topic.
    """
    if not topic_mastery:
        return {"type": "pie", "labels": [], "datasets": []}
    
    topics = []
    counts = []
    colors = [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(199, 199, 199, 0.6)',
        'rgba(83, 102, 255, 0.6)',
    ]
    
    for topic, data in topic_mastery.items():
        topics.append(topic)
        counts.append(data.get('total_count', 0))
    
    return {
        "type": "pie",
        "title": "Questions Attempted by Topic",
        "labels": topics,
        "datasets": [
            {
                "label": "Questions",
                "data": counts,
                "backgroundColor": colors[:len(topics)],
                "borderColor": [c.replace('0.6', '1') for c in colors[:len(topics)]],
                "borderWidth": 1
            }
        ],
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {
                    "position": "right"
                }
            }
        }
    }


def generate_consistency_gauge_data(consistency_score: float) -> Dict[str, Any]:
    """
    Generate data for a gauge/meter showing consistency score.
    """
    return {
        "type": "gauge",
        "title": "Performance Consistency",
        "value": round(consistency_score * 100, 1),
        "min": 0,
        "max": 100,
        "ranges": [
            {"from": 0, "to": 40, "color": "rgba(255, 99, 132, 0.6)", "label": "Variable"},
            {"from": 40, "to": 70, "color": "rgba(255, 206, 86, 0.6)", "label": "Moderate"},
            {"from": 70, "to": 100, "color": "rgba(75, 192, 192, 0.6)", "label": "Consistent"}
        ],
        "options": {
            "responsive": True,
            "valueLabel": {
                "fontSize": 24,
                "format": "percentage"
            }
        }
    }


def generate_all_visualizations(
    progress_snapshots: List[Dict],
    quiz_history: List[Dict],
    topic_mastery: Dict[str, Dict],
    consistency_score: float
) -> Dict[str, Any]:
    """
    Generate all visualization data at once.
    
    Returns:
        Dictionary with all chart data
    """
    return {
        "progress_over_time": generate_progress_chart_data(progress_snapshots),
        "difficulty_breakdown": generate_difficulty_breakdown_chart(progress_snapshots),
        "topic_mastery": generate_topic_mastery_chart(topic_mastery),
        "quiz_performance_trend": generate_quiz_performance_trend_chart(quiz_history),
        "learning_time": generate_learning_time_chart(progress_snapshots),
        "topic_distribution": generate_topic_distribution_pie_chart(topic_mastery),
        "consistency_gauge": generate_consistency_gauge_data(consistency_score)
    }


def format_chart_data_as_markdown(chart_data: Dict[str, Any]) -> str:
    """
    Format chart data as markdown for display (ASCII art style).
    """
    chart_type = chart_data.get('type', 'unknown')
    title = chart_data.get('title', 'Chart')
    
    output = [f"\n### {title}\n"]
    
    if chart_type in ['line', 'bar', 'horizontalBar']:
        labels = chart_data.get('labels', [])
        datasets = chart_data.get('datasets', [])
        
        if not datasets:
            return "No data available"
        
        for dataset in datasets:
            output.append(f"\n**{dataset.get('label', 'Data')}:**")
            data = dataset.get('data', [])
            
            for i, (label, value) in enumerate(zip(labels, data)):
                bar_length = int(value / 2)  # Scale to fit
                bar = '█' * bar_length
                output.append(f"{label:15} | {bar} {value:.1f}")
    
    elif chart_type == 'pie':
        labels = chart_data.get('labels', [])
        datasets = chart_data.get('datasets', [])
        
        if datasets:
            data = datasets[0].get('data', [])
            total = sum(data)
            
            for label, value in zip(labels, data):
                percentage = (value / total * 100) if total > 0 else 0
                output.append(f"{label:20} | {value:4} ({percentage:5.1f}%)")
    
    elif chart_type == 'gauge':
        value = chart_data.get('value', 0)
        output.append(f"\n**Score:** {value:.1f}%")
        
        # Simple gauge representation
        filled = int(value / 5)
        empty = 20 - filled
        gauge = '█' * filled + '░' * empty
        output.append(f"[{gauge}]")
    
    return '\n'.join(output)
