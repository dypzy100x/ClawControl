"""Tests for OpenClaw adapter (mocked)"""
import pytest
from unittest.mock import patch, MagicMock
from clawcontrol.services.openclaw_adapter import OpenClawAdapter


@pytest.fixture
def adapter(tmp_path):
    """Create adapter with temp log"""
    adapter = OpenClawAdapter()
    adapter.log_file = tmp_path / "openclaw.log"
    return adapter


@patch('subprocess.Popen')
def test_start_openclaw(mock_popen, adapter):
    """Test starting OpenClaw"""
    mock_process = MagicMock()
    mock_process.pid = 12345
    mock_popen.return_value = mock_process
    
    status = adapter.start()
    assert status.running is True
    assert status.pid == 12345
