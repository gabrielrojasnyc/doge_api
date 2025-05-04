#!/usr/bin/env python3
"""
Example usage of the DOGE API client
"""
from doge_api_client import DogeApiClient


def example_1_basic_usage():
    """
    Basic usage example
    """
    print("\n=== Example 1: Basic Usage ===")

    # Initialize client
    client = DogeApiClient()

    # Get and export department data
    print("Fetching department data...")
    try:
        departments = client.get_department_data()
        print(f"Found {len(departments)} departments")

        # Export to Excel
        file_path = client.export_to_excel(departments, "departments", "Departments")
        print(f"Exported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


def example_2_filtered_data():
    """
    Example with filtered data
    """
    print("\n=== Example 2: Filtered Data ===")

    # Initialize client
    client = DogeApiClient()

    # Get and export employee data with filter
    print("Fetching employee data for Treasury department...")
    try:
        employees = client.get_employee_data(department="Treasury")
        print(f"Found {len(employees)} employees in Treasury")

        # Export to Excel
        file_path = client.export_to_excel(employees, "treasury_employees", "Treasury Employees")
        print(f"Exported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


def example_3_export_all():
    """
    Example exporting all data
    """
    print("\n=== Example 3: Export All Data ===")

    # Initialize client
    client = DogeApiClient()

    # Export all data
    print("Exporting all data...")
    try:
        result = client.export_all_data()

        # Print summary
        print("\nExport Summary:")
        for data_type, file_path in result.items():
            if file_path:
                print(f"✅ {data_type}: {file_path}")
            else:
                print(f"❌ {data_type}: Failed to export")
    except Exception as e:
        print(f"Error: {str(e)}")


def example_4_custom_endpoint():
    """
    Example with custom endpoint
    """
    print("\n=== Example 4: Custom Endpoint ===")

    # Initialize client
    client = DogeApiClient()

    # Get data from a custom endpoint
    print("Fetching data from custom endpoint...")
    try:
        # Example with a custom endpoint
        custom_data = client._make_request("/metrics/efficiency")
        print(f"Found {len(custom_data)} efficiency metrics")

        # Export to Excel
        file_path = client.export_to_excel(custom_data, "efficiency_metrics", "Efficiency Metrics")
        print(f"Exported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    print("DOGE API Client - Example Usage")
    print("==============================")

    # Run examples
    try:
        example_1_basic_usage()
        example_2_filtered_data()
        example_3_export_all()
        example_4_custom_endpoint()

        print("\nAll examples completed.")
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
