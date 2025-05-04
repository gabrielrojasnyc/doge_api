# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands
- Setup: `python setup.py`
- Run: `python doge_api_processor.py --all`
- Run specific data type: `python doge_api_processor.py --data-type savings --filter "sort_by=savings"`
- Lint: `flake8 *.py`
- Format: `black *.py` 
- Type check: `mypy --ignore-missing-imports *.py`
- Test: `pytest -v`
- Run single test: `pytest -v tests/test_file.py::test_function`

## API Structure Notes
- Base URL: https://api.doge.gov
- Version: No version prefix needed in URL
- Authentication: API key via X-Api-Key header
- Endpoints:
  - /savings/grants
  - /savings/contracts
  - /savings/leases
- Common Parameters: 
  - sort_by=savings (or value, date)
  - sort_order=asc|desc
  - page=1 (minimum 1)
  - per_page=100 (between 1-500, default 100)
- Response Format: JSON with nested structure:
  ```json
  {
    "success": true,
    "result": {
      "grants": [{"date": "...", "value": 123, "savings": 456, ...}],
      "contracts": [...],
      "leases": [...]
    },
    "meta": {"total_results": 123, "pages": 2}
  }
  ```

## Code Style Guidelines
- **Imports**: Organize in groups (standard lib, third-party, local)
- **Formatting**: Black with 100 character line length
- **Types**: Static typing with explicit return types (use typing module)
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use specific exceptions with try/except blocks
- **Documentation**: Use docstrings for all modules, classes, and functions
- **Environment Variables**: Use dotenv for configuration
- **Logging**: Use the logging module with appropriate levels