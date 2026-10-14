"""
Automated Unit Tests for Guitar Tuner Application
Used in Jenkins CI/CD Pipeline - Stage 2: Build & Test
"""

import pytest
from app import app, get_string_frequency, calculate_cents_offset, GUITAR_STRINGS


@pytest.fixture
def client():
    """Create Flask test client instance."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test that the Kubernetes health check endpoint returns 200 OK and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "guitar-tuner"
    assert "version" in data


def test_index_page(client):
    """Test that the home page loads successfully and contains guitar tuner elements."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Guitar Tuner" in html
    assert "Standard Tuning" in html


def test_strings_endpoint(client):
    """Test the strings API returns all 6 standard guitar strings."""
    response = client.get("/api/strings")
    assert response.status_code == 200
    data = response.get_json()
    assert "strings" in data
    assert len(data["strings"]) == 6

    # Verify first string (High E) and 6th string (Low E)
    low_e = next(s for s in data["strings"] if s["number"] == 6)
    high_e = next(s for s in data["strings"] if s["number"] == 1)
    assert low_e["note"] == "E"
    assert low_e["frequency"] == 82.41
    assert high_e["note"] == "E"
    assert high_e["frequency"] == 329.63


def test_version_endpoint(client):
    """Test the version endpoint returns valid application metadata."""
    response = client.get("/api/version")
    assert response.status_code == 200
    data = response.get_json()
    assert data["appName"] == "Guitar Tuner"
    assert "version" in data
    assert data["totalStrings"] == 6


def test_frequency_lookup():
    """Unit test for string frequency helper function."""
    assert get_string_frequency(6) == 82.41
    assert get_string_frequency(5) == 110.00
    assert get_string_frequency(4) == 146.83
    assert get_string_frequency(3) == 196.00
    assert get_string_frequency(2) == 246.94
    assert get_string_frequency(1) == 329.63
    assert get_string_frequency(999) is None


def test_cents_calculation():
    """Unit test for pitch offset calculation in cents."""
    # When frequency equals target, offset should be exactly 0 cents
    assert calculate_cents_offset(440.0, 440.0) == 0.0

    # One octave higher (880 vs 440) is exactly 1200 cents
    assert calculate_cents_offset(880.0, 440.0) == 1200.0

    # Invalid frequency check
    assert calculate_cents_offset(-10, 440.0) == 0.0
    assert calculate_cents_offset(440.0, 0) == 0.0
