# Weather API Feature Spec

## Overview
A RESTful weather API that provides current weather data for cities.

## Endpoints

### GET /health
- Returns service health status
- No authentication required

### GET /api/weather?city={city_name}
- Returns current weather data for the specified city
- Requires API key authentication via `X-API-Key` header
- Returns temperature in Celsius and Fahrenheit

## Authentication
- API key passed via `X-API-Key` header
- Invalid or missing key returns 401

## Response Format
```json
{
  "city": "Beijing",
  "temperature_c": 22.5,
  "temperature_f": 72.5,
  "condition": "sunny",
  "humidity": 45
}
```

## Error Response
```json
{
  "error": "City not found",
  "status": 404
}
```

## Acceptance Criteria
- [ ] Health endpoint returns 200 with status
- [ ] Weather endpoint requires valid API key
- [ ] Temperature conversion is accurate (C to F)
- [ ] Invalid city returns 404
- [ ] Missing API key returns 401
- [ ] >= 80% unit test coverage
