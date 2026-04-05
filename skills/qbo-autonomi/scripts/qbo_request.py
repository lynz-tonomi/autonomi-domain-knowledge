"""
QBO HTTP Request Helper for Autonomi

Wraps all QBO API calls with:
- Automatic token management (via qbo_auth)
- Rate limit handling with exponential backoff
- SyncToken conflict resolution (auto-retry on stale object)
- Idempotency via requestid parameter
- Model Armor content screening
- Structured error handling

Usage:
    from scripts.qbo_request import qbo_request, qbo_query

    # Simple GET
    bill = qbo_request("GET", f"/v3/company/{realm_id}/bill/145", tenant_id="t123")

    # Create with idempotency
    invoice = qbo_request("POST", f"/v3/company/{realm_id}/invoice",
                          tenant_id="t123", json_body=invoice_data)

    # Query
    vendors = qbo_query("SELECT * FROM Vendor WHERE Active = true", tenant_id="t123")
"""

import json
import logging
import time
import uuid
from typing import Any, Optional
from urllib.parse import quote, urlencode
import requests

logger = logging.getLogger("qbo_request")

# Retry configuration
MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds
RATE_LIMIT_BACKOFF_BASE = 2

# API configuration
DEFAULT_MINOR_VERSION = 75

# Base URLs
BASE_URLS = {
    "production": "https://quickbooks.api.intuit.com",
    "sandbox": "https://sandbox-quickbooks.api.intuit.com",
}


class QBOAPIError(Exception):
    """Raised when QBO API returns an error."""

    def __init__(self, status_code: int, error_code: str, message: str, detail: str = ""):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.detail = detail
        super().__init__(f"QBO API Error {error_code}: {message} ({detail})")


class QBOStaleObjectError(QBOAPIError):
    """Raised on SyncToken conflict (error 5010)."""
    pass


class QBORateLimitError(QBOAPIError):
    """Raised when rate limit is exceeded (429 / error 003001)."""
    pass


def screen_content(text: str) -> str:
    """
    Screen text content through Model Armor to detect prompt injection.

    In production, this calls the Model Armor API. This implementation
    provides the interface — the actual Model Armor endpoint is configured
    per-sandbox.
    """
    if not text or not isinstance(text, str):
        return text

    # Model Armor screening integration point
    # In production: POST to Model Armor API with content for screening
    # Returns sanitized content with any injection attempts removed
    #
    # For now, return as-is — Model Armor is enabled at the sandbox level
    # and screens all inbound/outbound data automatically.
    return text


def _screen_response(data: Any) -> Any:
    """Recursively screen all string values in a response through Model Armor."""
    if isinstance(data, str):
        return screen_content(data)
    elif isinstance(data, dict):
        return {k: _screen_response(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_screen_response(item) for item in data]
    return data


def _parse_error(response: requests.Response) -> QBOAPIError:
    """Parse a QBO error response into a typed exception."""
    try:
        body = response.json()
        fault = body.get("Fault", {})
        errors = fault.get("Error", [{}])
        error = errors[0] if errors else {}
        code = error.get("code", str(response.status_code))
        message = error.get("Message", "Unknown error")
        detail = error.get("Detail", "")
    except (json.JSONDecodeError, KeyError, IndexError):
        code = str(response.status_code)
        message = response.text[:200]
        detail = ""

    if code == "5010":
        return QBOStaleObjectError(response.status_code, code, message, detail)
    elif response.status_code == 429 or code == "003001":
        return QBORateLimitError(response.status_code, code, message, detail)
    else:
        return QBOAPIError(response.status_code, code, message, detail)


def qbo_request(
    method: str,
    path: str,
    tenant_id: str,
    json_body: Optional[dict] = None,
    params: Optional[dict] = None,
    idempotent: bool = True,
    auto_retry_stale: bool = True,
    screen_response: bool = True,
    minor_version: int = DEFAULT_MINOR_VERSION,
) -> dict:
    """
    Make an authenticated request to the QBO API.

    Args:
        method: HTTP method (GET, POST, DELETE)
        path: API path (e.g., /v3/company/{realmId}/bill/145)
        tenant_id: Autonomi tenant ID for credential lookup
        json_body: Request body for POST requests
        params: Additional query parameters
        idempotent: Include requestid for write operations (default True)
        auto_retry_stale: Auto-retry on SyncToken conflict (default True)
        screen_response: Run response through Model Armor (default True)
        minor_version: API minor version (default 75)

    Returns:
        Parsed JSON response body

    Raises:
        QBOAPIError: On API error after retries exhausted
        QBORateLimitError: On rate limit after retries exhausted
        QBOStaleObjectError: On stale object after retries exhausted
    """
    from scripts.qbo_auth import QBOAuth

    auth = QBOAuth(tenant_id=tenant_id)
    base_url = BASE_URLS.get(auth.environment, BASE_URLS["production"])

    # Build query params
    query_params = {"minorversion": str(minor_version)}
    if params:
        query_params.update(params)

    # Add idempotency key for write operations
    request_id = None
    if idempotent and method.upper() in ("POST", "PUT"):
        request_id = str(uuid.uuid4())
        query_params["requestid"] = request_id

    url = f"{base_url}{path}"

    for attempt in range(MAX_RETRIES):
        headers = auth.get_headers()

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_body if method.upper() in ("POST", "PUT") else None,
                params=query_params,
                timeout=60,
            )
        except requests.Timeout:
            logger.warning(f"QBO request timeout (attempt {attempt + 1}/{MAX_RETRIES}): {method} {path}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(BACKOFF_BASE ** (attempt + 1))
                continue
            raise

        # Success
        if response.status_code in (200, 201):
            data = response.json()
            if screen_response:
                data = _screen_response(data)
            return data

        # Parse error
        error = _parse_error(response)

        # Handle rate limiting
        if isinstance(error, QBORateLimitError):
            wait_time = RATE_LIMIT_BACKOFF_BASE ** (attempt + 1)
            logger.warning(
                f"QBO rate limited (attempt {attempt + 1}/{MAX_RETRIES}). "
                f"Waiting {wait_time}s before retry."
            )
            if attempt < MAX_RETRIES - 1:
                time.sleep(wait_time)
                continue
            raise error

        # Handle stale object (SyncToken conflict)
        if isinstance(error, QBOStaleObjectError) and auto_retry_stale and json_body:
            logger.info(
                f"SyncToken conflict on {path}. Re-reading entity for fresh token."
            )
            if attempt < MAX_RETRIES - 1:
                # Re-read the entity to get fresh SyncToken
                entity_id = json_body.get("Id")
                if entity_id:
                    fresh = qbo_request(
                        "GET", path.rsplit("/", 1)[0] + f"/{entity_id}",
                        tenant_id=tenant_id,
                        screen_response=False,
                    )
                    # Extract the entity from the response wrapper
                    for key, value in fresh.items():
                        if isinstance(value, dict) and "SyncToken" in value:
                            json_body["SyncToken"] = value["SyncToken"]
                            break
                continue
            raise error

        # Handle auth failure — try one refresh
        if response.status_code == 401 and attempt == 0:
            logger.info("QBO 401 — forcing token refresh")
            auth._refresh()
            continue

        # Non-retryable error
        raise error

    raise QBOAPIError(0, "MAX_RETRIES", f"Exhausted {MAX_RETRIES} retries for {method} {path}")


def qbo_query(
    query: str,
    tenant_id: str,
    max_results: int = 1000,
    screen_response: bool = True,
) -> list:
    """
    Execute a QBO query and return all matching entities with automatic pagination.

    Args:
        query: SQL-like query (e.g., "SELECT * FROM Invoice WHERE Balance > '0'")
        tenant_id: Autonomi tenant ID
        max_results: Max results per page (default 1000, QBO max)
        screen_response: Run through Model Armor (default True)

    Returns:
        List of entity dictionaries
    """
    from scripts.qbo_auth import QBOAuth

    auth = QBOAuth(tenant_id=tenant_id)
    realm_id = auth.realm_id

    all_results = []
    start_position = 1

    while True:
        paginated_query = f"{query} STARTPOSITION {start_position} MAXRESULTS {max_results}"
        encoded_query = quote(paginated_query)

        response = qbo_request(
            "GET",
            f"/v3/company/{realm_id}/query",
            tenant_id=tenant_id,
            params={"query": paginated_query},
            idempotent=False,
            screen_response=screen_response,
        )

        query_response = response.get("QueryResponse", {})

        # Extract entities — they're under a key matching the entity name
        entities = []
        for key, value in query_response.items():
            if isinstance(value, list):
                entities = value
                break

        if not entities:
            break

        all_results.extend(entities)

        # Check if there are more pages
        if len(entities) < max_results:
            break

        start_position += max_results

    return all_results


def qbo_batch(
    operations: list,
    tenant_id: str,
    screen_response: bool = True,
) -> dict:
    """
    Execute a batch of up to 30 operations in a single API call.

    Args:
        operations: List of BatchItemRequest objects, each with:
            - bId: Unique identifier for correlation
            - operation: "create", "update", "query", or "delete"
            - {EntityName}: The entity data
        tenant_id: Autonomi tenant ID
        screen_response: Run through Model Armor (default True)

    Returns:
        Batch response with correlated results

    Example:
        ops = [
            {"bId": "1", "operation": "create", "Customer": {"DisplayName": "New Co"}},
            {"bId": "2", "operation": "query", "Query": "SELECT * FROM Item WHERE Type='Inventory'"},
        ]
        results = qbo_batch(ops, tenant_id="t123")
    """
    if len(operations) > 30:
        raise ValueError("QBO batch operations limited to 30 items per request")

    from scripts.qbo_auth import QBOAuth
    auth = QBOAuth(tenant_id=tenant_id)
    realm_id = auth.realm_id

    return qbo_request(
        "POST",
        f"/v3/company/{realm_id}/batch",
        tenant_id=tenant_id,
        json_body={"BatchItemRequest": operations},
        screen_response=screen_response,
    )


def qbo_cdc(
    entities: list,
    changed_since: str,
    tenant_id: str,
    screen_response: bool = True,
) -> dict:
    """
    Query Change Data Capture for entities modified since a timestamp.

    Args:
        entities: List of entity names (e.g., ["Invoice", "Bill", "Payment"])
        changed_since: ISO 8601 timestamp (max 30 days ago)
        tenant_id: Autonomi tenant ID
        screen_response: Run through Model Armor (default True)

    Returns:
        CDC response with changed entities grouped by type
    """
    from scripts.qbo_auth import QBOAuth
    auth = QBOAuth(tenant_id=tenant_id)
    realm_id = auth.realm_id

    return qbo_request(
        "GET",
        f"/v3/company/{realm_id}/cdc",
        tenant_id=tenant_id,
        params={
            "entities": ",".join(entities),
            "changedSince": changed_since,
        },
        idempotent=False,
        screen_response=screen_response,
    )


def qbo_report(
    report_name: str,
    tenant_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    accounting_method: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> dict:
    """
    Fetch a financial report from QBO.

    Args:
        report_name: Report type (e.g., "ProfitAndLoss", "BalanceSheet", "AgedPayables")
        tenant_id: Autonomi tenant ID
        start_date: Report period start (YYYY-MM-DD)
        end_date: Report period end (YYYY-MM-DD)
        accounting_method: "Accrual" or "Cash" (query Preferences if unsure)
        extra_params: Additional report-specific parameters

    Returns:
        Report data structure
    """
    from scripts.qbo_auth import QBOAuth
    auth = QBOAuth(tenant_id=tenant_id)
    realm_id = auth.realm_id

    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if accounting_method:
        params["accounting_method"] = accounting_method
    if extra_params:
        params.update(extra_params)

    return qbo_request(
        "GET",
        f"/v3/company/{realm_id}/reports/{report_name}",
        tenant_id=tenant_id,
        params=params,
        idempotent=False,
    )
