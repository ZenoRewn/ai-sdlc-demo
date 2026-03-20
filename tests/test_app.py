"""Tests for Weather API."""

import pytest

from app import app, celsius_to_fahrenheit


@pytest.fixture
def client():
    """Create test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def api_headers():
    """Headers with valid API key."""
    return {"X-API-Key": "dev-key-change-me"}


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"

    def test_health_no_auth_required(self, client):
        response = client.get("/health")
        assert response.status_code == 200


class TestWeatherEndpoint:
    def test_valid_city(self, client, api_headers):
        response = client.get("/api/weather?city=Beijing", headers=api_headers)
        assert response.status_code == 200
        assert response.json["city"] == "Beijing"
        assert "temperature_c" in response.json
        assert "temperature_f" in response.json

    def test_invalid_city(self, client, api_headers):
        response = client.get("/api/weather?city=Atlantis", headers=api_headers)
        assert response.status_code == 404

    def test_missing_city(self, client, api_headers):
        response = client.get("/api/weather", headers=api_headers)
        assert response.status_code == 400

    def test_missing_api_key(self, client):
        response = client.get("/api/weather?city=Beijing")
        assert response.status_code == 401

    def test_invalid_api_key(self, client):
        response = client.get(
            "/api/weather?city=Beijing", headers={"X-API-Key": "wrong"}
        )
        assert response.status_code == 401

    def test_case_insensitive_city(self, client, api_headers):
        response = client.get("/api/weather?city=TOKYO", headers=api_headers)
        assert response.status_code == 200
        assert response.json["city"] == "Tokyo"


class TestTemperatureConversion:
    def test_freezing_point(self):
        assert celsius_to_fahrenheit(0) == 32.0

    def test_boiling_point(self):
        assert celsius_to_fahrenheit(100) == 212.0

    def test_body_temperature(self):
        assert celsius_to_fahrenheit(37) == 98.6

    def test_negative_temperature(self):
        assert celsius_to_fahrenheit(-40) == -40.0
