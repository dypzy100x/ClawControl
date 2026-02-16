"""
Claw Control - Local Safety Orchestrator
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clawcontrol.api.routes import router
from clawcontrol.core.constants import VERSION

app = FastAPI(
    title="Claw Control",
    description="Local Safety Orchestrator for OpenClaw",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8787", "http://127.0.0.1:8787"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "Claw Control",
        "version": VERSION,
        "description": "Local Safety Orchestrator for OpenClaw",
        "disclaimer": "Claw Control is a community project and is not officially affiliated with or endorsed by OpenClaw",
        "docs": "/docs"
    }


def print_banner():
    """Print awesome ASCII banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║   ██████╗██╗      █████╗ ██╗    ██╗      ║
    ║  ██╔════╝██║     ██╔══██╗██║    ██║      ║
    ║  ██║     ██║     ███████║██║ █╗ ██║      ║
    ║  ██║     ██║     ██╔══██║██║███╗██║      ║
    ║  ╚██████╗███████╗██║  ██║╚███╔███╔╝      ║
    ║   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝       ║
    ║                                           ║
    ║   ██████╗████████╗██████╗ ██╗            ║
    ║  ██╔════╝╚══██╔══╝██╔══██╗██║            ║
    ║  ██║        ██║   ██████╔╝██║            ║
    ║  ██║        ██║   ██╔══██╗██║            ║
    ║  ╚██████╗   ██║   ██║  ██║███████╗       ║
    ║   ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝       ║
    ║                                           ║
    ║         🛡️  CLAW CONTROL 🛡️               ║
    ║   Local Runtime Controller for OpenClaw  ║
    ║              v0.1.0 (MVP)                 ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)


if __name__ == "__main__":
    import uvicorn
    from clawcontrol.core.config import config
    
    print_banner()
    print("🛡️  Claw Control - Local Safety Orchestrator")
    print(f"   Version: {VERSION}")
    print(f"   Binding to: {config.host}:{config.port}")
    print(f"   API docs available at http://{config.host}:{config.port}/docs")
    print()
    print("⚠️  Security Warning - Please Read:")
    print()
    print("   Claw Control is a powerful tool that manages OpenClaw processes.")
    print("   It can read files and execute actions if tools are enabled.")
    print("   Please ensure you understand what you're enabling.")
    print()
    print("🛡️  Recommended security baseline:")
    print("   • Review guardrail rules in ~/.clawcontrol/config/rules.json")
    print("   • Enable only necessary permissions (filesystem, browser, etc.)")
    print("   • Use strong token authentication")
    print("   • Run security audits regularly: openclaw security audit --deep")
    print()
    print("📖  Documentation: Check README.md and PROJECT_OVERVIEW.md")
    print("🔑  Your token is in .env (keep it secret!)")
    print()
    print("   Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        "clawcontrol.main:app",
        host=config.host,
        port=config.port,
        reload=True
    )
