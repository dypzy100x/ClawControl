# 🛡️ Claw Control

**Local Safety Orchestrator for OpenClaw** - Phase 1 MVP

> **Community Disclaimer**: Claw Control is a community project and is not officially affiliated with or endorsed by OpenClaw.

## Overview

Claw Control is a **localhost-first safety orchestrator** providing guardrail enforcement, observability, and process management for OpenClaw agents. It operates in **soft alert mode** - violations are surfaced for admin review rather than triggering automatic actions.

## How It Works

```
OpenClaw Process → Log Capture → Guardrail Engine → Violation Detection → API → Admin Review & Action
```

**Flow**: Claw Control tails OpenClaw logs → evaluates lines against guard rules → surfaces violations via API → **you** review and take action.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone
git clone https://github.com/dypzy100x/ClawControl.git
cd ClawControl

# 2. Install
pip install -r requirements.txt

# 3. Generate token
openssl rand -hex 32

# 4. Configure
cp .env.example .env
# Edit .env and set CLAW_TOKEN

# 5. Run
python -m clawcontrol.main
```

API available at: `http://127.0.0.1:8787`

## 📚 API Reference

All requests require `X-CLAW-TOKEN` header.

### Endpoints

**Health & Status**
- `GET /api/health` - Health check
- `GET /api/status` - Combined status

**Rules (CRUD)**
- `GET /api/rules` - List all
- `POST /api/rules` - Create
- `GET /api/rules/{id}` - Get one
- `PUT /api/rules/{id}` - Update
- `DELETE /api/rules/{id}` - Delete

**Violations**
- `GET /api/violations?since=TIMESTAMP&limit=100`

**Logs**
- `GET /api/logs?tail=100`

**OpenClaw Control**
- `POST /api/openclaw/start`
- `POST /api/openclaw/stop`
- `GET /api/openclaw/status`

### Example

```bash
curl -H "X-CLAW-TOKEN: your-token" http://127.0.0.1:8787/api/health
```

## 🔒 Security

- **Localhost binding** (127.0.0.1 only)
- **Token auth** required
- **No code execution** from inputs
- **Non-destructive** adapter
- **Soft alert mode** - no auto-kill

## 📐 Data Models

### GuardRule
```json
{
  "id": "string",
  "name": "string",
  "block_patterns": ["string"],
  "allowed_paths": ["string"],
  "rate_limit_per_min": 60,
  "enabled": true
}
```

**Note**: Default patterns are examples - tune for your environment.

### ViolationEvent
```json
{
  "ts": "2026-02-16T00:00:00",
  "rule_id": "string",
  "log_excerpt": "string",
  "severity": "warning"
}
```

### OpenClawStatus
```json
{
  "running": true,
  "pid": 12345,
  "last_seen": "2026-02-16T00:00:00"
}
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 🏗️ Architecture

```
ClawControl/
├── clawcontrol/
│   ├── api/           # Routes, models, auth
│   ├── services/      # Guardrails, adapter
│   ├── core/          # Config, constants
│   └── main.py
├── config/            # rules.json, permissions.json
├── tests/             # pytest with mocks
└── README.md
```

## 🗺️ Roadmap

### Phase 1: Local Safety Orchestrator ✅
- Core API
- Soft alert mode
- Pattern guardrails

### Phase 2: Global Safety Orchestrator 🔲
- Cloud deployment
- Multi-instance management
- Advanced detection

### Phase 3: Plugin SDK 🔲
- Custom plugins
- Marketplace
- Community extensions

## 🔌 Extensibility

Future plugin architecture for:
- Custom guard logic
- Adapter plugins
- Integration hooks

## 🐳 Docker (Optional)

```bash
docker build -t claw-control .
docker run -p 127.0.0.1:8787:8787 -e CLAW_TOKEN=token claw-control
```

## 🔧 Troubleshooting

**"CLAW_TOKEN must be set"**
```bash
cp .env.example .env
# Edit .env
```

**"OpenClaw not found"**
```bash
# Specify full path in start request
{"openclaw_path": "/path/to/openclaw"}
```

**Port in use**
```bash
# Change in .env
PORT=8788
```

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Add tests
4. Submit PR

## 📄 License

MIT License

---

**Built with 🛡️ for safe AI orchestration**

*Not affiliated with OpenClaw*
