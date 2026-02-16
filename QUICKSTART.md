# 🚀 Quick Start

## Install

```bash
./install.sh
```

## Configure

```bash
# Edit .env
CLAW_TOKEN=$(openssl rand -hex 32)
```

## Run

```bash
python -m clawcontrol.main
```

## Test

```bash
curl -H "X-CLAW-TOKEN: your-token" http://127.0.0.1:8787/api/health
```

That's it! 🛡️
