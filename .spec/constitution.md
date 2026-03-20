# Project Constitution

## Technology Stack
- **Language**: Python 3.11+
- **Framework**: Flask
- **Testing**: pytest with pytest-cov
- **Linting**: flake8, black (formatter)
- **Deployment**: Docker → Azure Container Apps

## Code Standards
- Follow PEP 8 style guidelines
- All code must pass `black --check` formatting
- All code must pass `flake8` linting
- No hardcoded secrets or credentials in source code
- Use environment variables for configuration

## Testing Requirements
- Minimum **80% code coverage**
- All API endpoints must have unit tests
- Test both success and error paths
- Mock external API calls in tests

## Security Requirements
- All API endpoints require authentication (API key via header)
- Use HTTPS for all external API calls
- No use of `eval()`, `exec()`, or `subprocess` with `shell=True`
- Input validation on all user-provided data
- Secrets loaded from environment variables only

## API Design
- RESTful JSON API
- Consistent error response format
- Proper HTTP status codes
