"""
Configuration settings for the DOGE API Data Export Tool
"""

# Standard library imports
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Third-party imports
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL: str = os.getenv("DOGE_API_BASE_URL", "https://api.doge.gov")
API_KEY: Optional[str] = os.getenv("DOGE_API_KEY")
# Reference version only (not used in URL construction)
API_VERSION: str = os.getenv("DOGE_API_VERSION", "v0.0.2-beta")

# Request Configuration
REQUEST_TIMEOUT: int = int(os.getenv("DOGE_REQUEST_TIMEOUT", "30"))
REQUEST_MAX_RETRIES: int = int(os.getenv("DOGE_REQUEST_MAX_RETRIES", "3"))
MAX_RECORDS_PER_REQUEST: int = int(os.getenv("DOGE_MAX_RECORDS_PER_REQUEST", "1000"))

# Processing Configuration
BATCH_SIZE: int = int(os.getenv("DOGE_BATCH_SIZE", "100"))

# Output Configuration
OUTPUT_DIR: str = os.getenv("DOGE_OUTPUT_DIR", "doge_data")
EXCEL_ENGINE: str = os.getenv("DOGE_EXCEL_ENGINE", "openpyxl")
INCLUDE_TIMESTAMP: bool = os.getenv("DOGE_INCLUDE_TIMESTAMP", "True").lower() == "true"

# Logging Configuration
LOG_LEVEL: str = os.getenv("DOGE_LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler(), logging.FileHandler(Path(OUTPUT_DIR) / "doge_api.log")],
)

# Data type configurations
DATA_TYPES: Dict[str, Dict[str, Any]] = {
    # Current API endpoints
    "grants": {
        "endpoint": "/savings/grants",
        "id_field": "grant_id",
        "display_name": "Grant Savings",
    },
    "contracts": {
        "endpoint": "/savings/contracts",
        "id_field": "contract_id",
        "display_name": "Contract Savings",
    },
    "leases": {
        "endpoint": "/savings/leases",
        "id_field": "lease_id",
        "display_name": "Lease Savings",
    },
    # Legacy data types (no longer available)
    "departments": {
        "endpoint": "/departments",
        "id_field": "department_id",
        "display_name": "Departments",
    },
    "employees": {"endpoint": "/employees", "id_field": "employee_id", "display_name": "Employees"},
    "budget": {
        "endpoint": "/budget",
        "id_field": "budget_id",
        "display_name": "Budget Information",
    },
    "efficiency_metrics": {
        "endpoint": "/metrics",
        "id_field": "metric_id",
        "display_name": "Efficiency Metrics",
    },
    "projects": {
        "endpoint": "/projects",
        "id_field": "project_id",
        "display_name": "Projects and Initiatives",
    },
}
