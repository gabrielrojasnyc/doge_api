#!/usr/bin/env python3
"""
Tests for the DogeApiClient class
"""
import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import requests

from doge_api_client import DogeApiClient


class TestDogeApiClient(unittest.TestCase):
    """Test cases for DogeApiClient class"""

    def setUp(self):
        """Set up test environment"""
        self.client = DogeApiClient(
            base_url="https://test-api.doge.gov",
            api_key="test-api-key",
            api_version="v1",
            timeout=5,
            max_retries=2
        )

    def test_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.base_url, "https://test-api.doge.gov")
        self.assertEqual(self.client.api_key, "test-api-key")
        self.assertEqual(self.client.api_version, "v1")
        self.assertEqual(self.client.timeout, 5)
        self.assertEqual(self.client.max_retries, 2)
        self.assertEqual(self.client.session.headers.get("X-Api-Key"), "test-api-key")

    @patch("requests.Session.get")
    def test_make_request_get(self, mock_get):
        """Test _make_request method with GET"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1, "name": "Test"}]}
        mock_get.return_value = mock_response

        # Make request
        result = self.client._make_request("/test")

        # Verify request
        mock_get.assert_called_once_with(
            "https://test-api.doge.gov/v1/test", 
            params=None,
            timeout=5
        )

        # Verify result
        self.assertEqual(result, [{"id": 1, "name": "Test"}])

    @patch("requests.Session.post")
    def test_make_request_post(self, mock_post):
        """Test _make_request method with POST"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1, "name": "Test"}]}
        mock_post.return_value = mock_response

        # Make request
        result = self.client._make_request(
            "/test", 
            method="POST", 
            data={"test": "data"}
        )

        # Verify request
        mock_post.assert_called_once_with(
            "https://test-api.doge.gov/v1/test", 
            params=None,
            json={"test": "data"},
            timeout=5
        )

        # Verify result
        self.assertEqual(result, [{"id": 1, "name": "Test"}])

    @patch("requests.Session.get")
    def test_make_request_list_response(self, mock_get):
        """Test _make_request method with list response"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Test"}]
        mock_get.return_value = mock_response

        # Make request
        result = self.client._make_request("/test")

        # Verify result
        self.assertEqual(result, [{"id": 1, "name": "Test"}])

    @patch("requests.Session.get")
    def test_make_request_error(self, mock_get):
        """Test _make_request method with error"""
        # Configure mock
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        # Make request and verify exception
        with self.assertRaises(Exception) as context:
            self.client._make_request("/test")

        self.assertIn("API request failed", str(context.exception))

    @patch("doge_api_client.DogeApiClient._make_request")
    def test_get_department_data(self, mock_make_request):
        """Test get_department_data method"""
        # Configure mock
        mock_make_request.return_value = [{"id": 1, "name": "Treasury"}]

        # Call method
        result = self.client.get_department_data(status="active")

        # Verify request
        mock_make_request.assert_called_once_with(
            "/departments", 
            params={"status": "active"}
        )

        # Verify result
        self.assertEqual(result, [{"id": 1, "name": "Treasury"}])

    @patch("os.makedirs")
    @patch("pandas.DataFrame.to_excel")
    def test_export_to_excel(self, mock_to_excel, mock_makedirs):
        """Test export_to_excel method"""
        # Configure mock
        mock_to_excel.return_value = None
        mock_makedirs.return_value = None

        # Prepare test data
        data = [{"id": 1, "name": "Test"}]

        # Mock config values
        with patch("doge_api_client.config") as mock_config:
            mock_config.OUTPUT_DIR = "test_output"
            mock_config.INCLUDE_TIMESTAMP = False
            mock_config.EXCEL_ENGINE = "openpyxl"

            # Call method
            result = self.client.export_to_excel(data, "test_file", "Test Sheet")

        # Verify calls
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)
        mock_to_excel.assert_called_once()

        # Verify result
        self.assertEqual(result, os.path.join("test_output", "test_file.xlsx"))

    @patch("doge_api_client.DogeApiClient.get_department_data")
    @patch("doge_api_client.DogeApiClient.export_to_excel")
    def test_export_all_data(self, mock_export, mock_get_data):
        """Test export_all_data method"""
        # Configure mocks
        mock_get_data.return_value = [{"id": 1, "name": "Test"}]
        mock_export.return_value = "/path/to/file.xlsx"

        # Call method
        result = self.client.export_all_data(status="active")

        # Verify calls
        self.assertEqual(mock_get_data.call_count, 5)
        self.assertEqual(mock_export.call_count, 5)

        # Verify result
        expected = {
            "departments": "/path/to/file.xlsx",
            "employees": "/path/to/file.xlsx",
            "budget": "/path/to/file.xlsx",
            "efficiency_metrics": "/path/to/file.xlsx",
            "projects": "/path/to/file.xlsx"
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()