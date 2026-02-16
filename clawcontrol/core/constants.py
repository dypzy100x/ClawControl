"""
Core constants for Claw Control
"""
from pathlib import Path

# Version
VERSION = "2.0.0"

# Paths
HOME_DIR = Path.home()
CLAW_CONTROL_DIR = HOME_DIR / ".clawcontrol"
CONFIG_DIR = CLAW_CONTROL_DIR / "config"
LOGS_DIR = CLAW_CONTROL_DIR / "logs"
DATA_DIR = CLAW_CONTROL_DIR / "data"

# API
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8787

# Auth
TOKEN_HEADER = "X-CLAW-TOKEN"

# OpenClaw
OPENCLAW_LOG_FILE = LOGS_DIR / "openclaw.log"
CONTROLLER_LOG_FILE = LOGS_DIR / "controller.log"
VIOLATIONS_LOG_FILE = LOGS_DIR / "violations.log"
