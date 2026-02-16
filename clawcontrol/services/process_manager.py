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
