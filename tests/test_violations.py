"""Tests for violations"""
import pytest
from clawcontrol.services.guardrails import GuardrailsEngine
from clawcontrol.api.models import GuardRuleCreate


@pytest.fixture
def engine(tmp_path):
    """Create engine"""
    from clawcontrol.core import constants
    constants.CONFIG_DIR = tmp_path / "config"
    constants.LOGS_DIR = tmp_path / "logs"
    constants.CONFIG_DIR.mkdir(parents=True)
    constants.LOGS_DIR.mkdir(parents=True)
    
    return GuardrailsEngine()


def test_evaluate_violation(engine):
    """Test violation detection (soft alert)"""
    rule = engine.create_rule(GuardRuleCreate(
        name="Test",
        block_patterns=["dangerous"]
    ))
    
    violation = engine.evaluate_log_line("dangerous command")
    assert violation is not None
    assert violation.rule_id == rule.id
