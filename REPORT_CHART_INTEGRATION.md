# Report Agent Chart Rendering Integration

## Overview

The Report Agent now automatically generates visual chart dashboards that can be displayed in the frontend. Charts are rendered as PNG images and saved to `api_server/public/` with unique filenames.

## How It Works

### Backend Flow

1. **User requests a report** via the API or chat interface
2. **Report Agent analyzes** the user's learning data
3. **Agent calls `render_progress_charts` tool** with:
   - `user_session_id`: The user's session ID
   - `days`: Time period to analyze (default: 14)
   - `chart_type`: "dashboard" (recommended) for complete visual dashboard
4. **Chart Renderer creates PNG file** in `api_server/public/` with unique filename
5. **Tool returns JSON** with filename and URL:
   ```json
   {
     "chart_type": "dashboard",
     "filename": "report_user123_dashboard_20251116_165019_33df4ffb.png",
     "url": "/public/report_user123_dashboard_20251116_165019_33df4ffb.png",
     "charts_included": [
       "progress_over_time",
       "difficulty_breakdown",
       "quiz_performance_trend",
       "learning_time",
       "topic_mastery",
       "topic_distribution"
     ]
   }
   ```
6. **Agent includes the URL** in its response markdown
7. **Frontend fetches and displays** the chart image

### Frontend Integration

The agent's response includes markdown links to the charts:

```markdown
## 📊 Visual Dashboard

**📈 [View Your Progress Dashboard](/public/report_user123_dashboard_20251116_165019.png)**
```

Your frontend should:

1. **Parse the agent's markdown response** to extract image URLs
2. **Fetch images** from the API server:
   ```javascript
   const imageUrl = 'http://localhost:8000/generated/report_user123_dashboard_20251116_165019.png';
   ```
3. **Display images** in the chat or report view:
   ```jsx
   <img src={imageUrl} alt="Progress Dashboard" style={{width: '100%', height: 'auto'}} />
   ```

## API Endpoints

### Static File Serving

Chart images are served via FastAPI's StaticFiles:

- **URL Pattern**: `/public/{filename}`
- **Example**: `http://localhost:8000/generated/report_user123_dashboard_20251116_165019.png`
- **Method**: GET
- **Response**: PNG image file

### Chart Types

The `render_progress_charts` tool supports three chart types:

#### 1. Dashboard (Recommended)
```python
chart_type = "dashboard"
```
Creates a comprehensive dashboard with 6 charts in a single image:
- Progress over time (line chart)
- Difficulty breakdown (bar chart)
- Quiz performance trend (line chart with moving average)
- Learning time distribution (bar chart)
- Topic mastery levels (horizontal bars)
- Topic distribution (pie chart)

#### 2. All Charts Separately
```python
chart_type = "all"
```
Generates individual PNG files for each chart type. Returns multiple filenames.

#### 3. Single Chart
```python
chart_type = "progress_over_time"  # or any specific chart name
```
Generates just one specific chart.

## Chart Dashboard

The dashboard image (20x12 inches at 150 DPI) includes:

### Top Row (Full Width)
- **Progress Over Time**: Line chart showing accuracy and ability score trends

### Middle Row (3 columns)
- **Difficulty Breakdown**: Performance on easy/medium/hard questions
- **Quiz Performance**: Quiz scores with moving average trend
- **Learning Time**: Daily time investment

### Bottom Row
- **Topic Mastery**: Horizontal bars showing mastery levels (2/3 width)
- **Topic Distribution**: Pie chart of question distribution (1/3 width)

## File Naming Convention

Files are named with a unique pattern to avoid collisions:

```
report_{user_session_id}_{chart_type}_{timestamp}_{uuid}.png
```

Example:
```
report_test_user_report_123_dashboard_20251116_165019_33df4ffb.png
```

Components:
- `user_session_id`: User's session identifier
- `chart_type`: "dashboard", "progress", etc.
- `timestamp`: YYYYMMDD_HHMMSS format
- `uuid`: First 8 characters of UUID4 for uniqueness

## Testing

### Test with Sample Data

```bash
# Run the test script
python3 test_chart_rendering.py
```

This will:
1. Create a Report Agent
2. Request a comprehensive report with charts
3. Save dashboard PNG to `api_server/public/`
4. Display the agent's response with chart URL

### Manual Testing

1. **Generate a report** via the API or chat
2. **Check the response** for chart URLs like `/public/report_*.png`
3. **Access the image** in your browser:
   ```
   http://localhost:8000/generated/report_user123_dashboard_20251116_165019.png
   ```
4. **Verify the dashboard** displays all 6 charts

## File Management

### Cleanup

Charts accumulate over time. You may want to implement cleanup:

```python
# Delete charts older than 7 days
from pathlib import Path
from datetime import datetime, timedelta

public_dir = Path("api_server/public")
cutoff = datetime.now() - timedelta(days=7)

for file in public_dir.glob("report_*.png"):
    if file.stat().st_mtime < cutoff.timestamp():
        file.unlink()
```

### Storage Considerations

- Each dashboard is ~500KB - 2MB depending on data density
- Consider implementing periodic cleanup
- Or store charts in cloud storage (S3, etc.) for production

## Production Deployment

### CORS Configuration

Update CORS in `api_server/main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### CDN Integration (Optional)

For better performance, serve charts via CDN:

1. Upload generated charts to S3/CloudFront
2. Update the tool to return CDN URLs instead of local paths
3. Modify `chart_renderer.py` to upload files after generation

## Troubleshooting

### Charts Not Displaying

1. **Check file exists**:
   ```bash
   ls api_server/public/report_*.png
   ```

2. **Check API server is serving static files**:
   ```bash
   curl http://localhost:8000/generated/report_test_user_report_123_dashboard_20251116_165019.png
   ```

3. **Check CORS headers** if accessing from different domain

### Agent Not Generating Charts

1. **Verify the tool is registered** in `agents/report/tools.py`
2. **Check agent prompts** mention chart rendering
3. **Review logs** for errors in chart generation

### Low Quality Images

Increase DPI in `chart_renderer.py`:
```python
plt.savefig(filepath, dpi=300, bbox_inches='tight')  # Higher quality
```

## Summary

✅ **Automatic chart generation** integrated into Report Agent  
✅ **PNG files saved** to `api_server/public/` with unique names  
✅ **Static file serving** via FastAPI  
✅ **Frontend-ready URLs** returned in agent responses  
✅ **Comprehensive dashboard** with 6 visualization types  
✅ **Easy to integrate** into existing chat/report interfaces  

The Report Agent now provides rich visual analytics alongside text reports! 🎨📊
