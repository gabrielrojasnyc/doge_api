#!/usr/bin/env python3
"""
DOGE API Client
--------------
Client for interacting with the DOGE (Department of Government Efficiency) API
"""

# Standard library imports
import logging
import time
from typing import Dict, List, Optional, Any

# Third-party imports
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Local imports
import config
from utils import process_data, save_to_excel

logger = logging.getLogger("doge_api_client")


class DogeApiClient:
    """
    Client for interacting with the DOGE (Department of Government Efficiency) API
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
    ):
        """
        Initialize the DOGE API client

        Args:
            base_url: Base URL for API requests (default from config)
            api_key: API key for authentication (default from config)
            api_version: API version (default from config)
            timeout: Request timeout in seconds (default from config)
            max_retries: Maximum number of retry attempts (default from config)
        """
        self.base_url = base_url or config.API_BASE_URL
        self.api_key = api_key or config.API_KEY
        self.api_version = api_version or config.API_VERSION
        self.timeout = timeout or config.REQUEST_TIMEOUT
        self.max_retries = max_retries or config.REQUEST_MAX_RETRIES

        # Create session with retry configuration
        self.session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Add API key to session headers if provided
        if self.api_key:
            self.session.headers.update({"X-Api-Key": self.api_key})

        logger.debug(f"Initialized DOGE API client with base URL: {self.base_url}")

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        paginate: bool = True,
    ) -> List[Dict]:
        """
        Make a request to the DOGE API

        Args:
            endpoint: API endpoint (e.g., "/departments")
            method: HTTP method (default: "GET")
            params: Query parameters
            data: Request body for POST requests
            paginate: Whether to automatically fetch all pages (default: True)

        Returns:
            List of dictionaries containing API response data

        Raises:
            Exception: If the API request fails
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        # Construct full URL (no version prefix needed as per API Structure Notes)
        url = f"{self.base_url}{endpoint}"

        # Initialize params dict if None
        if params is None:
            params = {}

        # Copy params to avoid modifying the original
        params_copy = params.copy()

        # Default pagination parameters if not specified
        if paginate and "per_page" not in params_copy:
            params_copy["per_page"] = config.BATCH_SIZE

        # For pagination tracking
        current_page = 1
        total_pages = 1
        all_results = []

        logger.debug(f"Making {method} request to {url}")

        while current_page <= total_pages:
            # Update page parameter for pagination
            if paginate:
                params_copy["page"] = current_page
                
            try:
                start_time = time.time()

                if method.upper() == "GET":
                    response = self.session.get(url, params=params_copy, timeout=self.timeout)
                elif method.upper() == "POST":
                    response = self.session.post(url, params=params_copy, json=data, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                elapsed = time.time() - start_time
                logger.debug(f"Request completed in {elapsed:.2f}s with status {response.status_code}")

                # Raise exception for HTTP errors
                response.raise_for_status()

                # Parse JSON response
                json_data = response.json()

                # Process pagination metadata if available
                if "meta" in json_data and paginate:
                    meta = json_data.get("meta", {})
                    if "pages" in meta:
                        total_pages = meta["pages"]
                    elif "total_pages" in meta:
                        total_pages = meta["total_pages"]
                    
                    logger.debug(f"Pagination: Page {current_page} of {total_pages}")
                
                # Extract data from response based on DOGE API format
                page_results = []
                
                if "result" in json_data:
                    result = json_data["result"]

                    # Handle nested structure in DOGE API
                    if isinstance(result, dict):
                        # Extract data type from endpoint (e.g., "grants" from "/savings/grants")
                        endpoint_parts = endpoint.strip("/").split("/")
                        if len(endpoint_parts) >= 2:
                            data_type = endpoint_parts[-1]
                            if data_type in result and isinstance(result[data_type], list):
                                page_results = result[data_type]

                        # If we can't extract by endpoint name, find the first list value
                        if not page_results:
                            for key, value in result.items():
                                if isinstance(value, list):
                                    logger.debug(f"Returning list from result[{key}]")
                                    page_results = value
                                    break

                    # Direct list in result field
                    elif isinstance(result, list):
                        page_results = result

                # Legacy format support
                elif "data" in json_data and isinstance(json_data["data"], list):
                    page_results = json_data["data"]
                elif isinstance(json_data, list):
                    page_results = json_data
                
                # Add results from this page to our collection
                all_results.extend(page_results)
                
                # If no items or no pagination, exit the loop
                if not paginate or not page_results:
                    break
                
                # Move to next page
                current_page += 1
                
            except requests.exceptions.ConnectionError as e:
                error_msg = f"Connection error while accessing {url}: {str(e)}"
                logger.error(error_msg)
                raise ConnectionError(error_msg)
            except requests.exceptions.Timeout as e:
                error_msg = f"Request timed out after {self.timeout}s while accessing {url}: {str(e)}"
                logger.error(error_msg)
                raise TimeoutError(error_msg)
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if hasattr(e, "response") else "unknown"
                error_msg = f"HTTP error {status_code} while accessing {url}: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            except requests.exceptions.RequestException as e:
                error_msg = f"API request failed for {url}: {str(e)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
        
        if paginate and total_pages > 1:
            logger.info(f"Retrieved {len(all_results)} records across {total_pages} pages")
        
        return all_results

    def get_department_data(self, **filters: Any) -> List[Dict]:
        """
        Get department data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of department dictionaries
        """
        return self._make_request("/departments", params=filters)

    def get_employee_data(self, **filters: Any) -> List[Dict]:
        """
        Get employee data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of employee dictionaries
        """
        return self._make_request("/employees", params=filters)

    def get_budget_data(self, **filters: Any) -> List[Dict]:
        """
        Get budget data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of budget dictionaries
        """
        return self._make_request("/budget", params=filters)

    def get_efficiency_metrics(self, **filters: Any) -> List[Dict]:
        """
        Get efficiency metrics from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of metric dictionaries
        """
        return self._make_request("/metrics/efficiency", params=filters)

    def get_projects_data(self, **filters: Any) -> List[Dict]:
        """
        Get projects data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of project dictionaries
        """
        return self._make_request("/projects", params=filters)

    def get_grants_data(self, **filters: Any) -> List[Dict]:
        """
        Get savings grants data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of grants dictionaries
        """
        return self._make_request("/savings/grants", params=filters)

    def get_contracts_data(self, **filters: Any) -> List[Dict]:
        """
        Get savings contracts data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of contracts dictionaries
        """
        return self._make_request("/savings/contracts", params=filters)

    def get_leases_data(self, **filters: Any) -> List[Dict]:
        """
        Get savings leases data from the API

        Args:
            **filters: Optional filters to apply

        Returns:
            List of leases dictionaries
        """
        return self._make_request("/savings/leases", params=filters)

    def export_to_excel(self, data: List[Dict], filename: str, sheet_name: str = "Data") -> str:
        """
        Export data to Excel file

        Args:
            data: List of dictionaries to export
            filename: Base filename (without extension)
            sheet_name: Excel sheet name

        Returns:
            Path to the saved Excel file
        """
        if not data:
            logger.warning(f"No data to export for {filename}")
            return ""

        # Create DataFrame
        df = process_data(data)

        # Save to Excel using utility function
        return save_to_excel(df, filename, sheet_name)

    def export_all_data(self, **filters: Any) -> Dict[str, str]:
        """
        Export all available data types to Excel

        Args:
            **filters: Optional filters to apply

        Returns:
            Dictionary mapping data types to file paths
        """
        results = {}

        # Export current API data types

        # Export grants
        try:
            grants = self.get_grants_data(**filters)
            results["grants"] = self.export_to_excel(grants, "grants_savings", "Grant Savings")
        except Exception as e:
            logger.error(f"Failed to export grants: {str(e)}")
            results["grants"] = ""

        # Export contracts
        try:
            contracts = self.get_contracts_data(**filters)
            results["contracts"] = self.export_to_excel(
                contracts, "contracts_savings", "Contract Savings"
            )
        except Exception as e:
            logger.error(f"Failed to export contracts: {str(e)}")
            results["contracts"] = ""

        # Export leases
        try:
            leases = self.get_leases_data(**filters)
            results["leases"] = self.export_to_excel(leases, "leases_savings", "Lease Savings")
        except Exception as e:
            logger.error(f"Failed to export leases: {str(e)}")
            results["leases"] = ""

        # Export legacy data types (may fail with 404)

        # Export departments
        try:
            departments = self.get_department_data(**filters)
            results["departments"] = self.export_to_excel(departments, "departments", "Departments")
        except Exception as e:
            logger.warning(f"Failed to export departments (legacy endpoint): {str(e)}")
            results["departments"] = ""

        # Export employees
        try:
            employees = self.get_employee_data(**filters)
            results["employees"] = self.export_to_excel(employees, "employees", "Employees")
        except Exception as e:
            logger.warning(f"Failed to export employees (legacy endpoint): {str(e)}")
            results["employees"] = ""

        # Export budget
        try:
            budget = self.get_budget_data(**filters)
            results["budget"] = self.export_to_excel(budget, "budget", "Budget")
        except Exception as e:
            logger.warning(f"Failed to export budget (legacy endpoint): {str(e)}")
            results["budget"] = ""

        # Export efficiency metrics
        try:
            metrics = self.get_efficiency_metrics(**filters)
            results["efficiency_metrics"] = self.export_to_excel(
                metrics, "efficiency_metrics", "Efficiency Metrics"
            )
        except Exception as e:
            logger.warning(f"Failed to export efficiency metrics (legacy endpoint): {str(e)}")
            results["efficiency_metrics"] = ""

        # Export projects
        try:
            projects = self.get_projects_data(**filters)
            results["projects"] = self.export_to_excel(projects, "projects", "Projects")
        except Exception as e:
            logger.warning(f"Failed to export projects (legacy endpoint): {str(e)}")
            results["projects"] = ""

        return results