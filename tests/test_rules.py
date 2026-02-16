"""Tests for rules endpoints"""
import pytest
from fastapi.testclient import TestClient
from clawcontrol.main import app

TEST_TOKEN = "test-token-123"


@pytest.fixture
def client(monkeypatch, tmp_path):
    """Create test client"""
    monkeypatch.setenv("CLAW_TOKEN", TEST_TOKEN)
    from clawcontrol.core import constants
    constants.CONFIG_DIR = tmp_path / "config"
    constants.LOGS_DIR = tmp_path / "logs"
    constants.CONFIG_DIR.mkdir(parents=True)
    
    from clawcontrol.core import config as config_module
    config_module.config = config_module.Config()
    
    from clawcontrol.services import guardrails as guardrails_module
    guardrails_module.guardrails_engine = guardrails_module.GuardrailsEngine()
    
    return TestClient(app)


def test_create_rule(client):
    """Test creating a rule"""
    headers = {"X-CLAW-TOKEN": TEST_TOKEN}
    rule_data = {
        "name": "Test Rule",
        "block_patterns": ["test"],
        "rate_limit_per_min": 100
    }
    
    response = client.post("/api/rules", json=rule_data, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
