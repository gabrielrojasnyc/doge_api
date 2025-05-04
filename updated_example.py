#!/usr/bin/env python3
"""
Updated example usage for the DOGE API client
with the correct endpoints and parameters
"""

import os
import logging
from typing import Dict, Optional, List, Any

import pandas as pd

from doge_api_client import DogeApiClient
import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_savings_data(data_type: str, sort_by: str = "savings", sort_order: str = "desc"):
    """Export savings data for a specific data type"""

    if data_type not in ["grants", "contracts", "leases"]:
        logger.error(f"Invalid data type: {data_type}")
        return

    # Initialize API client
    client = DogeApiClient(base_url=config.API_BASE_URL, api_key=config.API_KEY)

    # Set request parameters
    params = {"sort_by": sort_by, "sort_order": sort_order, "page": 1, "per_page": 100}

    # Get endpoint from config
    endpoint = config.DATA_TYPES[data_type]["endpoint"]

    try:
        # Fetch data from API
        logger.info(f"Fetching {data_type} data...")
        response = client.session.get(
            f"{client.base_url}{endpoint}",
            params=params,
            headers={"X-Api-Key": client.api_key} if client.api_key else {},
        )

        # Debug response
        logger.info(f"Status code: {response.status_code}")

        # Parse JSON
        json_data = response.json()
        logger.info(f"Response keys: {list(json_data.keys())}")

        # Extract result data - handles the nested structure
        if "result" in json_data:
            if isinstance(json_data["result"], dict) and data_type in json_data["result"]:
                # The actual data is inside a nested dictionary with the data type as key
                data = json_data["result"][data_type]
                logger.info(f"Found {len(data)} items in result[{data_type}]")
            elif isinstance(json_data["result"], list):
                data = json_data["result"]
                logger.info(f"Found {len(data)} items in result list")
            else:
                logger.warning(f"Unexpected result structure")
                logger.info(
                    f"Result keys: {list(json_data['result'].keys()) if isinstance(json_data['result'], dict) else 'Not a dict'}"
                )
                return
        else:
            logger.warning(f"No result field found in response")
            logger.info(f"Response keys: {list(json_data.keys())}")
            return

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Export to Excel
        export_path = client.export_to_excel(
            data, f"{data_type}_savings", config.DATA_TYPES[data_type]["display_name"]
        )

        if export_path:
            logger.info(f"Exported {data_type} data to {export_path}")

    except Exception as e:
        logger.error(f"Error processing {data_type}: {str(e)}")


def export_all_savings():
    """Export all savings data types"""
    export_savings_data("grants")
    export_savings_data("contracts")
    export_savings_data("leases")


if __name__ == "__main__":
    logger.info("Running updated DOGE API example")
    export_all_savings()
    logger.info("Done")
