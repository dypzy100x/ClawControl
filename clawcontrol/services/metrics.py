"""
Metrics System - CPU, RAM, Thread tracking
"""
from datetime import datetime, timedelta
from typing import List, Dict
from collections import deque
import psutil
import time

class MetricsCollector:
    def __init__(self, history_size: int = 300):
        self.history_size = history_size  # 5 minutes at 1s intervals
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.thread_history = deque(maxlen=history_size)
        self.last_collection = None
    
    def collect_system_metrics(self) -> Dict:
        """Collect current system metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_mb": psutil.virtual_memory().used / (1024 * 1024),
            "memory_percent": psutil.virtual_memory().percent,
            "thread_count": len(psutil.Process().threads())
        }
        
        # Add to history
        self.cpu_history.append(metrics["cpu_percent"])
        self.memory_history.append(metrics["memory_mb"])
        self.thread_history.append(metrics["thread_count"])
        
        self.last_collection = datetime.now()
        
        return metrics
    
    def get_stats(self) -> Dict:
        """Get statistical analysis of metrics."""
        if not self.cpu_history:
            return {}
        
        return {
            "cpu": {
                "current": self.cpu_history[-1] if self.cpu_history else 0,
                "min": min(self.cpu_history),
                "max": max(self.cpu_history),
                "avg": sum(self.cpu_history) / len(self.cpu_history)
            },
            "memory_mb": {
                "current": self.memory_history[-1] if self.memory_history else 0,
                "min": min(self.memory_history),
                "max": max(self.memory_history),
                "avg": sum(self.memory_history) / len(self.memory_history)
            },
            "threads": {
                "current": self.thread_history[-1] if self.thread_history else 0,
                "min": min(self.thread_history),
                "max": max(self.thread_history),
                "avg": sum(self.thread_history) / len(self.thread_history)
            }
        }
    
    def get_history(self, metric: str = "cpu", limit: int = 60) -> List[float]:
        """Get metric history."""
        histories = {
            "cpu": self.cpu_history,
            "memory": self.memory_history,
            "threads": self.thread_history
        }
        
        history = histories.get(metric, self.cpu_history)
        return list(history)[-limit:]

metrics_collector = MetricsCollector()
