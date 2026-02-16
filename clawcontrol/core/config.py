"""
Configuration management for Claw Control
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from .constants import CONFIG_DIR, LOGS_DIR, DATA_DIR

load_dotenv()


class Config:
    """Application configuration"""
    
    def __init__(self):
        # Ensure directories exist
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Auth
        self.claw_token = os.getenv("CLAW_TOKEN", "")
        if not self.claw_token:
            raise ValueError("CLAW_TOKEN must be set in environment or .env file")
        
        # Server
        self.host = os.getenv("HOST", "127.0.0.1")
        self.port = int(os.getenv("PORT", "8787"))
        
        # Paths
        self.config_dir = CONFIG_DIR
        self.logs_dir = LOGS_DIR
        self.data_dir = DATA_DIR
        
        self.rules_file = CONFIG_DIR / "rules.json"
        self.permissions_file = CONFIG_DIR / "permissions.json"
    
    def load_json_file(self, filepath: Path, default: dict = None) -> dict:
        """Load JSON file with fallback to default"""
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        return default or {}
    
    def save_json_file(self, filepath: Path, data: dict) -> None:
        """Save data to JSON file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


config = Config()
