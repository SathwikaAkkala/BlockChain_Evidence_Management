"""
Backend API Test Suite
Tests /submit endpoint
"""

import os
import requests
import tempfile


BASE_URL = "http://127.0.0.1:8000"


def test_server_running():
    """
    Check if backend server is up
    """

    try:
        res = requests.get(f"{BASE_URL}/docs")
        assert res.status_code == 200
    except Exception:
        assert False, "Backend server is not running"


def test_submit_file():
    """
    Test file upload to /submit
    """

    # Create temporary test file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Test cybercrime evidence file")
        tmp_path = tmp.name

    files = {
        "file": open(tmp_path, "rb")
    }

    res = requests.post(
        f"{BASE_URL}/submit",
        files=files
    )

    os.unlink(tmp_path)

    # Validate response
    assert res.status_code == 200

    data = res.json()

    assert "id" in data
    assert "cid" in data
    assert "hash" in data
    assert data["status"] == "success"


def test_submit_without_file():
    """
    Test submitting without file
    """

    res = requests.post(f"{BASE_URL}/submit")

    assert res.status_code in [400, 422]
