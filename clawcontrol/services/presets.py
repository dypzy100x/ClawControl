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
