#!/usr/bin/env python3
"""
Updated example script for DOGE API using the new endpoints
"""

import logging
from typing import Dict, List, Any, Optional

import pandas as pd

from doge_api_client import DogeApiClient
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main example function"""
    print("\nDOGE API Client - New Example\n" + "=" * 30 + "\n")

    # Initialize client
    client = DogeApiClient(base_url=config.API_BASE_URL, api_key=config.API_KEY)

    # Example 1: Fetch grant savings data
    print("\n=== Example 1: Grant Savings ===")
    try:
        print("Fetching grant savings data with highest savings first...")
        grants = client._make_request(
            "/savings/grants",
            params={"sort_by": "savings", "sort_order": "desc", "page": 1, "per_page": 5},
        )

        if grants:
            print(f"Retrieved {len(grants)} grants")
            print("\nTop 5 grants by savings:")
            for i, grant in enumerate(grants[:5], 1):
                print(
                    f"{i}. {grant.get('recipient', 'Unknown')}: ${grant.get('savings', 0):,.0f} savings"
                )

            # Export to Excel
            file_path = client.export_to_excel(grants, "top_grants", "Top Grants by Savings")
            if file_path:
                print(f"\nExported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Example 2: Fetch contract savings with filter
    print("\n=== Example 2: Contract Savings ===")
    try:
        print("Fetching contract savings data sorted by value...")
        contracts = client._make_request(
            "/savings/contracts",
            params={"sort_by": "value", "sort_order": "desc", "page": 1, "per_page": 5},
        )

        if contracts:
            print(f"Retrieved {len(contracts)} contracts")
            print("\nTop 5 contracts by value:")
            for i, contract in enumerate(contracts[:5], 1):
                print(
                    f"{i}. {contract.get('company', 'Unknown')}: ${contract.get('value', 0):,.0f} value"
                )

            # Export to Excel
            file_path = client.export_to_excel(contracts, "top_contracts", "Top Contracts by Value")
            if file_path:
                print(f"\nExported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Example 3: Fetch lease savings
    print("\n=== Example 3: Lease Savings ===")
    try:
        print("Fetching lease savings data...")
        leases = client._make_request(
            "/savings/leases",
            params={"sort_by": "savings", "sort_order": "desc", "page": 1, "per_page": 5},
        )

        if leases:
            print(f"Retrieved {len(leases)} leases")
            print("\nTop 5 leases by savings:")
            for i, lease in enumerate(leases[:5], 1):
                location = lease.get("location", "Unknown")
                savings = lease.get("savings", 0)
                sq_ft = lease.get("sq_ft", 0)
                print(f"{i}. {location}: ${savings:,.0f} savings ({sq_ft:,} sq ft)")

            # Export to Excel
            file_path = client.export_to_excel(leases, "top_leases", "Top Leases by Savings")
            if file_path:
                print(f"\nExported to: {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Example 4: Export all data types
    print("\n=== Example 4: Export All Savings Data ===")
    try:
        print("Exporting all savings data types...")

        # Export grants
        grants_file = client.export_to_excel(
            client._make_request("/savings/grants", params={"per_page": 10}),
            "grants_savings",
            "Grant Savings",
        )

        # Export contracts
        contracts_file = client.export_to_excel(
            client._make_request("/savings/contracts", params={"per_page": 10}),
            "contracts_savings",
            "Contract Savings",
        )

        # Export leases
        leases_file = client.export_to_excel(
            client._make_request("/savings/leases", params={"per_page": 10}),
            "leases_savings",
            "Lease Savings",
        )

        # Print summary
        print("\nExport Summary:")
        if grants_file:
            print(f"✅ grants: {grants_file}")
        else:
            print("❌ grants: Failed to export")

        if contracts_file:
            print(f"✅ contracts: {contracts_file}")
        else:
            print("❌ contracts: Failed to export")

        if leases_file:
            print(f"✅ leases: {leases_file}")
        else:
            print("❌ leases: Failed to export")

    except Exception as e:
        print(f"Error: {str(e)}")

    print("\nAll examples completed.")


if __name__ == "__main__":
    main()
