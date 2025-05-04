#!/usr/bin/env python3
"""
Main entry point for DOGE API Data Export Tool

This is a command-line wrapper for the doge_api_processor module.
"""

# Standard library imports
import argparse
import logging
import sys
from typing import Dict, List, Optional, Any

# Local imports
import config
from doge_api_client import DogeApiClient
from doge_api_processor import (
    export_all_data,
    export_department_data,
    export_employee_data,
    export_budget_data,
    export_efficiency_metrics,
    export_projects_data,
    export_grants_data,
    export_contracts_data,
    export_leases_data,
    parse_filter,
)
from utils import setup_logging


def setup_parser() -> argparse.ArgumentParser:
    """
    Set up command line argument parser

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="DOGE API Data Export Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --all
  python main.py --data-type departments
  python main.py --data-type employees --filter "department=Treasury"
  python main.py --all --output-dir exports
  python main.py --all --no-timestamp
""",
    )

    # Define argument groups
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Export all data types")
    group.add_argument(
        "--data-type",
        choices=[
            # Current data types
            "grants",
            "contracts",
            "leases",
            # Legacy data types
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
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    return parser


def main():
    """
    Main entry point for the application
    """
    # Parse command line arguments
    parser = setup_parser()
    args = parser.parse_args()

    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level=log_level, log_file="doge_export.log")
    logger = logging.getLogger("doge_export")

    # Update config from command line arguments
    if args.output_dir:
        config.OUTPUT_DIR = args.output_dir

    if args.no_timestamp:
        config.INCLUDE_TIMESTAMP = False

    # Parse filters
    filters = parse_filter(args.filter)

    try:
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
                    print(f" {data_type}: {file_path}")
                else:
                    print(f"L {data_type}: Failed to export")
        else:
            # Export specific data type
            data_type = args.data_type
            logger.info(f"Exporting {data_type} data...")

            # Current data types
            if data_type == "grants":
                file_path = export_grants_data(client, filters)
            elif data_type == "contracts":
                file_path = export_contracts_data(client, filters)
            elif data_type == "leases":
                file_path = export_leases_data(client, filters)
            # Legacy data types
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
                print(f"\n Successfully exported {data_type} data to: {file_path}")
            else:
                print(f"\nL Failed to export {data_type} data")

    except ValueError as e:
        logger.error(f"Parameter error: {str(e)}")
        print(f"\n❌ Parameter error: {str(e)}")
        print("Please check your command line arguments and try again.")
        sys.exit(1)
    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        print(f"\n❌ Connection error: {str(e)}")
        print("Please check your internet connection and API configuration.")
        sys.exit(2)
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        print(f"\n❌ Timeout error: {str(e)}")
        print("Try increasing the timeout in the configuration or check server status.")
        sys.exit(3)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check the logs for more details.")
        sys.exit(99)

    sys.exit(0)


if __name__ == "__main__":
    main()
