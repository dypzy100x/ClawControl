"""
Alert System - Notifications when violations occur
"""
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque
import json
from pathlib import Path

ALERTS_FILE = Path.home() / ".clawcontrol" / "logs" / "alerts.json"

class AlertLevel:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertSystem:
    def __init__(self, max_alerts: int = 1000):
        self.max_alerts = max_alerts
        self.alerts = deque(maxlen=max_alerts)
        self.unread_count = 0
        self.alerts_file = ALERTS_FILE
        self.alerts_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing alerts
        self._load_alerts()
    
    def _load_alerts(self):
        """Load alerts from file."""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)
                    for alert in data.get('alerts', [])[-self.max_alerts:]:
                        self.alerts.append(alert)
                    self.unread_count = data.get('unread_count', 0)
            except Exception:
                pass
    
    def _save_alerts(self):
        """Save alerts to file."""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump({
                    'alerts': list(self.alerts),
                    'unread_count': self.unread_count
                }, f, indent=2)
        except Exception:
            pass
    
    def create_alert(
        self,
        title: str,
        message: str,
        level: str = AlertLevel.INFO,
        data: Optional[Dict] = None
    ) -> Dict:
        """Create a new alert."""
        alert = {
            "id": str(len(self.alerts)),
            "title": title,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "data": data or {}
        }
        
        self.alerts.append(alert)
        self.unread_count += 1
        self._save_alerts()
        
        return alert
    
    def get_alerts(
        self,
        limit: int = 50,
        unread_only: bool = False,
        level: Optional[str] = None
    ) -> List[Dict]:
        """Get alerts with optional filtering."""
        alerts = list(self.alerts)
        
        # Filter by unread
        if unread_only:
            alerts = [a for a in alerts if not a.get("read", False)]
        
        # Filter by level
        if level:
            alerts = [a for a in alerts if a.get("level") == level]
        
        # Return most recent first
        alerts.reverse()
        
        return alerts[:limit]
    
    def mark_as_read(self, alert_ids: List[str]) -> int:
        """Mark alerts as read."""
        marked = 0
        
        for alert in self.alerts:
            if alert["id"] in alert_ids and not alert.get("read", False):
                alert["read"] = True
                self.unread_count = max(0, self.unread_count - 1)
                marked += 1
        
        if marked > 0:
            self._save_alerts()
        
        return marked
    
    def mark_all_as_read(self) -> int:
        """Mark all alerts as read."""
        marked = 0
        
        for alert in self.alerts:
            if not alert.get("read", False):
                alert["read"] = True
                marked += 1
        
        self.unread_count = 0
        
        if marked > 0:
            self._save_alerts()
        
        return marked
    
    def clear_old_alerts(self, days: int = 30) -> int:
        """Clear alerts older than N days."""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        original_count = len(self.alerts)
        
        # Filter alerts
        new_alerts = deque(maxlen=self.max_alerts)
        for alert in self.alerts:
            timestamp = datetime.fromisoformat(alert["timestamp"])
            if timestamp >= cutoff:
                new_alerts.append(alert)
            elif not alert.get("read", False):
                self.unread_count = max(0, self.unread_count - 1)
        
        self.alerts = new_alerts
        self._save_alerts()
        
        return original_count - len(self.alerts)
    
    def get_stats(self) -> Dict:
        """Get alert statistics."""
        if not self.alerts:
            return {
                "total": 0,
                "unread": 0,
                "by_level": {}
            }
        
        by_level = {}
        for alert in self.alerts:
            level = alert.get("level", AlertLevel.INFO)
            by_level[level] = by_level.get(level, 0) + 1
        
        return {
            "total": len(self.alerts),
            "unread": self.unread_count,
            "by_level": by_level
        }
    
    # Convenience methods for common alert types
    
    def violation_alert(self, violation_type: str, details: str, instance_id: str = None):
        """Create a violation alert."""
        return self.create_alert(
            title=f"Guardrail Violation: {violation_type}",
            message=details,
            level=AlertLevel.ERROR,
            data={
                "type": "violation",
                "violation_type": violation_type,
                "instance_id": instance_id
            }
        )
    
    def process_alert(self, action: str, success: bool, instance_id: str = None):
        """Create a process action alert."""
        level = AlertLevel.INFO if success else AlertLevel.WARNING
        return self.create_alert(
            title=f"Process {action}",
            message=f"OpenClaw {action} {'succeeded' if success else 'failed'}",
            level=level,
            data={
                "type": "process_action",
                "action": action,
                "success": success,
                "instance_id": instance_id
            }
        )
    
    def system_alert(self, title: str, message: str, critical: bool = False):
        """Create a system alert."""
        return self.create_alert(
            title=title,
            message=message,
            level=AlertLevel.CRITICAL if critical else AlertLevel.WARNING,
            data={"type": "system"}
        )
