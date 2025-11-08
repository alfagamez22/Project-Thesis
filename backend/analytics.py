"""
Real-time Analytics System for Employee Activity Recognition
Reads and aggregates data from Activity Detection Logs
"""

import threading
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple
import json


class ActivityAnalytics:
    """Real-time analytics engine that reads from activity logs"""
    
    def __init__(self):
        """Initialize analytics system"""
        self.lock = threading.Lock()
        self.session_start = datetime.now()
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse ISO format timestamp"""
        try:
            return datetime.fromisoformat(timestamp_str)
        except:
            return datetime.now()
    
    def _get_activity_logs(self):
        """Get activity logs from livefeed module"""
        try:
            from backend.har.livefeed import get_all_activity_logs
            return get_all_activity_logs()
        except Exception as e:
            print(f"Error getting activity logs: {e}")
            return []
    
    def _filter_logs_by_time(self, logs: List[Dict], minutes: Optional[int] = None) -> List[Dict]:
        """Filter logs by time window"""
        if not logs:
            return []
        
        if minutes is None:
            return logs
        
        cutoff = datetime.now() - timedelta(minutes=minutes)
        filtered = []
        
        for log in logs:
            timestamp = self._parse_timestamp(log.get('timestamp', ''))
            if timestamp >= cutoff:
                filtered.append(log)
        
        return filtered
    
    def get_current_snapshot(self, time_window_minutes: int = 60) -> Dict:
        """
        Get current snapshot of activities
        
        Args:
            time_window_minutes: Time window in minutes (default 60)
            
        Returns:
            Dict with summary statistics
        """
        with self.lock:
            logs = self._get_activity_logs()
            filtered_logs = self._filter_logs_by_time(logs, time_window_minutes)
            
            if not filtered_logs:
                return {
                    'total_activities': 0,
                    'active_employees': 0,
                    'unique_activities': 0,
                    'session_duration_minutes': 0,
                    'last_update': None
                }
            
            # Count unique employees
            employees = set()
            all_activities = []
            
            for log in filtered_logs:
                employees.add(log.get('employee_id', ''))
                all_activities.extend(log.get('actions', []))
            
            unique_activities = len(set(all_activities))
            
            # Calculate session duration
            session_duration = (datetime.now() - self.session_start).total_seconds() / 60
            
            # Get last update time
            last_log = filtered_logs[-1] if filtered_logs else None
            last_update = last_log.get('timestamp') if last_log else None
            
            return {
                'total_activities': len(filtered_logs),
                'active_employees': len(employees),
                'unique_activities': unique_activities,
                'session_duration_minutes': round(session_duration, 1),
                'last_update': last_update
            }
    
    def get_top_activities(self, limit: int = 10, time_window_minutes: int = 60) -> List[Tuple[str, int, float]]:
        """
        Get most frequent activities
        
        Args:
            limit: Number of top activities to return
            time_window_minutes: Time window in minutes
            
        Returns:
            List of tuples (activity_name, count, percentage)
        """
        with self.lock:
            logs = self._get_activity_logs()
            filtered_logs = self._filter_logs_by_time(logs, time_window_minutes)
            
            if not filtered_logs:
                return []
            
            # Count all activities
            activity_counter: Counter = Counter()
            
            for log in filtered_logs:
                actions = log.get('actions', [])
                for action in actions:
                    activity_counter[action] += 1
            
            total = sum(activity_counter.values())
            
            # Get top activities with percentages
            top_activities = []
            for activity, count in activity_counter.most_common(limit):
                percentage = (count / total * 100) if total > 0 else 0
                top_activities.append((activity, count, round(percentage, 2)))
            
            return top_activities
    
    def get_employee_statistics(self, employee_id: Optional[str] = None, time_window_minutes: int = 60) -> Dict:
        """
        Get statistics for a specific employee or all employees
        
        Args:
            employee_id: Optional employee ID (None for all employees)
            time_window_minutes: Time window in minutes
            
        Returns:
            Dict with employee statistics
        """
        with self.lock:
            logs = self._get_activity_logs()
            filtered_logs = self._filter_logs_by_time(logs, time_window_minutes)
            
            if not filtered_logs:
                return {}
            
            # Group by employee
            employee_data: Dict = defaultdict(lambda: {
                'total_activities': 0,
                'unique_activities': set(),
                'activity_counts': Counter(),
                'last_seen': None
            })
            
            for log in filtered_logs:
                emp_id = log.get('employee_id', '')
                actions = log.get('actions', [])
                timestamp = log.get('timestamp')
                
                if employee_id and emp_id != employee_id:
                    continue
                
                employee_data[emp_id]['total_activities'] += 1
                employee_data[emp_id]['last_seen'] = timestamp
                
                for action in actions:
                    employee_data[emp_id]['unique_activities'].add(action)
                    employee_data[emp_id]['activity_counts'][action] += 1
            
            # Format output
            result = {}
            for emp_id, data in employee_data.items():
                top_activity = data['activity_counts'].most_common(1)
                result[emp_id] = {
                    'employee_id': emp_id,
                    'total_activities': data['total_activities'],
                    'unique_activities': len(data['unique_activities']),
                    'top_activity': top_activity[0][0] if top_activity else None,
                    'top_activity_count': top_activity[0][1] if top_activity else 0,
                    'last_seen': data['last_seen'],
                    'all_activities': dict(data['activity_counts'])
                }
            
            if employee_id:
                return result.get(employee_id, {})
            
            return result
    
    def get_hourly_breakdown(self, time_window_hours: int = 24) -> Dict[int, Dict[str, int]]:
        """
        Get hourly breakdown of activities
        
        Args:
            time_window_hours: Time window in hours
            
        Returns:
            Dict mapping hour -> {activity: count}
        """
        with self.lock:
            logs = self._get_activity_logs()
            cutoff = datetime.now() - timedelta(hours=time_window_hours)
            
            hourly_stats: Dict = defaultdict(lambda: Counter())
            
            for log in logs:
                timestamp = self._parse_timestamp(log.get('timestamp', ''))
                
                if timestamp < cutoff:
                    continue
                
                hour = timestamp.hour
                actions = log.get('actions', [])
                
                for action in actions:
                    hourly_stats[hour][action] += 1
            
            # Convert to regular dict
            result = {}
            for hour, activities in hourly_stats.items():
                result[hour] = dict(activities)
            
            return result
    
    def get_activity_trends(self, activity_name: str, time_window_minutes: int = 60, interval_minutes: int = 5) -> List[Dict]:
        """
        Get trend data for a specific activity
        
        Args:
            activity_name: Name of activity to track
            time_window_minutes: Time window in minutes
            interval_minutes: Interval for grouping data points
            
        Returns:
            List of dicts with timestamp and count
        """
        with self.lock:
            logs = self._get_activity_logs()
            cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
            
            # Group by time intervals
            interval_counts: Dict = defaultdict(int)
            
            for log in logs:
                timestamp = self._parse_timestamp(log.get('timestamp', ''))
                
                if timestamp < cutoff:
                    continue
                
                actions = log.get('actions', [])
                
                if activity_name in actions:
                    # Round to interval
                    interval_time = timestamp.replace(
                        minute=(timestamp.minute // interval_minutes) * interval_minutes,
                        second=0,
                        microsecond=0
                    )
                    interval_counts[interval_time] += 1
            
            # Format output
            trends = []
            for ts, count in sorted(interval_counts.items()):
                trends.append({
                    'timestamp': ts.isoformat(),
                    'count': count
                })
            
            return trends
    
    def get_all_activity_trends(self, time_window_minutes: int = 60, interval_minutes: int = 5) -> Dict[str, List[Dict]]:
        """
        Get trend data for all activities
        
        Args:
            time_window_minutes: Time window in minutes
            interval_minutes: Interval for grouping data points
            
        Returns:
            Dict mapping activity_name -> list of trend points
        """
        with self.lock:
            logs = self._get_activity_logs()
            cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
            
            # Group by activity and time intervals
            activity_trends: Dict = defaultdict(lambda: defaultdict(int))
            
            for log in logs:
                timestamp = self._parse_timestamp(log.get('timestamp', ''))
                
                if timestamp < cutoff:
                    continue
                
                actions = log.get('actions', [])
                
                # Round to interval
                interval_time = timestamp.replace(
                    minute=(timestamp.minute // interval_minutes) * interval_minutes,
                    second=0,
                    microsecond=0
                )
                
                for action in actions:
                    activity_trends[action][interval_time] += 1
            
            # Format output
            result = {}
            for activity, intervals in activity_trends.items():
                trends = []
                for ts, count in sorted(intervals.items()):
                    trends.append({
                        'timestamp': ts.isoformat(),
                        'count': count
                    })
                result[activity] = trends
            
            return result
    
    def get_alerts(self) -> List[Dict]:
        """
        Get activity alerts based on patterns
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        with self.lock:
            logs = self._get_activity_logs()
            recent_logs = self._filter_logs_by_time(logs, 10)  # Last 10 minutes
            
            if not recent_logs:
                alerts.append({
                    'type': 'info',
                    'message': 'No recent activity detected',
                    'timestamp': datetime.now().isoformat()
                })
                return alerts
            
            # Check for prolonged standing
            employee_activities: Dict = defaultdict(list)
            for log in recent_logs:
                emp_id = log.get('employee_id', '')
                actions = log.get('actions', [])
                employee_activities[emp_id].extend(actions)
            
            for emp_id, actions in employee_activities.items():
                standing_count = actions.count('stand')
                total_actions = len(actions)
                
                if total_actions > 0 and standing_count / total_actions > 0.8 and standing_count > 50:
                    alerts.append({
                        'type': 'warning',
                        'message': f'{emp_id} has been standing for extended period',
                        'timestamp': datetime.now().isoformat(),
                        'employee_id': emp_id
                    })
        
        return alerts
    
    def get_analytics_dashboard(self, time_window_minutes: int = 60) -> Dict:
        """
        Get comprehensive dashboard data
        
        Args:
            time_window_minutes: Time window in minutes
            
        Returns:
            Dict with all analytics data
        """
        return {
            'snapshot': self.get_current_snapshot(time_window_minutes),
            'top_activities': self.get_top_activities(10, time_window_minutes),
            'employee_stats': self.get_employee_statistics(None, time_window_minutes),
            'hourly_breakdown': self.get_hourly_breakdown(24),
            'alerts': self.get_alerts(),
            'time_window_minutes': time_window_minutes,
            'generated_at': datetime.now().isoformat()
        }
    
    def reset(self):
        """Reset analytics (clears activity logs)"""
        try:
            from backend.har.livefeed import clear_activity_logs
            clear_activity_logs()
            self.session_start = datetime.now()
            return True
        except Exception as e:
            print(f"Error resetting analytics: {e}")
            return False


# Global analytics engine instance
analytics_engine = ActivityAnalytics()


# Convenience functions for external use (maintaining backward compatibility)
def record_activity(detections: Dict[str, List[str]]):
    """Helper function for backward compatibility - no longer records separately"""
    pass  # Analytics now reads directly from activity logs


def get_analytics_snapshot():
    """Get current analytics snapshot"""
    return analytics_engine.get_current_snapshot()


def get_analytics_dashboard():
    """Get full analytics dashboard"""
    return analytics_engine.get_analytics_dashboard()

