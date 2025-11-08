# Analytics System Update - Now Reading from Activity Detection Logs

## Overview
The analytics system has been completely refactored to read directly from the **Activity Detection Logs** displayed in the livefeed interface, eliminating duplicate data storage and ensuring consistency between what users see and what analytics reports.

## What Changed

### Before
- Analytics had its own separate data storage
- Activity data was recorded twice (once in logs, once in analytics)
- Required calling `record_activity()` function manually
- Data could become inconsistent between logs and analytics

### After
- Analytics reads directly from `activity_logs` in livefeed.py
- Single source of truth for all activity data
- No manual recording needed - analytics auto-syncs with logs
- What you see in Activity Detection Logs = What you see in Analytics

## Technical Changes

### 1. Analytics Engine (`backend/analytics.py`)
Complete rewrite of the `ActivityAnalytics` class:

**Removed:**
- `record_activities()` method
- Internal data storage (timeline, hourly_stats, employee_activities, etc.)
- Background cleanup threads
- Separate recording mechanism

**Added:**
- `_get_activity_logs()` - Fetches logs from livefeed
- `_filter_logs_by_time()` - Time-window filtering
- `_parse_timestamp()` - ISO timestamp parsing
- All analytics methods now process logs on-demand

**Key Methods:**
- `get_current_snapshot(time_window_minutes)` - Summary stats
- `get_top_activities(limit, time_window_minutes)` - Most frequent activities
- `get_employee_statistics(employee_id, time_window_minutes)` - Per-employee stats
- `get_hourly_breakdown(time_window_hours)` - Hour-by-hour breakdown
- `get_activity_trends(activity_name, time_window_minutes)` - Trend analysis
- `get_alerts()` - Pattern-based alerts
- `get_analytics_dashboard(time_window_minutes)` - Complete dashboard data

### 2. LiveFeed Integration (`backend/har/livefeed.py`)
Simplified `log_activity_detection()`:

**Removed:**
- Duplicate analytics recording code
- Threading for analytics updates
- Separate data extraction for analytics

**Kept:**
- Activity Detection Logs recording (single source)
- Caption caching for performance
- Thread-safe log appending

### 3. Activity Log Structure
Each log entry contains:
```python
{
    "timestamp": "2025-11-09T02:34:31.123456",  # ISO format
    "employee_id": "EMP_001",
    "actions": ["stand", "brewing"],  # List of detected actions
    "confidence_scores": [0.95, 0.87]  # Corresponding confidence values
}
```

## Benefits

### 1. Data Consistency
✅ Activity Detection Logs and Analytics always show the same data
✅ No sync issues or data mismatches
✅ Single source of truth

### 2. Performance
✅ Eliminated duplicate data storage
✅ Reduced memory usage
✅ No background threads for data management
✅ Caption caching prevents file I/O blocking

### 3. Simplicity
✅ No manual `record_activity()` calls needed
✅ Easier to maintain and debug
✅ Clear data flow: Detection → Logs → Analytics

### 4. Flexibility
✅ Time windows are dynamic (analytics can look at any time range)
✅ No data retention limitations
✅ Easy to clear/reset (clears logs = clears analytics)

## Using the Analytics

### From Python/Backend
```python
from backend.analytics import analytics_engine

# Get dashboard data
dashboard = analytics_engine.get_analytics_dashboard(time_window_minutes=60)

# Get specific stats
snapshot = analytics_engine.get_current_snapshot(time_window_minutes=30)
top_activities = analytics_engine.get_top_activities(limit=5, time_window_minutes=60)
employee_stats = analytics_engine.get_employee_statistics('EMP_001', time_window_minutes=60)
```

### From Web Interface
The `/analytics` page automatically displays data based on Activity Detection Logs:

1. **Current Snapshot** - Real-time stats
2. **Top Activities** - Most frequent activities with percentages
3. **Employee Statistics** - Per-employee breakdown
4. **Hourly Trends** - Activity patterns over time
5. **Alerts** - Pattern-based warnings

### Time Windows
All analytics support configurable time windows:
- **15 minutes** - Very recent activity
- **30 minutes** - Short-term trends
- **1 hour** - Default view (recommended)
- **3 hours** - Extended analysis
- **24 hours** - Full day overview

## API Endpoints

All analytics endpoints support `?time_window=<minutes>` parameter:

| Endpoint | Description | Default Window |
|----------|-------------|----------------|
| `/api/analytics/dashboard` | Full dashboard data | 60 min |
| `/api/analytics/snapshot` | Current snapshot | 60 min |
| `/api/analytics/top-activities` | Top activities | 60 min |
| `/api/analytics/employee/<id>` | Employee stats | 60 min |
| `/api/analytics/employees` | All employees | 60 min |
| `/api/analytics/hourly` | Hourly breakdown | 24 hours |
| `/api/analytics/trends/<activity>` | Activity trend | 60 min |
| `/api/analytics/timeline/all` | All trends | 60 min |
| `/api/analytics/alerts` | Active alerts | 10 min |
| `/api/analytics/reset` | Clear analytics | - |

## Example Queries

```bash
# Get last 30 minutes of data
curl "http://localhost:5000/api/analytics/dashboard?time_window=30"

# Get top 5 activities from last hour
curl "http://localhost:5000/api/analytics/top-activities?limit=5&time_window=60"

# Get specific employee stats for last 15 minutes
curl "http://localhost:5000/api/analytics/employee/EMP_001?time_window=15"
```

## Testing

### Manual Test
1. Start server: `python start_server.py`
2. Go to `/livefeed` and enable activity recognition
3. Wait for Activity Detection Logs to populate
4. Go to `/analytics` - should show data matching the logs
5. Try different time windows (15min, 30min, 1hr, 3hr)
6. Verify all charts and stats update correctly

### Automated Test
```python
# Test file already exists: test_analytics.py
python test_analytics.py
```

## Migration Notes

### Backward Compatibility
The following functions still exist for backward compatibility but are no-ops:

```python
from backend.analytics import record_activity

# This now does nothing (analytics reads logs directly)
record_activity({"EMP_001": ["walking", "talking"]})
```

### Breaking Changes
None - all existing API endpoints work the same way

### Data Reset
To clear analytics:
```python
analytics_engine.reset()  # Clears activity logs
```

Or via API:
```bash
POST http://localhost:5000/api/analytics/reset
```

## Troubleshooting

**Q: Analytics shows no data**
A: Check that Activity Recognition is enabled in /livefeed and Activity Detection Logs are populating

**Q: Analytics data doesn't match logs**
A: This should no longer happen! If it does, it's a bug - please report

**Q: Analytics are slow**
A: Reduce time window (use 15-30 min instead of hours) or check if activity logs have grown too large

**Q: How to clear old data?**
A: Use "Clear" button in Activity Detection Logs or call `/api/analytics/reset`

## Performance Considerations

- Analytics process logs on-demand (no background storage)
- Time-window filtering is O(n) where n = number of logs
- Recommend clearing logs periodically for long-running sessions
- Caption caching prevents I/O bottlenecks
- No locks held during computations (only during log reads)

## Future Enhancements

Possible future additions:
- [ ] Export analytics to CSV/PDF
- [ ] Email alerts for prolonged activities
- [ ] Custom date range selection
- [ ] Advanced filtering (by activity type, employee, etc.)
- [ ] Activity correlation analysis
- [ ] Predictive analytics based on patterns
