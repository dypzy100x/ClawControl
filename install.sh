#!/bin/bash
echo "🛡️ Installing Claw Control..."
pip install -r requirements.txt
cp .env.example .env
echo "✅ Installation complete! Edit .env and set CLAW_TOKEN"
