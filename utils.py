#!/usr/bin/env python3
"""
Utility functions for the DOGE API
"""

# Standard library imports
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Third-party imports
import pandas as pd

# Local imports
import config

logger = logging.getLogger("doge_utils")


def process_data(data: List[Dict], transformations: Optional[Dict] = None) -> pd.DataFrame:
    """
    Process and transform API data

    Args:
        data: List of dictionaries from the API
        transformations: Optional dictionary of column transformations

    Returns:
        Processed DataFrame
    """
    if not data:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Apply transformations if provided
    if transformations:
        for column, transform_func in transformations.items():
            if column in df.columns:
                df[column] = df[column].apply(transform_func)

    return df


def save_to_excel(
    df: pd.DataFrame,
    filename: str,
    sheet_name: str = "Data",
    output_dir: Optional[str] = None,
    include_timestamp: Optional[bool] = None,
) -> str:
    """
    Save DataFrame to Excel file

    Args:
        df: DataFrame to save
        filename: Base filename
        sheet_name: Excel sheet name
        output_dir: Optional override for output directory
        include_timestamp: Optional override for including timestamp

    Returns:
        Path to saved file
    """
    if df.empty:
        logger.warning(f"No data to save for {filename}")
        return ""

    # Use configuration with optional overrides
    output_dir = output_dir or config.OUTPUT_DIR
    include_timestamp = (
        include_timestamp if include_timestamp is not None else config.INCLUDE_TIMESTAMP
    )

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Add timestamp if configured
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.xlsx"
    else:
        full_filename = f"{filename}.xlsx"

    file_path = os.path.join(output_dir, full_filename)

    # Save to Excel
    try:
        df.to_excel(file_path, sheet_name=sheet_name, index=False, engine=config.EXCEL_ENGINE)
        logger.info(f"Data exported to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to export data to Excel: {str(e)}")
        return ""


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    """
    Set up logging configuration

    Args:
        log_level: Logging level (default from config)
        log_file: Log file path (default to None)
        log_format: Log format string (default from config)
    """
    # Use configuration with optional overrides
    level = getattr(logging, log_level or config.LOG_LEVEL)
    format_str = log_format or config.LOG_FORMAT

    # Set up handlers
    handlers = [logging.StreamHandler()]

    # Add file handler if specified
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    # Configure logging
    logging.basicConfig(level=level, format=format_str, handlers=handlers)

    # Log configuration
    logger.debug(f"Logging configured with level {logging.getLevelName(level)}")
