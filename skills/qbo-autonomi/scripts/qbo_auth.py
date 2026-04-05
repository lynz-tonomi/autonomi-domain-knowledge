"""
QBO OAuth 2.0 Token Management for Autonomi

Handles per-tenant credential loading, automatic token refresh,
and secure header generation for all QBO API calls.

Usage:
    from scripts.qbo_auth import QBOAuth

    auth = QBOAuth(tenant_id="tenant_123")
    headers = auth.get_headers()  # Auto-refreshes if needed
    realm_id = auth.realm_id
"""

import json
import os
import time
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import requests

logger = logging.getLogger("qbo_auth")

TOKEN_ENDPOINT = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
REVOKE_ENDPOINT = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"

# Refresh proactively when less than this many seconds remain
REFRESH_BUFFER_SECONDS = 300  # 5 minutes

# Warn when refresh token is within this many days of expiry
REFRESH_TOKEN_WARNING_DAYS = 14


class QBOAuth:
    """Manages OAuth 2.0 tokens for a specific Autonomi tenant's QBO connection."""

    def __init__(self, tenant_id: str, credentials_base: str = "/sandbox/credentials"):
        self.tenant_id = tenant_id
        self.cred_path = Path(credentials_base) / f"tenant_{tenant_id}" / "qbo"

        self._load_config()
        self._load_tokens()

    def _load_config(self):
        """Load app credentials (client_id, client_secret)."""
        config_path = self.cred_path / "oauth_config.json"
        if not config_path.exists():
            raise FileNotFoundError(
                f"QBO OAuth config not found for tenant {self.tenant_id}. "
                f"Expected at {config_path}"
            )
        with open(config_path) as f:
            config = json.load(f)

        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.redirect_uri = config.get("redirect_uri", "")
        self.environment = config.get("environment", "production")

    def _load_tokens(self):
        """Load current token state."""
        token_path = self.cred_path / "token.json"
        if not token_path.exists():
            raise FileNotFoundError(
                f"QBO tokens not found for tenant {self.tenant_id}. "
                f"Tenant must complete OAuth authorization first."
            )
        with open(token_path) as f:
            tokens = json.load(f)

        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.realm_id = tokens["realm_id"]
        self.expires_at = datetime.fromisoformat(tokens["expires_at"])
        self.refresh_expires_at = datetime.fromisoformat(tokens.get(
            "refresh_expires_at",
            (datetime.now(timezone.utc) + timedelta(days=100)).isoformat()
        ))
        self.scopes = tokens.get("scopes", ["com.intuit.quickbooks.accounting"])

    def _save_tokens(self):
        """Persist updated tokens to disk."""
        token_path = self.cred_path / "token.json"
        data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "realm_id": self.realm_id,
            "token_type": "bearer",
            "expires_at": self.expires_at.isoformat(),
            "refresh_expires_at": self.refresh_expires_at.isoformat(),
            "scopes": self.scopes,
        }
        with open(token_path, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(token_path, 0o600)

    def _needs_refresh(self) -> bool:
        """Check if the access token is expired or about to expire."""
        now = datetime.now(timezone.utc)
        return now >= (self.expires_at - timedelta(seconds=REFRESH_BUFFER_SECONDS))

    def _check_refresh_token_health(self):
        """Log a warning if the refresh token is nearing expiry."""
        now = datetime.now(timezone.utc)
        days_remaining = (self.refresh_expires_at - now).days
        if days_remaining <= REFRESH_TOKEN_WARNING_DAYS:
            logger.warning(
                f"QBO refresh token for tenant {self.tenant_id} expires in "
                f"{days_remaining} days. Tenant must re-authorize soon."
            )
        return days_remaining

    def _refresh(self):
        """Exchange the refresh token for a new access token."""
        import base64

        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        response = requests.post(
            TOKEN_ENDPOINT,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            timeout=30,
        )

        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"Token refresh failed for tenant {self.tenant_id}: {error_detail}")
            raise RuntimeError(
                f"QBO token refresh failed (HTTP {response.status_code}). "
                f"Tenant may need to re-authorize."
            )

        data = response.json()
        now = datetime.now(timezone.utc)

        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]  # Always update — old one is invalidated
        self.expires_at = now + timedelta(seconds=data.get("expires_in", 3600))
        self.refresh_expires_at = now + timedelta(
            seconds=data.get("x_refresh_token_expires_in", 8726400)
        )

        self._save_tokens()
        logger.info(f"QBO token refreshed for tenant {self.tenant_id}")

    def get_headers(self) -> dict:
        """
        Return HTTP headers with a valid access token.
        Automatically refreshes if the token is expired or about to expire.
        """
        self._check_refresh_token_health()

        if self._needs_refresh():
            self._refresh()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def check_connection(self) -> dict:
        """Return connection health information."""
        now = datetime.now(timezone.utc)
        token_seconds = max(0, (self.expires_at - now).total_seconds())
        refresh_days = max(0, (self.refresh_expires_at - now).days)

        return {
            "connected": True,
            "tenant_id": self.tenant_id,
            "realm_id": self.realm_id,
            "environment": self.environment,
            "token_expires_in_seconds": int(token_seconds),
            "refresh_expires_in_days": refresh_days,
            "scopes": self.scopes,
            "needs_reauthorization": refresh_days <= 0,
        }

    def revoke(self):
        """Revoke tokens and disconnect the tenant."""
        import base64

        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        requests.post(
            REVOKE_ENDPOINT,
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"token": self.refresh_token},
            timeout=30,
        )
        logger.info(f"QBO tokens revoked for tenant {self.tenant_id}")


def setup_initial_tokens(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    auth_code: str,
    realm_id: str,
    redirect_uri: str,
    environment: str = "production",
    credentials_base: str = "/sandbox/credentials",
):
    """
    Exchange an authorization code for tokens and set up the tenant's
    credential files. Called once during initial tenant onboarding.
    """
    import base64

    cred_path = Path(credentials_base) / f"tenant_{tenant_id}" / "qbo"
    cred_path.mkdir(parents=True, exist_ok=True)

    # Save app config
    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "environment": environment,
    }
    config_path = cred_path / "oauth_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(config_path, 0o600)

    # Exchange auth code for tokens
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        TOKEN_ENDPOINT,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Token exchange failed: {response.text}")

    data = response.json()
    now = datetime.now(timezone.utc)

    tokens = {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "realm_id": realm_id,
        "token_type": "bearer",
        "expires_at": (now + timedelta(seconds=data.get("expires_in", 3600))).isoformat(),
        "refresh_expires_at": (now + timedelta(seconds=data.get("x_refresh_token_expires_in", 8726400))).isoformat(),
        "scopes": ["com.intuit.quickbooks.accounting"],
    }
    token_path = cred_path / "token.json"
    with open(token_path, "w") as f:
        json.dump(tokens, f, indent=2)
    os.chmod(token_path, 0o600)

    logger.info(f"QBO credentials initialized for tenant {tenant_id} (realm: {realm_id})")
    return QBOAuth(tenant_id, credentials_base)
