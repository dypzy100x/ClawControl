"""Tests for health endpoint"""
import pytest
from fastapi.testclient import TestClient
from clawcontrol.main import app

TEST_TOKEN = "test-token-123"


@pytest.fixture
def client(monkeypatch):
    """Create test client"""
    monkeypatch.setenv("CLAW_TOKEN", TEST_TOKEN)
    from clawcontrol.core import config as config_module
    config_module.config = config_module.Config()
    return TestClient(app)


def test_health_check(client):
    """Test health endpoint"""
    headers = {"X-CLAW-TOKEN": TEST_TOKEN}
    response = client.get("/api/health", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
