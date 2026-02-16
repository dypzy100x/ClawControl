"""Analytics - Session tracking and usage history"""
from datetime import datetime, timedelta
from typing import List, Dict
from collections import deque
import json
from pathlib import Path

ANALYTICS_FILE = Path.home() / ".clawcontrol" / "data" / "analytics.json"

class AnalyticsTracker:
    def __init__(self):
        self.sessions = deque(maxlen=1000)
        self.analytics_file = ANALYTICS_FILE
        self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
        self._load()
    
    def _load(self):
        if self.analytics_file.exists():
            try:
                with open(self.analytics_file, 'r') as f:
                    data = json.load(f)
                    for session in data.get('sessions', [])[-1000:]:
                        self.sessions.append(session)
            except: pass
    
    def _save(self):
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump({'sessions': list(self.sessions)}, f, indent=2)
        except: pass
    
    def track_session(self, duration: int, actions: int, violations: int):
        session = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "actions": actions,
            "violations": violations
        }
        self.sessions.append(session)
        self._save()
        return session
    
    def get_stats(self, days: int = 30) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [s for s in self.sessions 
                  if datetime.fromisoformat(s["timestamp"]) >= cutoff]
        
        if not recent:
            return {"total_sessions": 0}
        
        return {
            "total_sessions": len(recent),
            "total_actions": sum(s["actions"] for s in recent),
            "total_violations": sum(s["violations"] for s in recent),
            "avg_duration": sum(s["duration_seconds"] for s in recent) / len(recent)
        }

analytics_tracker = AnalyticsTracker()
