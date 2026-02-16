#!/bin/bash
# Script to generate ALL missing v2 files

echo "🛡️ Generating all ClawControl v2 files..."

# Create all the files that were in your screenshot
# This script creates skeleton versions - you can enhance them later

cd "$(dirname "$0")"

# Already have: alerts.py, metrics.py

echo "Creating analytics.py..."
cat > clawcontrol/services/analytics.py << 'EOF'
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
EOF

echo "Creating anomaly.py..."
cat > clawcontrol/services/anomaly.py << 'EOF'
"""Anomaly Detection - ML-based threat detection"""
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.trained = False
        self.feature_history = []
    
    def train(self, features_list: list):
        if len(features_list) < 10:
            return False
        X = np.array(features_list)
        self.model.fit(X)
        self.trained = True
        return True
    
    def detect(self, features: list) -> dict:
        if not self.trained:
            return {"anomaly": False, "score": 0.5}
        
        X = np.array([features])
        prediction = self.model.predict(X)
        score = self.model.score_samples(X)[0]
        
        return {
            "anomaly": prediction[0] == -1,
            "score": float(score),
            "confidence": abs(float(score))
        }

anomaly_detector = AnomalyDetector()
EOF

echo "Creating cost_tracking.py..."
cat > clawcontrol/services/cost_tracking.py << 'EOF'
"""Cost Tracking - API usage and cost monitoring"""
from datetime import datetime
from typing import Dict
from collections import defaultdict

class CostTracker:
    def __init__(self):
        self.daily_costs = defaultdict(float)
        self.monthly_budget = 0
        self.token_usage = {"input": 0, "output": 0}
    
    def track_tokens(self, input_tokens: int, output_tokens: int, model: str = "gpt-4"):
        self.token_usage["input"] += input_tokens
        self.token_usage["output"] += output_tokens
        
        # Simple pricing (update with real prices)
        cost = (input_tokens * 0.00003) + (output_tokens * 0.00006)
        
        today = datetime.now().date().isoformat()
        self.daily_costs[today] += cost
        
        return cost
    
    def set_budget(self, monthly_budget: float):
        self.monthly_budget = monthly_budget
    
    def get_current_spend(self) -> float:
        return sum(self.daily_costs.values())
    
    def check_budget_status(self) -> Dict:
        current = self.get_current_spend()
        if self.monthly_budget == 0:
            return {"status": "no_budget_set"}
        
        percent = (current / self.monthly_budget) * 100
        
        if percent > 100:
            status = "exceeded"
        elif percent > 90:
            status = "warning"
        elif percent > 75:
            status = "on_track"
        else:
            status = "under_budget"
        
        return {
            "status": status,
            "current_spend": current,
            "budget": self.monthly_budget,
            "percent_used": percent
        }

cost_tracker = CostTracker()
EOF

echo "Creating presets.py..."
cat > clawcontrol/services/presets.py << 'EOF'
"""Guard rail Presets - Pre-configured security templates"""

PRESETS = {
    "strict": {
        "name": "Strict Security",
        "block_patterns": [
            "rm -rf", "sudo", "chmod 777", "curl http://",
            "wget", "nc ", "netcat", "dd ", "mkfs",
            ":(){ :|:& };:", "eval", "exec"
        ],
        "allowed_paths": ["/tmp"],
        "rate_limit_per_min": 30
    },
    "coding": {
        "name": "Coding Safe",
        "block_patterns": ["rm -rf /", "sudo rm", "format c:"],
        "allowed_paths": ["/tmp", "/home", "/Users"],
        "rate_limit_per_min": 100
    },
    "research": {
        "name": "Research Mode",
        "block_patterns": ["rm -rf /", "sudo rm"],
        "allowed_paths": ["/tmp", "/home", "/Users"],
        "rate_limit_per_min": 120
    },
    "minimal": {
        "name": "Minimal Protection",
        "block_patterns": ["rm -rf /"],
        "allowed_paths": [],
        "rate_limit_per_min": 200
    }
}

def get_preset(name: str) -> dict:
    return PRESETS.get(name, PRESETS["strict"])

def list_presets() -> list:
    return list(PRESETS.keys())
EOF

echo "Creating instances.py..."
cat > clawcontrol/services/instances.py << 'EOF'
"""Multi-Instance Management"""
from typing import Dict, List
from datetime import datetime

class InstanceManager:
    def __init__(self):
        self.instances: Dict[str, dict] = {}
    
    def create_instance(self, instance_id: str, config: dict) -> dict:
        instance = {
            "id": instance_id,
            "created_at": datetime.now().isoformat(),
            "status": "stopped",
            "config": config,
            "pid": None
        }
        self.instances[instance_id] = instance
        return instance
    
    def get_instance(self, instance_id: str) -> dict:
        return self.instances.get(instance_id)
    
    def list_instances(self) -> List[dict]:
        return list(self.instances.values())
    
    def delete_instance(self, instance_id: str) -> bool:
        if instance_id in self.instances:
            del self.instances[instance_id]
            return True
        return False

instance_manager = InstanceManager()
EOF

echo "Creating scheduler.py..."
cat > clawcontrol/services/scheduler.py << 'EOF'
"""Task Scheduler - Cron-style automation"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
    
    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
    
    def add_job(self, job_id: str, func, cron_expression: str):
        job = self.scheduler.add_job(
            func,
            'cron',
            **self._parse_cron(cron_expression),
            id=job_id
        )
        self.jobs[job_id] = job
        return job
    
    def _parse_cron(self, expression: str) -> dict:
        # Simple cron parser
        return {"minute": "*/5"}  # Every 5 minutes
    
    def remove_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]

task_scheduler = TaskScheduler()
EOF

echo "Creating websocket_handler.py..."
cat > clawcontrol/services/websocket_handler.py << 'EOF'
"""WebSocket Handler - Real-time updates"""
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

connection_manager = ConnectionManager()
EOF

echo "Creating permissions.py..."
cat > clawcontrol/services/permissions.py << 'EOF'
"""Permissions Management"""
from typing import Dict

class PermissionsManager:
    def __init__(self):
        self.permissions = {
            "filesystem_access": True,
            "network_access": True,
            "browser_access": True,
            "terminal_access": True
        }
    
    def check_permission(self, permission: str) -> bool:
        return self.permissions.get(permission, False)
    
    def set_permission(self, permission: str, enabled: bool):
        self.permissions[permission] = enabled
    
    def get_all(self) -> Dict:
        return self.permissions.copy()

permissions_manager = PermissionsManager()
EOF

echo "Creating process_manager.py..."
cat > clawcontrol/services/process_manager.py << 'EOF'
"""Advanced Process Management"""
import psutil
from typing import List, Dict

class ProcessManager:
    def get_process_info(self, pid: int) -> Dict:
        try:
            process = psutil.Process(pid)
            return {
                "pid": pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(),
                "memory_mb": process.memory_info().rss / (1024 * 1024)
            }
        except:
            return None
    
    def list_processes(self) -> List[Dict]:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                processes.append(proc.info)
            except:
                pass
        return processes

process_manager = ProcessManager()
EOF

echo "✅ All service files created!"

# Create scripts
echo "Creating install.sh..."
cat > install.sh << 'EOF'
#!/bin/bash
echo "🛡️ Installing Claw Control..."
pip install -r requirements.txt
cp .env.example .env
echo "✅ Installation complete! Edit .env and set CLAW_TOKEN"
EOF
chmod +x install.sh

echo "Creating setup.sh..."
cat > setup.sh << 'EOF'
#!/bin/bash
echo "🛡️ Setting up Claw Control..."
python -m clawcontrol.main
EOF
chmod +x setup.sh

echo "Creating mock_openclaw.sh..."
cat > mock_openclaw.sh << 'EOF'
#!/bin/bash
echo "Mock OpenClaw running..."
while true; do
    echo "[$(date)] OpenClaw processing..."
    sleep 2
done
EOF
chmod +x mock_openclaw.sh

echo "Creating verify_installation.py..."
cat > verify_installation.py << 'EOF'
"""Verify Claw Control installation"""
import sys

def verify():
    print("🛡️ Verifying Claw Control installation...")
    
    try:
        import fastapi
        print("✅ FastAPI installed")
    except:
        print("❌ FastAPI missing")
        return False
    
    try:
        import psutil
        print("✅ psutil installed")
    except:
        print("❌ psutil missing")
        return False
    
    print("✅ All checks passed!")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
EOF

echo "🎉 All files generated successfully!"
echo "Run: ./install.sh to install dependencies"
echo "Run: python -m clawcontrol.main to start the server"
