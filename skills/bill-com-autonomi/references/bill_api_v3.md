# BILL v3 API Reference for Autonomi

## Base URLs

| Environment | API Base URL | Webhook Base URL |
|-------------|-------------|-----------------|
| Sandbox | `https://gateway.stage.bill.com/connect` | `https://gateway.stage.bill.com/connect-events` |
| Production | `https://gateway.prod.bill.com/connect` | `https://gateway.prod.bill.com/connect-events` |

## Authentication

### POST /v3/login

Sign in to get a session ID.

**Headers**: `Content-Type: application/json`, `devKey: {developer_key}`

**Request**:
```json
{
  "userName": "{username}",
  "password": "{password}",
  "orgId": "{organization_id}",
  "rememberMeId": "{optional_mfa_remember_id}",
  "device": "{optional_device_id}"
}
```

**Response**: Returns `sessionId` used in all subsequent requests.

### MFA Flow

Required for payment operations in production.

1. `POST /v3/mfa/challenge` — Initiates MFA challenge (sends code to phone)
2. `POST /v3/mfa/challenge/validate` — Validates the MFA code
3. On subsequent logins, pass `rememberMeId` and `device` to skip MFA

---

## Vendors

### POST /v3/vendors — Create a vendor

**Headers**: `devKey`, `sessionId`, `Content-Type: application/json`

**Request**:
```json
{
  "name": "Happy Music Supplies",
  "accountType": "BUSINESS",
  "email": "info@vendor.org",
  "phone": "9876543210",
  "address": {
    "line1": "123 Main Street",
    "city": "San Jose",
    "stateOrProvince": "CA",
    "zipOrPostalCode": "95131",
    "country": "US"
  },
  "bankAccount": {
    "routingNumber": "322271627",
    "accountNumber": "1234567890",
    "usersName": "Happy Music Supplies"
  }
}
```

**Response**: Returns vendor with `id` (begins with `009`). If `bankAccount` provided, electronic payments enabled; otherwise BILL sends checks.

### GET /v3/vendors — List vendors
### GET /v3/vendors/{vendorId} — Get vendor by ID
### PUT /v3/vendors/{vendorId} — Full update vendor
### PATCH /v3/vendors/{vendorId} — Partial update vendor
### DELETE /v3/vendors/{vendorId} — Archive vendor

---

## Bills

### POST /v3/bills — Create a bill

**Headers**: `devKey`, `sessionId`, `Content-Type: application/json`

**Request**:
```json
{
  "vendorId": "{vendor_id}",
  "dueDate": "2026-12-31",
  "billLineItems": [
    { "amount": 149.00, "description": "USB audio interface" },
    { "amount": 79.99, "description": "Drum foot pedal" }
  ],
  "invoice": {
    "invoiceNumber": "202601",
    "invoiceDate": "2026-12-31"
  }
}
```

**Response**:
```json
{
  "id": "{bill_id}",
  "archived": false,
  "vendorId": "{vendor_id}",
  "amount": 228.99,
  "dueDate": "2026-12-31",
  "invoice": {
    "invoiceNumber": "202601",
    "invoiceDate": "2026-12-31"
  },
  "billLineItems": [
    { "id": "{billLineItem_id01}", "amount": 149.00, "description": "USB audio interface" },
    { "id": "{billLineItem_id02}", "amount": 79.99, "description": "Drum foot pedal" }
  ],
  "paymentStatus": "UNPAID",
  "approvalStatus": "UNASSIGNED",
  "createdTime": "2026-12-30T23:15:23.127+00:00",
  "updatedTime": "2026-12-30T23:15:23.127+00:00"
}
```

**Notes**:
- Bill ID begins with `00n`
- Line item amounts: set `amount` directly, OR set `quantity` and `price` for BILL to calculate
- To include approval info, set `billApprovals=true` query parameter
- International bills include: `fundingAmount` (USD), `exchangeRate`, `amount` (local currency)

### POST /v3/bills/bulk — Create multiple bills

All-or-nothing: if any bill fails, entire request fails and none are created.

**Request**: JSON array of bill objects (same schema as single bill).

**Error codes**:
- `BDC_1205`: No data found for object with given ID
- `BDC_1246`: Rollback due to other failures in bulk transaction

### GET /v3/bills — List bills
### GET /v3/bills/{billId} — Get bill by ID
### PUT /v3/bills/{billId} — Full update bill
### PATCH /v3/bills/{billId} — Partial update bill

---

## Bill Approvals

### POST /v3/bill-approvals — Create approval policy

**Request**:
```json
{
  "policyName": "Bills 1000 to 2000",
  "rules": [
    { "key": "BILL_AMOUNT", "op": "gte", "values": ["1000"] },
    { "key": "BILL_AMOUNT", "op": "lt", "values": ["2000"] }
  ],
  "approvers": ["{user_id01}", "{user_id02}"]
}
```

**Response**:
```json
{
  "id": "{bill_approval_policy_id}",
  "policyName": "Bills 1000 to 2000",
  "status": "ACTIVE",
  "rules": [
    {
      "key": "BILL_AMOUNT",
      "op": "gte",
      "values": [{ "value": "1000", "displayName": "1000" }]
    },
    {
      "key": "BILL_AMOUNT",
      "op": "lt",
      "values": [{ "value": "2000", "displayName": "2000" }]
    }
  ],
  "approvers": {
    "users": [
      { "userId": "{user_id01}", "fullName": "Clark Billenterson" },
      { "userId": "{user_id02}", "fullName": "Final boss" }
    ],
    "groups": []
  }
}
```

**Key details**:
- Policy ID format: `{organization_id}-{unique_id}`
- Rule key: `BILL_AMOUNT`. Operators: `gte`, `lt`
- Approvers in request: simple string array of user IDs (begin with `006`)
- Approvers in response: object with `users` array and `groups` array
- Approval groups must be created via BILL web app (not yet available in API)

### GET /v3/bill-approvals/pending-user-approvals — Get pending bills

**Response**:
```json
{
  "bills": [
    { "billId": "{bill_id}", "vendorId": "{vendor_id}", "amount": 1500.00, "dueDate": "2026-12-31" }
  ]
}
```

**Note**: User must have Administrator, Accountant, or Approver role.

### POST /v3/bill-approvals/actions — Approve or deny

**Request**:
```json
{
  "billId": "{bill_id}",
  "action": "APPROVE"
}
```

- `action`: `APPROVE` or `DENY`
- Returns HTTP 200 on success

### Bill with approvers (when billApprovals=true)

```json
{
  "id": "{bill_id}",
  "approvalStatus": "ASSIGNED",
  "approvers": [
    {
      "userId": "{user_id01}",
      "status": "WAITING",
      "approverOrder": 0,
      "statusChangedTime": "2026-12-30T23:15:23.127+00:00"
    },
    {
      "userId": "{user_id02}",
      "status": "WAITING",
      "approverOrder": 1,
      "statusChangedTime": "2026-12-30T23:15:23.127+00:00"
    }
  ]
}
```

---

## Payments

### POST /v3/payments — Create a payment

**MFA-trusted session required.**

**Request**:
```json
{
  "vendorId": "{vendor_id}",
  "billId": "{bill_id}",
  "processDate": "2026-12-31",
  "fundingAccount": {
    "type": "BANK_ACCOUNT",
    "id": "{org_bank_account_id}"
  },
  "amount": 228.99,
  "processingOptions": {
    "requestPayFaster": false,
    "createBill": false
  }
}
```

**Response**:
```json
{
  "id": "stp01ZZRCUFIQWHP6ldb",
  "vendorId": "{vendor_id}",
  "vendorName": "{vendor_name}",
  "billId": "{bill_id}",
  "billPayments": [
    { "id": "{bill_payment_id}", "billId": "{bill_id}", "amount": 228.99 }
  ],
  "processDate": "2026-12-31",
  "fundingAccount": { "type": "BANK_ACCOUNT", "id": "{org_bank_account_id}" },
  "amount": 228.99,
  "processingOptions": {
    "requestPayFaster": false,
    "createBill": false,
    "requestCheckDeliveryType": "STANDARD"
  },
  "transactionNumber": "EPKZLNTSTYSEUWVALISV",
  "confirmationNumber": "P24123101 - 0411839",
  "status": "SCHEDULED",
  "onlinePayment": true,
  "disbursementType": "ACH",
  "singleStatus": "SCHEDULED",
  "createdBy": "{user_id}",
  "voidInfo": [],
  "cancelRequestSubmitted": false
}
```

**Funding account types**: `BANK_ACCOUNT`, `CARD_ACCOUNT`, `WALLET` (no `id` needed for WALLET)

### POST /v3/payments/bulk — Bulk payment

All-or-nothing. Requires existing bills (`createBill` not supported in bulk).

**Request**:
```json
{
  "processDate": "2026-12-16",
  "fundingAccount": { "type": "BANK_ACCOUNT", "id": "{org_bank_account_id}" },
  "payments": [
    { "billId": "{bill_id01}", "amount": 228.99 },
    { "billId": "{bill_id02}", "amount": 142.00 }
  ]
}
```

**Notes**:
- No negative amounts — use vendor credits on bills first
- `combinePayments: true` on vendor combines up to 35 bills into one payment
- Bill payment IDs begin with `blp`
- Error `BDC_1159`: Cannot overpay a bill

### Pay Faster options

Set `requestPayFaster: true` in `processingOptions`:
- Pay Faster ACH: same-day or next business day
- Pay Faster Check: UPS 1-day, 2-day, 3-day via `requestCheckDeliveryType`
- Instant Payment (RTP): `requestCheckDeliveryType: "RTP_DELIVERY"` — only for Verified National Vendors

### GET /v3/funding-accounts/banks — List bank accounts

---

## Vendor Credits

### POST /v3/vendor-credits — Create vendor credit

**Request**:
```json
{
  "vendorId": "{vendor_id}",
  "referenceNumber": "202602-vendorcredit",
  "creditDate": "2026-12-28",
  "vendorCreditLineItems": [
    { "description": "Classic extreme drum sticks", "amount": 14.99 },
    { "description": "Metal guitar picks (5-pack)", "amount": 50.00 }
  ],
  "description": "Vendor Credit 20261228"
}
```

**Response**: `id` (begins with `vcr`), `amount`, `appliedAmount` (0.00), `status` ("NOT_APPLIED")

### Apply to bill — PATCH /v3/bills/{billId}

```json
{ "vendorCredits": [{ "id": "{vcr_id}", "amount": 10.00 }] }
```

### Apply to payment — POST /v3/payments

Include `vendorCredits` in payment request body. Set `amount` to bill amount minus credit.

### Unapply from bill — PUT /v3/bills/{billId}

Send complete bill details without vendorCredits. **Cannot unapply from a payment.**

### Status lifecycle

`NOT_APPLIED` → `PARTIALLY_APPLIED` → `FULLY_APPLIED`

---

## Webhooks

### Subscription headers by scope

| Scope | Headers |
|-------|---------|
| Org AP & AR | `devKey` + `sessionId` |
| Partner AP & AR | `appKey` + `sessionId` |
| Spend & Expense | `apiToken` |

Required: `X-Idempotent-Key` header (UUID4 format), `notificationUrl`

### Events

| Event | Category |
|-------|----------|
| `vendor.created/updated/archived/restored` | Vendor |
| `autopay.failed` | Vendor Auto-pay |
| `bill.created/updated/archived/restored` | AP Bill |
| `payment.updated/failed` | AP Payment |
| `bank-account.created/updated` | Bank Account |
| `card-account.created/updated` | Card Account |
| `invoice.created/updated/archived/restored` | AR Invoice |
| `risk-verification.updated` | Risk Verification |
| `spend.transaction.updated` | S&E Transaction |
| `spend.reimbursement.created/updated/deleted` | S&E Reimbursement |
| `spend.three-ds-challenge.created` | S&E 3DS |

### Best Practices

- Do not rely on webhooks as only source of truth — validate with GET operations
- Implement idempotent event processing (webhooks may deliver duplicates)
- Use polling as fallback to catch missed events
