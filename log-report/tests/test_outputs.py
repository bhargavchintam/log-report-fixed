import json
from pathlib import Path

import pytest

REPORT = Path("/app/report.json")

# Ground truth for the six-line access.log baked into the image. Computed by hand from
# the fixture and hardcoded here so the check can't be gamed by editing /app/access.log.
EXPECTED = {"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}


@pytest.fixture(scope="module")
def report():
    """Parse the report the agent was asked to write."""
    assert REPORT.exists(), "no /app/report.json was produced"
    try:
        return json.loads(REPORT.read_text())
    except json.JSONDecodeError as e:
        pytest.fail(f"/app/report.json is not valid JSON: {e}")


def test_is_json_object_with_exact_keys(report):
    """The report is a JSON object with exactly the three required keys."""
    assert isinstance(report, dict)
    assert set(report) == set(EXPECTED)


def test_total_requests(report):
    """total_requests counts every request in the log."""
    assert report["total_requests"] == EXPECTED["total_requests"]


def test_unique_ips(report):
    """unique_ips counts the distinct client IPs."""
    assert report["unique_ips"] == EXPECTED["unique_ips"]


def test_top_path(report):
    """top_path is the most frequently requested path."""
    assert report["top_path"] == EXPECTED["top_path"]
