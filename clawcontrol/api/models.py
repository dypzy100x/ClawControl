"""
Pydantic models for Claw Control API
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class GuardRule(BaseModel):
    """Guardrail rule model"""
    id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Human-readable rule name")
    block_patterns: List[str] = Field(default_factory=list, description="Patterns to block")
    allowed_paths: List[str] = Field(default_factory=list, description="Allowed file paths")
    rate_limit_per_min: int = Field(default=60, description="Max actions per minute")
    enabled: bool = Field(default=True, description="Whether rule is active")


class GuardRuleCreate(BaseModel):
    """Model for creating a new rule"""
    name: str
    block_patterns: List[str] = Field(default_factory=list)
    allowed_paths: List[str] = Field(default_factory=list)
    rate_limit_per_min: int = 60
    enabled: bool = True


class ViolationEvent(BaseModel):
    """Violation event model"""
    ts: datetime = Field(default_factory=datetime.now, description="Timestamp")
    rule_id: str = Field(..., description="ID of violated rule")
    log_excerpt: str = Field(..., description="Relevant log excerpt")
    severity: str = Field(default="warning", description="Severity level")


class OpenClawStatus(BaseModel):
    """OpenClaw status model"""
    running: bool = Field(..., description="Whether OpenClaw is running")
    pid: Optional[int] = Field(None, description="Process ID if running")
    last_seen: Optional[datetime] = Field(None, description="Last activity timestamp")


class OpenClawStartRequest(BaseModel):
    """Request to start OpenClaw"""
    openclaw_path: Optional[str] = Field("openclaw", description="Path to OpenClaw executable")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    version: str = "2.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)


class StatusResponse(BaseModel):
    """System status response"""
    health: str
    openclaw_status: OpenClawStatus
    last_violation: Optional[ViolationEvent] = None


class LogsResponse(BaseModel):
    """Logs response"""
    lines: List[str]
    total: int


class ViolationsResponse(BaseModel):
    """Violations response"""
    violations: List[ViolationEvent]
    total: int
