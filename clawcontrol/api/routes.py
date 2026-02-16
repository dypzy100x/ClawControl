"""
API Routes for Claw Control (Phase 1 LSO MVP)
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from clawcontrol.api.auth import verify_token
from clawcontrol.api.models import (
    GuardRule,
    GuardRuleCreate,
    ViolationEvent,
    OpenClawStatus,
    OpenClawStartRequest,
    HealthResponse,
    StatusResponse,
    LogsResponse,
    ViolationsResponse,
)
from clawcontrol.services.guardrails import guardrails_engine
from clawcontrol.services.openclaw_adapter import openclaw_adapter

router = APIRouter(prefix="/api", dependencies=[Depends(verify_token)])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Get combined system status"""
    openclaw_status = openclaw_adapter.status()
    violations = guardrails_engine.get_violations(limit=1)
    last_violation = violations[0] if violations else None
    
    return StatusResponse(
        health="ok",
        openclaw_status=openclaw_status,
        last_violation=last_violation
    )


@router.get("/rules", response_model=List[GuardRule])
async def get_rules():
    """Get all guardrail rules"""
    return guardrails_engine.get_all_rules()


@router.post("/rules", response_model=GuardRule)
async def create_rule(rule: GuardRuleCreate):
    """Create a new guardrail rule"""
    return guardrails_engine.create_rule(rule)


@router.get("/rules/{rule_id}", response_model=GuardRule)
async def get_rule(rule_id: str):
    """Get specific rule by ID"""
    rule = guardrails_engine.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/rules/{rule_id}", response_model=GuardRule)
async def update_rule(rule_id: str, rule_data: dict):
    """Update existing rule"""
    rule = guardrails_engine.update_rule(rule_id, rule_data)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    """Delete a rule"""
    deleted = guardrails_engine.delete_rule(rule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "deleted", "rule_id": rule_id}


@router.get("/violations", response_model=ViolationsResponse)
async def get_violations(
    since: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000)
):
    """Get violation events"""
    violations = guardrails_engine.get_violations(since=since, limit=limit)
    return ViolationsResponse(
        violations=violations,
        total=len(violations)
    )


@router.get("/logs", response_model=LogsResponse)
async def get_logs(tail: int = Query(100, ge=1, le=1000)):
    """Get OpenClaw logs"""
    lines = openclaw_adapter.logs(tail=tail)
    return LogsResponse(
        lines=lines,
        total=len(lines)
    )


@router.post("/openclaw/start", response_model=OpenClawStatus)
async def start_openclaw(request: OpenClawStartRequest = OpenClawStartRequest()):
    """Start OpenClaw process"""
    try:
        return openclaw_adapter.start(openclaw_path=request.openclaw_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/openclaw/stop", response_model=OpenClawStatus)
async def stop_openclaw():
    """Stop OpenClaw gracefully"""
    try:
        return openclaw_adapter.stop()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/openclaw/status", response_model=OpenClawStatus)
async def get_openclaw_status():
    """Get OpenClaw status"""
    return openclaw_adapter.status()
