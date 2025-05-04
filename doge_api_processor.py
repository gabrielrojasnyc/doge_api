#!/usr/bin/env python3
"""
DOGE API Data Processor
-----------------------
This script fetches data from the DOGE API and exports it to Excel files.
It can export various types of government data including:
- Departments
- Employees 
- Budget information
- Efficiency metrics
- Projects and initiatives

Usage:
    python doge_api_processor.py --all
    python doge_api_processor.py --data-type departments
    python doge_api_processor.py --data-type employees --filter "department=Treasury"
"""

# Standard library imports
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Third-party imports
import pandas as pd
from dotenv import load_dotenv

# Local imports
import config
from doge_api_client import DogeApiClient
from utils import process_data, save_to_excel, setup_logging

# Set up logging
setup_logging(log_file="doge_processor.log")
logger = logging.getLogger("doge_processor")


def parse_filter(filter_str: Optional[str]) -> Dict[str, str]:
    """
    Parse filter string into a dictionary

    Args:
        filter_str: Filter string in the format "key1=value1,key2=value2"

    Returns:
        Dictionary of filter parameters

    Raises:
        ValueError: If the filter string is improperly formatted
    """
    if not filter_str:
        return {}

    filters = {}
    try:
        for item in filter_str.split(","):
            item = item.strip()
            if not item:
                continue

            if "=" not in item:
                raise ValueError(f"Filter '{item}' does not contain '=' separator")

            key, value = item.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ValueError(f"Empty key found in filter '{item}'")

            filters[key] = value

    except ValueError as e:
        # Re-raise ValueError for specific parsing errors
        logger.error(f"Error parsing filter string: {str(e)}")
        raise
    except Exception as e:
        # Catch other unexpected errors
        logger.error(f"Unexpected error parsing filter string: {str(e)}")
        raise ValueError(f"Failed to parse filter string '{filter_str}': {str(e)}")

    # Log the parsed filters
    logger.debug(f"Parsed filters: {filters}")
    return filters


def export_department_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export department data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching department data...")
    try:
        # Get department data with filters
        data = client.get_department_data(**(filters or {}))

        # Process the data
        df = process_data(data)

        # Save to Excel
        return save_to_excel(df, "departments", "Departments")
    except Exception as e:
        logger.error(f"Failed to export department data: {str(e)}")
        return ""


def export_employee_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export employee data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching employee data...")
    try:
        # Get employee data with filters
        data = client.get_employee_data(**(filters or {}))

        # Process the data
        transformations = {
            "salary": lambda x: float(x) if x else 0,
            "hire_date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "employees", "Employees")
    except Exception as e:
        logger.error(f"Failed to export employee data: {str(e)}")
        return ""


def export_budget_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export budget data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching budget data...")
    try:
        # Get budget data with filters
        data = client.get_budget_data(**(filters or {}))

        # Process the data
        transformations = {
            "amount": lambda x: float(x) if x else 0,
            "fiscal_year": lambda x: int(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "budget", "Budget")
    except Exception as e:
        logger.error(f"Failed to export budget data: {str(e)}")
        return ""


def export_efficiency_metrics(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export efficiency metrics to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching efficiency metrics...")
    try:
        # Get efficiency metrics with filters
        data = client.get_efficiency_metrics(**(filters or {}))

        # Process the data
        transformations = {
            "value": lambda x: float(x) if x else 0,
            "target": lambda x: float(x) if x else 0,
            "date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "efficiency_metrics", "Efficiency Metrics")
    except Exception as e:
        logger.error(f"Failed to export efficiency metrics: {str(e)}")
        return ""


def export_projects_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export projects data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching projects data...")
    try:
        # Get projects data with filters
        data = client.get_projects_data(**(filters or {}))

        # Process the data
        transformations = {
            "budget": lambda x: float(x) if x else 0,
            "start_date": lambda x: pd.to_datetime(x) if x else None,
            "end_date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "projects", "Projects")
    except Exception as e:
        logger.error(f"Failed to export projects data: {str(e)}")
        return ""


def export_grants_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export grants savings data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching grants savings data...")
    try:
        # Get grants data with filters
        data = client.get_grants_data(**(filters or {}))

        # Process the data
        transformations = {
            "value": lambda x: float(x) if x else 0,
            "savings": lambda x: float(x) if x else 0,
            "date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "grants_savings", "Grant Savings")
    except Exception as e:
        logger.error(f"Failed to export grants data: {str(e)}")
        return ""


def export_contracts_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export contracts savings data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching contracts savings data...")
    try:
        # Get contracts data with filters
        data = client.get_contracts_data(**(filters or {}))

        # Process the data
        transformations = {
            "value": lambda x: float(x) if x else 0,
            "savings": lambda x: float(x) if x else 0,
            "date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "contracts_savings", "Contract Savings")
    except Exception as e:
        logger.error(f"Failed to export contracts data: {str(e)}")
        return ""


def export_leases_data(client: DogeApiClient, filters: Dict = None) -> str:
    """
    Export leases savings data to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Path to saved file
    """
    logger.info("Fetching leases savings data...")
    try:
        # Get leases data with filters
        data = client.get_leases_data(**(filters or {}))

        # Process the data
        transformations = {
            "value": lambda x: float(x) if x else 0,
            "savings": lambda x: float(x) if x else 0,
            "date": lambda x: pd.to_datetime(x) if x else None,
        }
        df = process_data(data, transformations)

        # Save to Excel
        return save_to_excel(df, "leases_savings", "Lease Savings")
    except Exception as e:
        logger.error(f"Failed to export leases data: {str(e)}")
        return ""


def export_all_data(client: DogeApiClient, filters: Dict = None) -> Dict[str, str]:
    """
    Export all available data types to Excel

    Args:
        client: API client instance
        filters: Optional filters to apply

    Returns:
        Dictionary mapping data types to file paths
    """
    results = {}

    # Export current data types
    try:
        results["grants"] = export_grants_data(client, filters)
    except Exception as e:
        logger.error(f"Failed to export grants data: {str(e)}")
        results["grants"] = ""

    try:
        results["contracts"] = export_contracts_data(client, filters)
    except Exception as e:
        logger.error(f"Failed to export contracts data: {str(e)}")
        results["contracts"] = ""

    try:
        results["leases"] = export_leases_data(client, filters)
    except Exception as e:
        logger.error(f"Failed to export leases data: {str(e)}")
        results["leases"] = ""

    return results


def main():
    """
    Main entry point for the script
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DOGE API Data Processor")

    # Define argument groups
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Export all data types")
    group.add_argument(
        "--data-type",
        choices=[
            # Current endpoints
            "grants",
            "contracts",
            "leases",
            # Legacy endpoints (no longer available)
            "departments",
            "employees",
            "budget",
            "efficiency_metrics",
            "projects",
        ],
        help="Data type to export",
    )

    parser.add_argument("--filter", help="Filter in format 'key1=value1,key2=value2'")
    parser.add_argument("--output-dir", help="Output directory for Excel files")
    parser.add_argument(
        "--no-timestamp", action="store_true", help="Disable timestamp in filenames"
    )

    args = parser.parse_args()

    # Update config from command line arguments
    if args.output_dir:
        config.OUTPUT_DIR = args.output_dir

    if args.no_timestamp:
        config.INCLUDE_TIMESTAMP = False

    # Parse filters
    filters = parse_filter(args.filter)

    # Initialize API client
    client = DogeApiClient(base_url=config.API_BASE_URL, api_key=config.API_KEY)

    # Export data based on arguments
    if args.all:
        logger.info("Exporting all data types...")
        results = export_all_data(client, filters)

        # Print summary
        print("\nExport Summary:")
        for data_type, file_path in results.items():
            if file_path:
                print(f"✅ {data_type}: {file_path}")
            else:
                print(f"❌ {data_type}: Failed to export")
    else:
        # Export specific data type
        data_type = args.data_type
        logger.info(f"Exporting {data_type} data...")

        # Handle current data types
        if data_type == "grants":
            file_path = export_grants_data(client, filters)
        elif data_type == "contracts":
            file_path = export_contracts_data(client, filters)
        elif data_type == "leases":
            file_path = export_leases_data(client, filters)
        # Handle legacy data types (will likely fail with 404)
        elif data_type == "departments":
            file_path = export_department_data(client, filters)
        elif data_type == "employees":
            file_path = export_employee_data(client, filters)
        elif data_type == "budget":
            file_path = export_budget_data(client, filters)
        elif data_type == "efficiency_metrics":
            file_path = export_efficiency_metrics(client, filters)
        elif data_type == "projects":
            file_path = export_projects_data(client, filters)

        # Print result
        if file_path:
            print(f"\n✅ Successfully exported {data_type} data to: {file_path}")
        else:
            print(f"\n❌ Failed to export {data_type} data")


if __name__ == "__main__":
    main()
