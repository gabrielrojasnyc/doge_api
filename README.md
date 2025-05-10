# DOGE API Data Export Tool

This tool allows you to interact with the DOGE (Department of Government Efficiency) API and export data to Excel files.

![Video](/assets/Video_Ready_Saving_Money.gif)

## Overview

The DOGE API provides access to government efficiency and savings data, including:

- Grants savings data
- Contracts savings data
- Lease savings data
- Legacy data (departments, employees, budget, efficiency metrics, projects)

This tool provides a flexible framework for:

- Making requests to the API
- Processing the JSON responses
- Exporting the data to Excel files

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd doge_api
```

2. Set up the environment:
```bash
python setup.py
```

This will:
- Create a virtual environment
- Install dependencies
- Create a .env file from the sample
- Create the data directory

3. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Basic Command Line Usage

The tool can be used from the command line to export data:

```bash
# Export all current data types
python doge_api_processor.py --all

# Export specific data type
python doge_api_processor.py --data-type grants
python doge_api_processor.py --data-type contracts
python doge_api_processor.py --data-type leases

# Export with filters
python doge_api_processor.py --data-type grants --filter "sort_by=savings"

# Specify output directory
python doge_api_processor.py --all --output-dir exports

# Disable timestamp in filenames
python doge_api_processor.py --all --no-timestamp
```

### Programmatic Usage

You can also use the API client programmatically in your own Python scripts:

```python
from doge_api_client import DogeApiClient

# Initialize client
client = DogeApiClient(api_key="your_api_key")

# Get grants data
grants = client.get_grants_data()

# Get contracts data with filter
contracts = client.get_contracts_data(sort_by="savings", sort_order="desc")

# Export data to Excel
file_path = client.export_to_excel(contracts, "contracts_savings", "Contract Savings")
print(f"Data exported to: {file_path}")

# Export all available data
results = client.export_all_data()
```

Check the `example_usage.py` file for more detailed examples.

## Configuration

You can customize the tool's behavior through environment variables or by modifying the `config.py` file:

| Setting | Description | Default |
|---------|-------------|---------|
| API_BASE_URL | Base URL for the DOGE API | https://api.doge.gov |
| API_KEY | API key for authentication | - |
| API_VERSION | API version | v0.0.2-beta |
| REQUEST_TIMEOUT | Request timeout in seconds | 30 |
| REQUEST_MAX_RETRIES | Maximum number of retry attempts | 3 |
| OUTPUT_DIR | Directory for exported files | doge_data |
| LOG_LEVEL | Logging level (INFO, DEBUG, etc.) | INFO |
| MAX_RECORDS_PER_REQUEST | Maximum records per API request | 1000 |
| BATCH_SIZE | Batch size for processing large datasets | 100 |
| EXCEL_ENGINE | Excel engine (openpyxl, xlsxwriter) | openpyxl |
| INCLUDE_TIMESTAMP | Include timestamp in filenames | True |

## File Structure

```
.
├── README.md               # This documentation
├── CLAUDE.md               # Instructions for Claude Code
├── requirements.txt        # Python dependencies
├── config.py               # Configuration settings
├── doge_api_client.py      # Core API client
├── doge_api_processor.py   # Command-line data processor
├── main.py                 # Alternative CLI interface
├── utils.py                # Utility functions
├── example_usage.py        # Example usage
├── setup.py                # Setup script
└── doge_data/              # Default output directory
```

## Supported Data Types

The tool currently supports exporting the following data types:

### Current API Endpoints
- **Grants** - Grant savings data
- **Contracts** - Contract savings data
- **Leases** - Lease savings data

### Legacy API Endpoints (may not be available)
- **Departments** - Information about government departments
- **Employees** - Employee data including position, salary, etc.
- **Budget** - Budget information by department and fiscal year
- **Efficiency Metrics** - Performance and efficiency metrics
- **Projects** - Information about government projects and initiatives

## API Structure Notes

- **Base URL**: https://api.doge.gov
- **Version**: No version prefix needed in URL
- **Authentication**: API key via X-Api-Key header
- **Endpoints**:
  - /savings/grants
  - /savings/contracts
  - /savings/leases

### Common Parameters
- sort_by=savings (or value, date)
- sort_order=asc|desc
- page=1 (minimum 1)
- per_page=100 (between 1-500, default 100)

### Response Format
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

## Error Handling

The tool includes robust error handling and logging:

- Connection errors are automatically retried with exponential backoff
- All errors are logged to both console and log file
- Specific error types (connection, timeout, HTTP) have dedicated handling
- Detailed error messages help diagnose issues

## Development

The codebase follows these guidelines:
- **Imports**: Organized in groups (standard lib, third-party, local)
- **Formatting**: Black with 100 character line length
- **Types**: Static typing with explicit return types (uses typing module)
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Error Handling**: Use specific exceptions with try/except blocks
- **Documentation**: Use docstrings for all modules, classes, and functions
- **Environment Variables**: Use dotenv for configuration
- **Logging**: Use the logging module with appropriate levels

## License

This project is licensed under the MIT License - see the LICENSE file for details.