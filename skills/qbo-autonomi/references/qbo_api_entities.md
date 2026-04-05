# QuickBooks Online API Entity Reference

## Table of Contents

1. [Accounts Payable Entities](#accounts-payable-entities)
   - [Bill](#bill)
   - [BillPayment](#billpayment)
   - [VendorCredit](#vendorcredit)
   - [Vendor](#vendor)
2. [Accounts Receivable Entities](#accounts-receivable-entities)
   - [Invoice](#invoice)
   - [Payment](#payment)
   - [CreditMemo](#creditmemo)
   - [Deposit](#deposit)
   - [Customer](#customer)
3. [Inventory & Purchasing Entities](#inventory--purchasing-entities)
   - [Item](#item)
   - [PurchaseOrder](#purchaseorder)
   - [Purchase](#purchase)
   - [Estimate](#estimate)
   - [SalesReceipt](#salesreceipt)
4. [Accounting Entities](#accounting-entities)
   - [Account](#account)
   - [JournalEntry](#journalentry)
5. [Tax Entities](#tax-entities)
   - [TaxCode](#taxcode)
   - [TaxRate](#taxrate)
6. [Other Entities](#other-entities)
   - [Attachable](#attachable)
   - [Preferences](#preferences)
   - [CompanyInfo](#companyinfo)

---

All endpoints use the base pattern:
```
{BASE_URL}/v3/company/{realmId}/{entity}?minorversion=75
```

All update (POST) operations require the current `SyncToken` and `Id` in the
request body. Omitting SyncToken results in error 5010.

---

## Accounts Payable Entities

### Bill

Represents a payable from a vendor.

**Create:**
```http
POST /v3/company/{realmId}/bill?minorversion=75

{
  "VendorRef": {"value": "56"},
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 200.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {"value": "7"}
      }
    }
  ],
  "DueDate": "2025-04-15"
}
```

**Read:**
```http
GET /v3/company/{realmId}/bill/{billId}?minorversion=75
```

**Update** (must include Id and SyncToken):
```http
POST /v3/company/{realmId}/bill?minorversion=75

{
  "Id": "145",
  "SyncToken": "2",
  "VendorRef": {"value": "56"},
  "Line": [...],
  "DueDate": "2025-04-30"
}
```

**Delete:**
```http
POST /v3/company/{realmId}/bill?operation=delete&minorversion=75

{"Id": "145", "SyncToken": "2"}
```

**Key fields:** VendorRef (required), Line (required), DueDate, TxnDate, APAccountRef,
DocNumber, PrivateNote, DepartmentRef, CurrencyRef.

**Line detail types:** AccountBasedExpenseLineDetail (expense account) or
ItemBasedExpenseLineDetail (links to an Item for inventory tracking).

---

### BillPayment

Records payment of one or more bills.

**Create:**
```http
POST /v3/company/{realmId}/billpayment?minorversion=75

{
  "VendorRef": {"value": "56"},
  "TotalAmt": 200.00,
  "PayType": "Check",
  "CheckPayment": {
    "BankAccountRef": {"value": "35"}
  },
  "Line": [
    {
      "Amount": 200.00,
      "LinkedTxn": [
        {"TxnId": "145", "TxnType": "Bill"}
      ]
    }
  ]
}
```

**PayType options:** `Check` (requires CheckPayment.BankAccountRef) or
`CreditCard` (requires CreditCardPayment.CCAccountRef).

A single BillPayment can reference multiple bills in the Line array, enabling
batch payment of multiple vendor invoices.

---

### VendorCredit

A credit from a vendor that can offset future bills.

**Create:**
```http
POST /v3/company/{realmId}/vendorcredit?minorversion=75

{
  "VendorRef": {"value": "56"},
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 50.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {"value": "7"}
      }
    }
  ]
}
```

Apply a vendor credit to a bill payment by including it as a LinkedTxn in the
BillPayment's Line array with `"TxnType": "VendorCredit"`.

---

### Vendor

**Create:**
```http
POST /v3/company/{realmId}/vendor?minorversion=75

{
  "DisplayName": "Acme Ingredients LLC",
  "CompanyName": "Acme Ingredients",
  "PrimaryEmailAddr": {"Address": "ap@acme-ingredients.com"},
  "PrimaryPhone": {"FreeFormNumber": "555-0100"},
  "BillAddr": {
    "Line1": "123 Supply St",
    "City": "Portland",
    "CountrySubDivisionCode": "OR",
    "PostalCode": "97201"
  },
  "TaxIdentifier": "12-3456789"
}
```

**Query examples:**
```sql
SELECT * FROM Vendor WHERE Active = true
SELECT * FROM Vendor WHERE DisplayName LIKE '%Acme%'
SELECT * FROM Vendor WHERE Balance > '0'
```

---

## Accounts Receivable Entities

### Invoice

**Create:**
```http
POST /v3/company/{realmId}/invoice?minorversion=75

{
  "CustomerRef": {"value": "23"},
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 500.00,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1"},
        "Qty": 100,
        "UnitPrice": 5.00
      }
    }
  ],
  "DueDate": "2025-04-15",
  "BillEmail": {"Address": "customer@example.com"}
}
```

**Send via email:**
```http
POST /v3/company/{realmId}/invoice/{invoiceId}/send?sendTo=customer@example.com&minorversion=75
```

**Void:**
```http
POST /v3/company/{realmId}/invoice?minorversion=75

{
  "Id": "130",
  "SyncToken": "3",
  "sparse": true,
  "Void": true
}
```

**Key fields:** CustomerRef (required), Line (required), DueDate, DocNumber,
BillEmail, ShipAddr, BillAddr, SalesTermRef, DepartmentRef, TxnTaxDetail.

---

### Payment

Records receipt of payment from a customer, applied to one or more invoices.

**Create:**
```http
POST /v3/company/{realmId}/payment?minorversion=75

{
  "CustomerRef": {"value": "23"},
  "TotalAmt": 500.00,
  "Line": [
    {
      "Amount": 500.00,
      "LinkedTxn": [
        {"TxnId": "130", "TxnType": "Invoice"}
      ]
    }
  ],
  "DepositToAccountRef": {"value": "35"}
}
```

If TotalAmt exceeds the sum of linked invoices, the excess creates an unapplied
credit on the customer's account.

---

### CreditMemo

A credit issued to a customer.

**Create:**
```http
POST /v3/company/{realmId}/creditmemo?minorversion=75

{
  "CustomerRef": {"value": "23"},
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 50.00,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1"},
        "Qty": 10,
        "UnitPrice": 5.00
      }
    }
  ]
}
```

---

### Deposit

Records a bank deposit, optionally linking undeposited funds from payments.

**Create:**
```http
POST /v3/company/{realmId}/deposit?minorversion=75

{
  "DepositToAccountRef": {"value": "35"},
  "Line": [
    {
      "Amount": 500.00,
      "LinkedTxn": [
        {"TxnId": "200", "TxnType": "Payment"}
      ]
    }
  ]
}
```

---

### Customer

**Create:**
```http
POST /v3/company/{realmId}/customer?minorversion=75

{
  "DisplayName": "Fresh Foods Market",
  "CompanyName": "Fresh Foods Market Inc.",
  "PrimaryEmailAddr": {"Address": "orders@freshfoods.com"},
  "PrimaryPhone": {"FreeFormNumber": "555-0200"},
  "BillAddr": {
    "Line1": "456 Retail Ave",
    "City": "Seattle",
    "CountrySubDivisionCode": "WA",
    "PostalCode": "98101"
  }
}
```

**Query examples:**
```sql
SELECT * FROM Customer WHERE Active = true
SELECT * FROM Customer WHERE DisplayName LIKE '%Fresh%'
SELECT * FROM Customer WHERE Balance > '0'
```

---

## Inventory & Purchasing Entities

### Item

Represents a product or service in the catalog.

**Create inventory item:**
```http
POST /v3/company/{realmId}/item?minorversion=75

{
  "Name": "Organic Vanilla Extract",
  "Type": "Inventory",
  "TrackQtyOnHand": true,
  "QtyOnHand": 500,
  "InvStartDate": "2025-03-01",
  "IncomeAccountRef": {"value": "79"},
  "ExpenseAccountRef": {"value": "80"},
  "AssetAccountRef": {"value": "81"},
  "UnitPrice": 12.50,
  "PurchaseCost": 8.00
}
```

**Item types:**
- `Inventory`: Tracked quantity on hand; requires IncomeAccountRef, ExpenseAccountRef, AssetAccountRef
- `NonInventory`: Purchased or sold but not tracked in inventory
- `Service`: Labor, consulting, professional services

**Query examples:**
```sql
SELECT * FROM Item WHERE Type = 'Inventory'
SELECT * FROM Item WHERE Name LIKE '%Vanilla%'
SELECT * FROM Item WHERE QtyOnHand < '100'
```

---

### PurchaseOrder

Non-posting transaction — does not affect the books until converted to a bill.

**Create:**
```http
POST /v3/company/{realmId}/purchaseorder?minorversion=75

{
  "VendorRef": {"value": "56"},
  "APAccountRef": {"value": "33"},
  "Line": [
    {
      "DetailType": "ItemBasedExpenseLineDetail",
      "Amount": 4000.00,
      "ItemBasedExpenseLineDetail": {
        "ItemRef": {"value": "11"},
        "Qty": 500,
        "UnitPrice": 8.00
      }
    }
  ],
  "ShipAddr": {
    "Line1": "789 Warehouse Blvd",
    "City": "Portland",
    "CountrySubDivisionCode": "OR",
    "PostalCode": "97201"
  }
}
```

Requires QBO Plus or Advanced subscription. Query with:
```sql
SELECT * FROM PurchaseOrder WHERE VendorRef = '56'
SELECT * FROM PurchaseOrder WHERE POStatus = 'Open'
```

---

### Purchase

Records a direct purchase (check, cash, credit card) without a purchase order.

**Create:**
```http
POST /v3/company/{realmId}/purchase?minorversion=75

{
  "PaymentType": "CreditCard",
  "AccountRef": {"value": "42"},
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 150.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {"value": "7"}
      }
    }
  ]
}
```

**PaymentType options:** `Cash`, `Check`, `CreditCard`.

---

### Estimate

A quote or proposal sent to a customer (non-posting).

**Create:**
```http
POST /v3/company/{realmId}/estimate?minorversion=75

{
  "CustomerRef": {"value": "23"},
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 2500.00,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1"},
        "Qty": 500,
        "UnitPrice": 5.00
      }
    }
  ],
  "ExpirationDate": "2025-04-30"
}
```

---

### SalesReceipt

Records a sale where payment is received immediately (no invoice needed).

**Create:**
```http
POST /v3/company/{realmId}/salesreceipt?minorversion=75

{
  "CustomerRef": {"value": "23"},
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 250.00,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1"},
        "Qty": 50,
        "UnitPrice": 5.00
      }
    }
  ],
  "DepositToAccountRef": {"value": "35"},
  "PaymentMethodRef": {"value": "1"}
}
```

---

## Accounting Entities

### Account

Represents a ledger account in the Chart of Accounts.

**Create:**
```http
POST /v3/company/{realmId}/account?minorversion=75

{
  "Name": "Raw Materials - Organic",
  "AccountType": "Cost of Goods Sold",
  "AccountSubType": "SuppliesMaterialsCogs"
}
```

**Common AccountType values:** `Bank`, `Accounts Receivable`, `Other Current Asset`,
`Fixed Asset`, `Accounts Payable`, `Credit Card`, `Other Current Liability`,
`Long Term Liability`, `Equity`, `Income`, `Cost of Goods Sold`, `Expense`,
`Other Income`, `Other Expense`.

**Query:**
```sql
SELECT * FROM Account WHERE AccountType = 'Expense'
SELECT * FROM Account WHERE Active = true
```

---

### JournalEntry

**Create:**
```http
POST /v3/company/{realmId}/journalentry?minorversion=75

{
  "Line": [
    {
      "DetailType": "JournalEntryLineDetail",
      "Amount": 1000.00,
      "JournalEntryLineDetail": {
        "PostingType": "Debit",
        "AccountRef": {"value": "7"}
      }
    },
    {
      "DetailType": "JournalEntryLineDetail",
      "Amount": 1000.00,
      "JournalEntryLineDetail": {
        "PostingType": "Credit",
        "AccountRef": {"value": "35"}
      }
    }
  ],
  "TxnDate": "2025-03-21",
  "PrivateNote": "Inventory adjustment - spoilage"
}
```

Lines referencing an AR-type account must include `"Entity": {"EntityRef": {"value": "customer_id"}, "Type": "Customer"}`.
Lines referencing an AP-type account must include `"Entity": {"EntityRef": {"value": "vendor_id"}, "Type": "Vendor"}`.

---

## Tax Entities

### TaxCode

Proxy tax codes for automated sales tax (AST) in US companies.

**Create proxy:**
```http
POST /v3/company/{realmId}/taxservice/taxcode?minorversion=75

{
  "TaxCode": "MyTax",
  "TaxRateDetails": [
    {
      "TaxRateName": "StateTax",
      "RateValue": "5",
      "TaxAgencyId": "1",
      "TaxApplicableOn": "Sales"
    }
  ]
}
```

For US companies with AST enabled, QBO automatically replaces proxy TaxCodes with
the correct AST-determined rate when the transaction is saved. The correct tax
appears when you read the transaction back.

### TaxRate

Query existing rates:
```sql
SELECT * FROM TaxRate
SELECT * FROM TaxCode
```

TaxRates are typically system-managed in AST-enabled companies. Manual TaxRate
creation is primarily for non-US locales.

---

## Other Entities

### Attachable

Upload documents to QBO and link them to transactions.

**Upload:**
```http
POST /v3/company/{realmId}/upload?minorversion=75
Content-Type: multipart/form-data

--boundary
Content-Disposition: form-data; name="file_metadata_0"
Content-Type: application/json

{
  "FileName": "COA_Acme_Mar2025.pdf",
  "ContentType": "application/pdf",
  "AttachableRef": [
    {"EntityRef": {"type": "Bill", "value": "145"}}
  ]
}
--boundary
Content-Disposition: form-data; name="file_content_0"; filename="COA_Acme_Mar2025.pdf"
Content-Type: application/pdf

{binary file content}
--boundary--
```

**Limits:** 20 MB per transaction, 1000-character file name limit.

### Preferences

Query tenant's accounting settings:
```http
GET /v3/company/{realmId}/preferences?minorversion=75
```

Returns accounting method (Accrual/Cash), currency, fiscal year start, tax settings,
and feature toggles. Always query Preferences before generating reports to use the
correct accounting method.

### CompanyInfo

Query company details and subscription tier:
```http
GET /v3/company/{realmId}/companyinfo/{realmId}?minorversion=75
```

Returns company name, address, subscription status (Simple Start, Essentials, Plus,
Advanced), and feature availability.
