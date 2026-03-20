"""Weather API - Flask Application."""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEY = os.environ.get("WEATHER_API_KEY", "dev-key-change-me")

# Simulated weather data
WEATHER_DATA = {
    "beijing": {"temperature_c": 22.5, "condition": "sunny", "humidity": 45},
    "shanghai": {"temperature_c": 25.0, "condition": "cloudy", "humidity": 60},
    "tokyo": {"temperature_c": 18.0, "condition": "rainy", "humidity": 75},
    "london": {"temperature_c": 12.0, "condition": "overcast", "humidity": 80},
    "new york": {"temperature_c": 20.0, "condition": "clear", "humidity": 55},
}


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return round(celsius * 9 / 5 + 32, 1)


def require_api_key(f):
    """Decorator to require API key authentication."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized", "status": 401}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "weather-api"})


@app.route("/api/weather")
@require_api_key
def get_weather():
    """Get weather for a city."""
    city = request.args.get("city", "").strip().lower()
    if not city:
        return jsonify({"error": "Missing 'city' parameter", "status": 400}), 400

    weather = WEATHER_DATA.get(city)
    if not weather:
        return jsonify({"error": "City not found", "status": 404}), 404

    return jsonify(
        {
            "city": city.title(),
            "temperature_c": weather["temperature_c"],
            "temperature_f": celsius_to_fahrenheit(weather["temperature_c"]),
            "condition": weather["condition"],
            "humidity": weather["humidity"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
