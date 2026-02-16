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
