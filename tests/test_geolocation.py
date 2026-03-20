"""Tests for geolocation module.

NOTE: Intentionally incomplete - coverage will be below 80% threshold.
"""

from geolocation import GeoCache


class TestGeoCache:
    def test_cache_set_and_get(self):
        cache = GeoCache()
        cache.set("beijing", {"lat": 39.9, "lon": 116.4})
        result = cache.get("beijing")
        assert result["lat"] == 39.9
