"""
OpenClaw Adapter - Non-destructive wrapper
"""
import subprocess
import psutil
from datetime import datetime
from typing import Optional, List
from clawcontrol.core.constants import OPENCLAW_LOG_FILE
from clawcontrol.api.models import OpenClawStatus


class OpenClawAdapter:
    """Non-intrusive, mockable wrapper around OpenClaw"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.pid: Optional[int] = None
        self.log_file = OPENCLAW_LOG_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def start(self, openclaw_path: str = "openclaw") -> OpenClawStatus:
        """Start OpenClaw process (non-destructive)"""
        if self.is_running():
            return self.status()
        
        try:
            log_handle = open(self.log_file, 'a')
            
            self.process = subprocess.Popen(
                [openclaw_path],
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE
            )
            
            self.pid = self.process.pid
            
            return OpenClawStatus(
                running=True,
                pid=self.pid,
                last_seen=datetime.now()
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"OpenClaw executable not found: {openclaw_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to start OpenClaw: {str(e)}")
    
    def stop(self) -> OpenClawStatus:
        """Stop OpenClaw gracefully (non-destructive)"""
        if not self.is_running():
            return self.status()
        
        try:
            self.process.terminate()
            
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            self.process = None
            self.pid = None
            
            return OpenClawStatus(
                running=False,
                pid=None,
                last_seen=datetime.now()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to stop OpenClaw: {str(e)}")
    
    def status(self) -> OpenClawStatus:
        """Get current OpenClaw status"""
        running = self.is_running()
        
        return OpenClawStatus(
            running=running,
            pid=self.pid if running else None,
            last_seen=datetime.now() if running else None
        )
    
    def is_running(self) -> bool:
        """Check if OpenClaw process is running"""
        if self.process is None or self.pid is None:
            return False
        
        try:
            process = psutil.Process(self.pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def logs(self, tail: int = 100) -> List[str]:
        """Get last N lines from OpenClaw log (read-only)"""
        if not self.log_file.exists():
            return []
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                return lines[-tail:] if len(lines) > tail else lines
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []


openclaw_adapter = OpenClawAdapter()
