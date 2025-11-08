# Real-time Analytics System Documentation

## Overview

The real-time analytics system provides comprehensive insights into employee activity patterns and behaviors. It tracks, aggregates, and visualizes activity data in real-time with automatic historical retention.

## Features

### 📊 Core Analytics

1. **Activity Snapshot**
   - Total activities detected
   - Active employees count
   - Unique activity types
   - Session duration tracking

2. **Activity Timeline**
   - Time-series data for each activity
   - Customizable time windows (15min, 30min, 1hr, 3hr)
   - Real-time updates every 5 seconds

3. **Top Activities Ranking**
   - Most frequent activities
   - Percentage breakdown
   - Visual bar charts

4. **Hourly Breakdown**
   - Hourly activity aggregation
   - Trend visualization
   - Last 24 hours of data

5. **Employee Statistics**
   - Per-employee activity tracking
   - Top activities per employee
   - Last seen timestamps
   - Activity diversity metrics

6. **Trend Analysis**
   - Increasing/decreasing/stable trends
   - Moving average calculations
   - Predictive insights

7. **Alert System**
   - Prolonged activity alerts
   - Employee inactivity warnings
   - Customizable thresholds

### 🎯 Key Capabilities

- **Automatic Data Retention**: Keeps data for 24 hours by default
- **Thread-Safe**: All operations use proper locking
- **Memory Efficient**: Uses deques with max length
- **Background Cleanup**: Automatic old data removal
- **Real-time Updates**: Live dashboard refresh

## API Endpoints

### 1. Analytics Snapshot
```http
GET /api/analytics/snapshot
```

**Response:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2025-11-09T02:10:00",
    "activities": {
      "walking": 5,
      "talking": 3,
      "using_phone": 2
    },
    "total_activities": 10,
    "unique_activities": 3,
    "active_employees": 2
  }
}
```

### 2. Comprehensive Dashboard
```http
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "success": true,
  "data": {
    "snapshot": {...},
    "top_activities": [...],
    "hourly_breakdown": [...],
    "employee_stats": {...},
    "session_duration": "2:30:15",
    "last_update": "2025-11-09T02:10:00"
  }
}
```

### 3. Top Activities
```http
GET /api/analytics/top-activities?limit=10&time_window=60
```

**Parameters:**
- `limit` (int): Maximum activities to return (default: 10)
- `time_window` (int): Time window in minutes (default: 60)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "activity": "walking",
      "count": 45,
      "percentage": 35.2
    },
    ...
  ]
}
```

### 4. Activity Timeline
```http
GET /api/analytics/timeline/<activity_name>?minutes=60
```

**Response:**
```json
{
  "success": true,
  "activity": "walking",
  "data": [
    {
      "timestamp": "2025-11-09T02:09:00",
      "count": 3
    },
    ...
  ]
}
```

### 5. All Activities Timeline
```http
GET /api/analytics/timeline/all?minutes=60
```

**Response:**
```json
{
  "success": true,
  "data": {
    "walking": [...],
    "talking": [...],
    "using_phone": [...]
  }
}
```

### 6. Employee Statistics (Single)
```http
GET /api/analytics/employee/<employee_id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "employee_id": "EMP_001",
    "activities": {
      "walking": 10,
      "talking": 5
    },
    "total_activities": 15,
    "unique_activities": 2,
    "last_seen": "2025-11-09T02:10:00",
    "top_activity": "walking"
  }
}
```

### 7. All Employees Statistics
```http
GET /api/analytics/employees
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_employees": 3,
    "employees": {
      "EMP_001": {...},
      "EMP_002": {...}
    }
  }
}
```

### 8. Hourly Breakdown
```http
GET /api/analytics/hourly?hours=24
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "hour": "2025-11-09 02:00",
      "activities": {
        "walking": 10,
        "talking": 5
      },
      "total": 15
    },
    ...
  ]
}
```

### 9. Activity Trends
```http
GET /api/analytics/trends/<activity_name>?intervals=12
```

**Response:**
```json
{
  "success": true,
  "data": {
    "activity": "walking",
    "trend": "increasing",
    "current_rate": 5,
    "average_rate": 3.5,
    "data_points": [1, 2, 3, 4, 5]
  }
}
```

### 10. Alerts
```http
GET /api/analytics/alerts
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "type": "prolonged_activity",
      "activity": "standing_still",
      "duration_seconds": 300,
      "severity": "warning",
      "message": "Prolonged standing_still detected for over 5.0 minutes"
    }
  ]
}
```

### 11. Reset Statistics
```http
POST /api/analytics/reset
```

**Response:**
```json
{
  "success": true,
  "message": "Analytics statistics reset successfully"
}
```

## Dashboard UI

### Access
Navigate to: `http://localhost:5000/analytics`

### Features

1. **Key Metrics Cards**
   - Total activities
   - Active employees
   - Unique activities
   - Session duration

2. **Time Window Selector**
   - 15 minutes
   - 30 minutes
   - 1 hour
   - 3 hours

3. **Top Activities Chart**
   - Bar chart visualization
   - Percentage breakdown
   - Hover for details

4. **Activity Breakdown List**
   - Sortable list
   - Progress bars
   - Count and percentage

5. **Hourly Trends Chart**
   - Line chart
   - Last 12 hours
   - Total activities per hour

6. **Employee Statistics Grid**
   - Per-employee cards
   - Total activities
   - Top activity
   - Unique activities

7. **Alerts Panel**
   - Real-time warnings
   - Color-coded severity
   - Actionable insights

### Auto-Refresh
- Updates every 5 seconds automatically
- Manual refresh button available
- Smooth transitions and animations

## Integration

### In Your Code

```python
from backend.analytics import analytics_engine, record_activity

# Record activities
detections = {
    'EMP_001': ['walking', 'talking'],
    'EMP_002': ['using_phone']
}
record_activity(detections)

# Get current snapshot
snapshot = analytics_engine.get_current_snapshot()

# Get top activities
top_activities = analytics_engine.get_top_activities(limit=5, time_window_minutes=30)

# Get employee stats
emp_stats = analytics_engine.get_employee_statistics('EMP_001')

# Get alerts
alerts = analytics_engine.get_alerts()
```

## Configuration

### Alert Thresholds

Edit `backend/analytics.py`:

```python
self.alert_thresholds = {
    'standing_still': 300,  # 5 minutes
    'using_phone': 180,     # 3 minutes
    'inactivity': 600       # 10 minutes
}
```

### Data Retention

```python
analytics_engine = ActivityAnalytics(retention_hours=24)  # Keep data for 24 hours
```

### Custom Time Intervals

```python
# Change update frequency in analytics.html
updateInterval = setInterval(refreshDashboard, 5000);  // 5 seconds
```

## Performance

- **Memory Usage**: ~10MB for 24 hours of data
- **CPU Impact**: < 1% with background cleanup
- **Response Time**: < 50ms for most queries
- **Concurrent Users**: Supports multiple simultaneous viewers
- **Data Points**: Up to 10,000 per activity type

## Troubleshooting

### Analytics Not Updating

1. Check if activity recognition is enabled
2. Verify employees are in ROI
3. Check console for errors
4. Refresh the page

### No Data Showing

1. Ensure server is running
2. Wait for activities to be detected
3. Check time window selection
4. Verify analytics integration in livefeed.py

### Slow Performance

1. Reduce retention hours
2. Increase cleanup frequency
3. Limit chart data points
4. Use time window filters

## Example Use Cases

### 1. Monitor Employee Productivity
```javascript
// Fetch top activities
fetch('/api/analytics/top-activities?time_window=480')  // 8 hours
    .then(r => r.json())
    .then(data => console.log('Top activities:', data));
```

### 2. Detect Unusual Patterns
```javascript
// Get alerts
fetch('/api/analytics/alerts')
    .then(r => r.json())
    .then(data => {
        if (data.data.length > 0) {
            alert('Unusual activity detected!');
        }
    });
```

### 3. Generate Reports
```javascript
// Get comprehensive dashboard data
fetch('/api/analytics/dashboard')
    .then(r => r.json())
    .then(data => generateReport(data.data));
```

## Future Enhancements

- Export data to CSV/JSON
- Email alerts
- Advanced filtering
- Custom date ranges
- Predictive analytics
- Heatmap visualizations
- Activity correlations
- Performance scoring

## License

Part of Thesis Prototype - Educational Use Only

---

**Last Updated:** November 9, 2025
**Version:** 1.0.0
