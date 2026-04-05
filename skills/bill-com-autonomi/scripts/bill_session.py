#!/usr/bin/env python3
"""
BILL.com Session Management for Autonomi Agents.

Handles authentication, session caching, and auto-refresh for the BILL.com API.
Supports both v3 (primary) and v2 (legacy fallback) API calls.

Base URLs (from official BILL.com documentation):
  Sandbox API:      https://gateway.stage.bill.com/connect
  Production API:   https://gateway.prod.bill.com/connect
  Sandbox Webhooks: https://gateway.stage.bill.com/connect-events
  Production Webhooks: https://gateway.prod.bill.com/connect-events

  v2 Sandbox: https://api-sandbox.bill.com/api/v2
  v2 Production: https://api.bill.com/api/v2
"""

import os
import json
import time
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger("autonomi.bill_session")

# ---------------------------------------------------------------------------
# Base URL configuration
# ---------------------------------------------------------------------------
V3_BASE_URLS = {
    "sandbox": "https://gateway.stage.bill.com/connect",
    "production": "https://gateway.prod.bill.com/connect",
}
V2_BASE_URLS = {
    "sandbox": "https://api-sandbox.bill.com/api/v2",
    "production": "https://api.bill.com/api/v2",
}
WEBHOOK_BASE_URLS = {
    "sandbox": "https://gateway.stage.bill.com/connect-events",
    "production": "https://gateway.prod.bill.com/connect-events",
}

# Retry configuration
RETRY_CODES = {401, 429, 500, 503}
MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds, exponential


class BillSession:
    """Manages BILL.com API sessions for a single Autonomi tenant.

    Loads credentials from NemoClaw-managed env or config file,
    authenticates via POST /v3/login, caches the sessionId,
    and auto-refreshes on 401.
    """

    def __init__(
        self,
        environment: str = "sandbox",
        credentials: Optional[Dict[str, str]] = None,
        cache_path: Optional[str] = None,
    ):
        self.environment = environment
        self.v3_base = V3_BASE_URLS[environment]
        self.v2_base = V2_BASE_URLS[environment]
        self.webhook_base = WEBHOOK_BASE_URLS[environment]

        # Load credentials from arg, env, or NemoClaw config
        self.credentials = credentials or self._load_credentials()
        self.dev_key = self.credentials["developer_key"]
        self.session_id: Optional[str] = None
        self.session_expiry: float = 0

        # Persistent session cache
        self.cache_path = Path(cache_path or "/tmp/bill_session_cache.json")
        self._load_cached_session()

    # ------------------------------------------------------------------
    # Credential loading
    # ------------------------------------------------------------------
    def _load_credentials(self) -> Dict[str, str]:
        """Load BILL.com credentials from environment or NemoClaw vault."""
        creds = {
            "username": os.environ.get("BILL_USERNAME", ""),
            "password": os.environ.get("BILL_PASSWORD", ""),
            "developer_key": os.environ.get("BILL_DEV_KEY", ""),
            "organization_id": os.environ.get("BILL_ORG_ID", ""),
        }
        # NemoClaw config fallback
        nc_path = Path(os.environ.get(
            "NEMOCLAW_BILL_CREDS",
            "/opt/nemoclaw/secrets/bill_credentials.json"
        ))
        if not all(creds.values()) and nc_path.exists():
            with open(nc_path) as f:
                nc = json.load(f)
            creds.update({k: v for k, v in nc.items() if v})

        missing = [k for k, v in creds.items() if not v]
        if missing:
            raise ValueError(f"Missing BILL.com credentials: {missing}")
        return creds

    # ------------------------------------------------------------------
    # Session caching
    # ------------------------------------------------------------------
    def _load_cached_session(self):
        if self.cache_path.exists():
            try:
                data = json.loads(self.cache_path.read_text())
                if data.get("environment") == self.environment and data.get("expiry", 0) > time.time():
                    self.session_id = data["session_id"]
                    self.session_expiry = data["expiry"]
                    logger.info("Loaded cached BILL session")
            except (json.JSONDecodeError, KeyError):
                pass

    def _save_session_cache(self):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps({
            "session_id": self.session_id,
            "environment": self.environment,
            "expiry": self.session_expiry,
        }))

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def authenticate(self) -> str:
        """Authenticate with POST /v3/login and return sessionId."""
        url = f"{self.v3_base}/v3/login"
        headers = {
            "Content-Type": "application/json",
            "devKey": self.dev_key,
        }
        payload = {
            "userName": self.credentials["username"],
            "password": self.credentials["password"],
            "orgId": self.credentials["organization_id"],
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        self.session_id = data["sessionId"]
        # Sessions typically last ~35 minutes; refresh proactively at 30 min
        self.session_expiry = time.time() + 1800
        self._save_session_cache()
        logger.info("Authenticated with BILL.com v3 API")
        return self.session_id

    def ensure_session(self) -> str:
        """Return a valid sessionId, re-authenticating if needed."""
        if not self.session_id or time.time() >= self.session_expiry:
            self.authenticate()
        return self.session_id

    # ------------------------------------------------------------------
    # API call helpers
    # ------------------------------------------------------------------
    def _v3_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "devKey": self.dev_key,
            "sessionId": self.ensure_session(),
        }

    def api_call_v3(
        self,
        method: str,
        path: str,
        payload: Optional[Any] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated v3 API call with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: API path (e.g., '/v3/bills')
            payload: JSON-serializable body for POST/PUT/PATCH
            params: Query parameters
        """
        url = f"{self.v3_base}{path}"

        for attempt in range(MAX_RETRIES + 1):
            headers = self._v3_headers()
            try:
                resp = requests.request(
                    method, url,
                    json=payload if method != "GET" else None,
                    params=params,
                    headers=headers,
                    timeout=60,
                )

                if resp.status_code not in RETRY_CODES:
                    resp.raise_for_status()
                    return resp.json() if resp.content else {}

                # Handle retryable errors
                if resp.status_code == 401:
                    logger.warning("Session expired, re-authenticating...")
                    self.session_id = None
                    self.authenticate()
                    continue

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", BACKOFF_BASE ** (attempt + 1)))
                    logger.warning(f"Rate limited, waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue

                # 500/503
                wait = BACKOFF_BASE ** (attempt + 1)
                logger.warning(f"Server error {resp.status_code}, retrying in {wait}s...")
                time.sleep(wait)

            except requests.exceptions.Timeout:
                if attempt == MAX_RETRIES:
                    raise
                wait = BACKOFF_BASE ** (attempt + 1)
                logger.warning(f"Timeout, retrying in {wait}s...")
                time.sleep(wait)

        # If we exhausted retries, raise the last error
        resp.raise_for_status()
        return {}

    def api_call_v2(
        self,
        operation: str,
        payload: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated v2 API call (legacy, form-encoded).

        Args:
            operation: v2 operation path (e.g., 'Crud/Read/Bill')
            payload: Form data as dict (will be JSON-encoded in 'data' field)
        """
        url = f"{self.v2_base}/{operation}.json"
        form_data = {
            "devKey": self.dev_key,
            "sessionId": self.ensure_session(),
        }
        if payload:
            form_data["data"] = json.dumps(payload)

        for attempt in range(MAX_RETRIES + 1):
            resp = requests.post(url, data=form_data, timeout=60)

            if resp.status_code == 401:
                self.session_id = None
                self.authenticate()
                form_data["sessionId"] = self.session_id
                continue

            if resp.status_code in RETRY_CODES:
                wait = BACKOFF_BASE ** (attempt + 1)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            result = resp.json()

            if result.get("response_status") == 1:
                return result.get("response_data", result)
            else:
                error_list = result.get("response_data", {}).get("error_list", [])
                raise RuntimeError(f"BILL v2 error: {error_list}")

        resp.raise_for_status()
        return {}
