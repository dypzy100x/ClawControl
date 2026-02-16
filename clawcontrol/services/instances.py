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
