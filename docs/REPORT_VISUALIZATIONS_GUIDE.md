# Report Agent Visualizations Guide

## Overview

The Report Agent now includes powerful visualization capabilities that generate chart data for displaying student progress through graphs and charts.

## Visualization Types

### 1. Progress Over Time (Line Chart)
Shows overall accuracy and ability score trends over the selected period.

**Use Case**: Track improvement trajectory, identify learning patterns

### 2. Difficulty Breakdown (Bar Chart)
Compares performance across easy, medium, and difficult questions.

**Use Case**: Identify which difficulty levels need focus

### 3. Topic Mastery (Horizontal Bar Chart)
Shows mastery levels and accuracy for each topic.

**Use Case**: See strongest and weakest topics at a glance

### 4. Quiz Performance Trend (Line Chart with Moving Average)
Displays quiz scores over time with a smoothed trend line.

**Use Case**: Understand quiz performance patterns and consistency

### 5. Learning Time Distribution (Bar Chart)
Shows daily learning time investment.

**Use Case**: Track study habits and time management

### 6. Topic Distribution (Pie Chart)
Shows proportion of questions attempted by topic.

**Use Case**: Understand study focus areas

### 7. Consistency Gauge (Meter/Gauge)
Displays performance consistency score (0-100).

**Use Case**: Measure reliability of performance

## Using Visualizations

### Method 1: Through Report Agent

```python
from agents.report.agent import ReportAgent

agent = ReportAgent()

# Get text-based visualizations
text_viz = agent.get_visualizations(
    user_session_id="user_123",
    days=7,
    format="markdown"
)
print(text_viz)

# Get JSON data for charts
json_viz = agent.get_visualizations(
    user_session_id="user_123",
    days=7,
    format="json"
)
```

### Method 2: Direct Tool Usage

```python
from agents.report.tools import generate_progress_visualizations

# Get visualization data
viz_data = generate_progress_visualizations(
    user_session_id="user_123",
    days=7,
    format="json"
)
```

### Method 3: Backend Utilities

```python
from agents.report.backend.visualizations import generate_all_visualizations

# Get raw data
snapshots = [...]  # Progress snapshots
quiz_history = [...]  # Quiz attempts
topic_mastery = {...}  # Topic data
consistency = 0.85

viz_data = generate_all_visualizations(
    snapshots, quiz_history, topic_mastery, consistency
)
```

## Output Formats

### JSON Format
Chart.js compatible data structure:

```json
{
  "progress_over_time": {
    "type": "line",
    "title": "Learning Progress Over Time",
    "labels": ["2025-11-01", "2025-11-02", ...],
    "datasets": [
      {
        "label": "Overall Accuracy",
        "data": [65.5, 68.2, 70.1, ...],
        "borderColor": "rgb(75, 192, 192)"
      }
    ],
    "options": {...}
  },
  "difficulty_breakdown": {...},
  ...
}
```

### Markdown Format
ASCII-art style text visualization:

```
### Learning Progress Over Time

**Overall Accuracy:**
2025-11-01      | ████████████████████████████████ 65.5
2025-11-02      | █████████████████████████████████ 68.2
2025-11-03      | ██████████████████████████████████ 70.1
```

## Running the Examples

### Test with Sample Data

```bash
# Run test script with visualizations
python test_report_agent.py
```

This will generate:
- Text-based visualizations in the console
- JSON data structures

### Create Actual Charts

```bash
# Requires matplotlib
pip install matplotlib

# Run visualization example
python example_report_visualizations.py
```

This will:
- Generate a PNG file with all charts
- Display charts in a window

## Customization

### Custom Chart Colors

Modify `agents/report/backend/visualizations.py`:

```python
def generate_progress_chart_data(snapshots):
    return {
        "datasets": [{
            "borderColor": "rgb(YOUR_COLOR)",
            "backgroundColor": "rgba(YOUR_COLOR, 0.2)"
        }]
    }
```

### Custom Time Windows

```python
# Weekly report
viz = agent.get_visualizations(user_id, days=7)

# Monthly report  
viz = agent.get_visualizations(user_id, days=30)

# All-time
viz = agent.get_visualizations(user_id, days=365)
```

### Additional Metrics

Add new visualization functions in `visualizations.py`:

```python
def generate_custom_chart(data):
    return {
        "type": "line",
        "title": "Custom Metric",
        "labels": [...],
        "datasets": [...]
    }
```

## Best Practices

1. **Caching**: Cache visualization data to avoid repeated database queries
2. **Lazy Loading**: Load charts on-demand, not all at once
3. **Responsive Design**: Use responsive chart options for mobile
4. **Color Accessibility**: Use colorblind-friendly palettes
5. **Performance**: Limit data points for large time ranges

## Troubleshooting

### No Data Displayed
- Ensure user has completed quizzes
- Check date range is valid
- Verify database contains progress snapshots

### JSON Parse Error
- Extract JSON from agent response
- Handle wrapped text around JSON
- Validate JSON structure

### Chart Not Rendering
- Check data format matches chart type
- Verify labels and data arrays are same length
- Ensure chart library is installed

## Dependencies

```bash
# For matplotlib examples
pip install matplotlib

# For plotly examples
pip install plotly

# For web integration
npm install chart.js
# or
npm install recharts
```

## Summary

The Report Agent's visualization system provides:
- ✅ 7 different chart types
- ✅ JSON and Markdown formats
- ✅ Chart.js compatible output
- ✅ Easy integration with plotting libraries
- ✅ Text-based visualization fallback
- ✅ Customizable and extensible

Perfect for dashboards, reports, and data analysis!
