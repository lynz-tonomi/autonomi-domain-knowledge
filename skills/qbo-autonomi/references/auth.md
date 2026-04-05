# QuickBooks Online OAuth 2.0 Authentication Guide

## Table of Contents

1. [Overview](#overview)
2. [Intuit Developer App Setup](#intuit-developer-app-setup)
3. [Authorization Code Flow](#authorization-code-flow)
4. [Token Management](#token-management)
5. [Per-Tenant Credential Isolation](#per-tenant-credential-isolation)
6. [Python Implementation](#python-implementation)
7. [Troubleshooting](#troubleshooting)

---

## Overview

All QBO API access requires OAuth 2.0. There are no API keys, no basic auth, and
no service account patterns like Google Workspace. Each Autonomi tenant must
complete an interactive OAuth consent flow once, after which the system manages
token refresh automatically.

**Key endpoints:**

| Purpose | URL |
|---------|-----|
| Authorization | `https://appcenter.intuit.com/connect/oauth2` |
| Token exchange | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Token revocation | `https://developer.api.intuit.com/v2/oauth2/tokens/revoke` |
| User info | `https://accounts.platform.intuit.com/v1/openid_connect/userinfo` |

**Available scopes:**

| Scope | Access |
|-------|--------|
| `com.intuit.quickbooks.accounting` | Full accounting data (invoices, bills, customers, vendors, reports, etc.) |
| `com.intuit.quickbooks.payment` | Payment processing (charges, refunds) |
| `openid` | OpenID Connect user identity |
| `profile` | User profile information |
| `email` | User email address |
| `phone` | User phone number |
| `address` | User physical address |

For Autonomi, always request at minimum `com.intuit.quickbooks.accounting`. Add
`com.intuit.quickbooks.payment` if the tenant uses QBO Payments for processing
customer credit card / ACH payments.

---

## Intuit Developer App Setup

1. Go to `https://developer.intuit.com` and sign in
2. Create a new app → select "QuickBooks Online and Payments"
3. Under the app's Keys & credentials tab:
   - Note the **Client ID** and **Client Secret** (these are per-environment)
   - Sandbox and Production have separate key pairs
4. Configure **Redirect URIs** — these must exactly match what your auth flow sends
5. Under Webhooks tab (if using webhooks):
   - Add your webhook endpoint URL
   - Note the **Verifier Token** for HMAC-SHA256 signature validation

**Sandbox vs Production:**
- Sandbox uses production OAuth endpoints (same auth URLs) but sandbox API base URL
- Sandbox has its own company data — changes don't affect production
- Sandbox has lower email limits (40/day vs production limits)

---

## Authorization Code Flow

### Step 1: Build the Authorization URL

```
https://appcenter.intuit.com/connect/oauth2
  ?client_id={CLIENT_ID}
  &response_type=code
  &scope=com.intuit.quickbooks.accounting
  &redirect_uri={REDIRECT_URI}
  &state={CSRF_TOKEN}
```

- `state`: Generate a random string for CSRF protection. Verify it matches on callback.
- `redirect_uri`: Must exactly match one of the URIs configured in the Intuit Developer portal.
- Multiple scopes separated by spaces (URL-encoded as `%20`).

### Step 2: User Authorizes

The user is redirected to Intuit's login page, selects their QBO company, and
approves the requested permissions. Intuit redirects back to your `redirect_uri`:

```
{REDIRECT_URI}?code={AUTH_CODE}&state={CSRF_TOKEN}&realmId={REALM_ID}
```

**CRITICAL:** The `realmId` parameter in this redirect is the only time QBO tells
you the Company ID. There is no API endpoint to look it up later. Store it
immediately alongside the tenant's credentials.

### Step 3: Exchange Code for Tokens

POST to the token endpoint with Basic auth (Client ID:Client Secret as base64):

```http
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {base64(client_id:client_secret)}

grant_type=authorization_code&code={AUTH_CODE}&redirect_uri={REDIRECT_URI}
```

Response:
```json
{
  "access_token": "eyJlbmMi...",
  "refresh_token": "AB11234...",
  "token_type": "bearer",
  "expires_in": 3600,
  "x_refresh_token_expires_in": 8726400,
  "id_token": "eyJraWQi..."
}
```

- `access_token`: Valid for ~1 hour (3600 seconds)
- `refresh_token`: Valid for ~100 days (8,726,400 seconds)
- `id_token`: Present if `openid` scope was requested

### Step 4: Store Credentials

Save to the tenant's credential path:
```json
// /sandbox/credentials/tenant_{TENANT_ID}/qbo/token.json
{
  "access_token": "eyJlbmMi...",
  "refresh_token": "AB11234...",
  "realm_id": "1234567890",
  "token_type": "bearer",
  "expires_at": "2025-03-21T15:30:00Z",
  "refresh_expires_at": "2025-06-19T14:30:00Z",
  "scopes": ["com.intuit.quickbooks.accounting"]
}
```

---

## Token Management

### Automatic Refresh

Access tokens expire hourly. The `scripts/qbo_auth.py` helper checks token expiry
before every API call and refreshes proactively (when less than 5 minutes remain)
rather than waiting for a 401 error.

**Refresh request:**
```http
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {base64(client_id:client_secret)}

grant_type=refresh_token&refresh_token={REFRESH_TOKEN}
```

The response includes both a new `access_token` and a new `refresh_token`. Always
store the new refresh token — the old one is invalidated.

### Refresh Token Expiry

Refresh tokens last ~100 days. If a tenant's integration goes unused for over 100
days, re-authorization is required. The `scripts/qbo_auth.py` helper logs a warning
when the refresh token is within 14 days of expiry so the tenant can be notified.

### Token Revocation

To disconnect a tenant:
```http
POST https://developer.api.intuit.com/v2/oauth2/tokens/revoke
Content-Type: application/json
Authorization: Basic {base64(client_id:client_secret)}

{"token": "{REFRESH_TOKEN}"}
```

---

## Per-Tenant Credential Isolation

Each Autonomi tenant's QBO credentials are stored in an isolated sandbox path:

```
/sandbox/credentials/tenant_{TENANT_ID}/qbo/
├── oauth_config.json      # App credentials (client_id, client_secret, redirect_uri)
├── token.json             # Current tokens + realm_id + expiry timestamps
└── webhook_verifier.txt   # Verifier token for webhook HMAC validation
```

**Isolation enforcement:**
- Filesystem permissions: each agent sandbox can only access its own tenant's directory
- Credentials encrypted at rest (AES-256-GCM) via OS keyring
- Token files are chmod 600 (owner read/write only)
- Network policy: only QBO-related hostnames are allowed outbound
- No cross-tenant credential access is possible from within a sandbox

**oauth_config.json structure:**
```json
{
  "client_id": "AB...",
  "client_secret": "...",
  "redirect_uri": "https://autonomi.example.com/auth/qbo/callback",
  "environment": "production"
}
```

---

## Python Implementation

The `scripts/qbo_auth.py` module provides the `QBOAuth` class:

```python
from scripts.qbo_auth import QBOAuth

# Initialize for a specific tenant
auth = QBOAuth(tenant_id="tenant_123")

# Get valid headers (auto-refreshes if needed)
headers = auth.get_headers()
# Returns: {"Authorization": "Bearer eyJ...", "Accept": "application/json", "Content-Type": "application/json"}

# Get realm_id for URL construction
realm_id = auth.realm_id

# Check connection health
status = auth.check_connection()
# Returns: {"connected": True, "token_expires_in_seconds": 2847, "refresh_expires_in_days": 89}
```

The `intuit-oauth` Python package can also be used directly if needed:

```python
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

auth_client = AuthClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    environment='production'  # or 'sandbox'
)

# Generate authorization URL
auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

# Exchange code for tokens
auth_client.get_bearer_token(auth_code, realm_id=realm_id)

# Refresh
auth_client.refresh(refresh_token=refresh_token)
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 Unauthorized | Expired access token | Auto-refresh should handle this; if not, check refresh token expiry |
| 403 Forbidden | Missing scope or subscription | Verify scopes in token; check tenant's QBO subscription tier |
| `invalid_grant` on refresh | Refresh token expired or revoked | Tenant must re-authorize (new OAuth flow) |
| `redirect_uri_mismatch` | Redirect URI doesn't match app config | Exact match required including trailing slashes |
| No realmId in callback | Scope missing `com.intuit.quickbooks.accounting` | Add the accounting scope to authorization request |
| Tokens work in sandbox but not production | Using sandbox keys for production | Ensure correct environment keys are configured |
