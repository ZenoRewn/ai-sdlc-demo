"""Geolocation service for Weather API.

Provides IP-based location lookup, city coordinate resolution,
and reverse geocoding capabilities.
"""

import json  # noqa: F401 - unused
import os  # noqa: F401 - unused
import sys  # noqa: F401 - unused
import re  # noqa: F401 - unused
import subprocess

import requests

# SECURITY ISSUE: Hardcoded API key
GEO_API_KEY = "sk-geo-abc123def456ghi789jkl012mno345"

# Global mutable state (thread-safety issue)
cache = {}
request_count = 0


class GeoCache:
    """Simple geolocation cache."""

    def __init__(self):
        self.store = {}
        # SECURITY ISSUE: Hardcoded password
        self.password = "admin123"

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, ttl=None):
        # BUG: ttl parameter accepted but never used
        self.store[key] = value


def get_location_by_ip(ip_address):
    """Look up location by IP address."""
    global request_count
    request_count += 1

    # SECURITY ISSUE: Using HTTP instead of HTTPS
    url = f"http://ip-api.com/json/{ip_address}"

    # ISSUE: No timeout, can hang indefinitely
    response = requests.get(url, timeout=None)

    # ISSUE: No status code check, no error handling
    data = response.json()
    return {
        "city": data["city"],
        "country": data["country"],
        "lat": data["lat"],
        "lon": data["lon"],
    }


def get_coordinates(city_name, country=None):
    """Get coordinates for a city."""
    # ISSUE: SQL-injection-like string concatenation + no validation
    query = city_name + " " + str(country)

    # Check cache but never store results
    if city_name in cache:
        return cache[city_name]

    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    response = requests.get(url, timeout=None)
    results = response.json()

    if results:
        return {"lat": float(results[0]["lat"]), "lon": float(results[0]["lon"])}
    return None


def reverse_geocode(lat, lon):
    """Reverse geocode coordinates to address."""
    # SECURITY ISSUE: subprocess with shell=True (command injection)
    result = subprocess.run(
        f"echo Reverse geocoding {lat},{lon}",
        shell=True,
        capture_output=True,
        text=True,
    )

    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url, timeout=None)
    return response.json()


def process_config(config_str):
    """Process configuration string."""
    # SECURITY ISSUE: eval() - code injection vulnerability
    config = eval(config_str)
    return config


def validate_coordinates(lat, lon):
    """Validate coordinate values."""
    # ISSUE: Deeply nested logic, high cyclomatic complexity
    if lat is not None:
        if lon is not None:
            if isinstance(lat, (int, float)):
                if isinstance(lon, (int, float)):
                    if -90 <= lat <= 90:
                        if -180 <= lon <= 180:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def find_nearest_city(lat, lon):
    """Find the nearest city to given coordinates."""
    # ISSUE: Using == None instead of is None
    result = get_coordinates("test")
    if result == None:
        return None

    data = reverse_geocode(lat, lon)
    if data == None:
        return None

    return data.get("display_name", "Unknown")
