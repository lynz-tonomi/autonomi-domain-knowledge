# Data Models Reference
**Skill:** erp-integration | **Domain:** data-models | **Version:** 1.0.0

---

## 1. Autonomi Core Entities

### 1.1 Production Order

| Autonomi Field | Type | Description |
|---|---|---|
| `production_order_id` | String | `PRD-{SITE}-{YYYYMMDD}-{SEQ}` |
| `bom_id` | String | Links to BOM master (BOM-01 through BOM-08) |
| `batch_id` | String | `{SITE}-{LINE}-{YYYYMMDD}-{SEQ}` |
| `status` | Enum | PLANNED / CONFIRMED / IN_PROGRESS / COMPLETED / HOLD / CANCELLED |
| `scheduled_start` | ISO 8601 | Planned start datetime |
| `scheduled_end` | ISO 8601 | Planned end datetime |
| `actual_start` | ISO 8601 | Actual fill start |
| `actual_end` | ISO 8601 | Actual fill end |
| `planned_qty` | Number | Units planned (from batch yield formula) |
| `actual_qty` | Number | Units actually produced |
| `yield_variance` | Number | (actual_qty / planned_qty) - 1, as % |
| `line_id` | String | LINE-01 through LINE-08 |
| `qa_status` | Enum | PENDING / RELEASED / HOLD / REJECTED |
| `blockchain_tx_id` | String | Blockchain record of batch creation |

### 1.2 SAP PP Mapping

| Autonomi Field | SAP Field | SAP Object | Notes |
|---|---|---|---|
| `production_order_id` | `OrderNumber` | Production Order (PP-PI) | SAP auto-generates; Autonomi stores |
| `bom_id` | `Material` | Material Master | Material number in SAP |
| `status` | `SystemStatus` | Production Order | CRTD/REL/TECO/CLSD mapping |
| `scheduled_start` | `BasicStartDate` + `BasicStartTime` | Production Order | Split into date/time fields |
| `planned_qty` | `TotalQuantity` | Production Order | In base UoM |
| `actual_qty` | `ConfirmedQuantity` | Confirmation | From PP order confirmation |
| `yield_variance` | Calculated: PP order report | — | Autonomi calculates; pushes to CO |
| `qa_status` | `UsageDecision` | QM Inspection Lot | 1 = Accepted; 2 = Rejected |

### 1.3 NetSuite Manufacturing Mapping

| Autonomi Field | NetSuite Field | NetSuite Record | Notes |
|---|---|---|---|
| `production_order_id` | `tranId` | Work Order | NS auto-generates |
| `bom_id` | `assemblyItem` | Assembly Item | Item internal ID |
| `status` | `status` | Work Order | Pending Build / Built / Closed |
| `planned_qty` | `quantity` | Work Order | — |
| `actual_qty` | `builtQuantity` | Work Order | After assembly completion |
| `qa_status` | Custom field: `custbody_autonomi_qa_status` | Work Order | Autonomi-specific extension |

---

## 2. Purchase Order Entity

| Autonomi Field | Type | Description |
|---|---|---|
| `po_number` | String | `PO-{SITE}-{YYYYMMDD}-{SEQ}` |
| `vendor_id` | String | Links to vendor master |
| `status` | Enum | DRAFT / ISSUED / ACKNOWLEDGED / RECEIVED / CLOSED / CANCELLED |
| `line_items` | Array | [{sku, description, qty, uom, unit_price, extended_price}] |
| `requested_delivery` | ISO 8601 | Date required at dock |
| `actual_delivery` | ISO 8601 | Actual delivery timestamp |
| `payment_method` | Enum | USDC / ACH / WIRE |
| `payment_terms` | String | Net-7, Net-15, Net-30 |
| `smart_contract_id` | String | Ampersend contract reference |
| `blockchain_tx_id` | String | On-chain PO record |

### 2.1 SAP MM Mapping

| Autonomi Field | SAP Field | SAP Object |
|---|---|---|
| `po_number` | `PurchaseOrder` | Purchasing Document |
| `vendor_id` | `Supplier` | Business Partner (Supplier) |
| `status` | `ProcessingStatus` | PO header |
| `line_items[].sku` | `Material` | PO item |
| `line_items[].qty` | `OrderQuantity` | PO item |
| `line_items[].unit_price` | `NetPriceAmount` | PO item |
| `requested_delivery` | `DeliveryDate` | PO item schedule line |
| `payment_terms` | `PaymentTerms` | PO header |

### 2.2 QBO Mapping

| Autonomi Field | QBO Field | QBO Object |
|---|---|---|
| `po_number` | `DocNumber` | PurchaseOrder |
| `vendor_id` | `VendorRef.value` | PurchaseOrder |
| `line_items` | `Line[]` | PurchaseOrder lines |
| `line_items[].unit_price` | `UnitPrice` | ItemBasedExpenseLineDetail |
| `line_items[].qty` | `Qty` | ItemBasedExpenseLineDetail |
| `requested_delivery` | `ShipDate` | PurchaseOrder |
| `payment_terms` | `SalesTermRef` | Not standard in PO; used in Bill |

---

## 3. Inventory Lot Entity

| Autonomi Field | Type | Description |
|---|---|---|
| `lot_id` | String | `LOT-{SKU}-{YYYYMMDD}-{SEQ}` |
| `sku` | String | Ingredient or finished good SKU |
| `description` | String | Full item description |
| `vendor_id` | String | Source supplier |
| `po_number` | String | Related PO |
| `received_date` | ISO 8601 | Goods receipt timestamp |
| `expiry_date` | ISO 8601 | Best-by or use-by |
| `quantity_received` | Number | Gross weight (lbs) or count |
| `quantity_on_hand` | Number | Current available balance |
| `storage_zone` | String | ZONE-A / ZONE-R / ZONE-F / ZONE-FG-C / ZONE-Q |
| `hold_status` | Enum | RELEASED / HOLD / QUARANTINE |
| `coa_status` | Enum | PENDING / APPROVED / FAILED |
| `blockchain_tx_id` | String | On-chain receipt record |

### 3.1 SAP MM Mapping

| Autonomi Field | SAP Field | SAP Object |
|---|---|---|
| `lot_id` | `Batch` | Batch Master |
| `sku` | `Material` | Material Master |
| `expiry_date` | `NextInspectionDate` or Custom Classification | Batch classification |
| `quantity_on_hand` | `StockInStorageLocation` | Stock Overview (MMBE) |
| `storage_zone` | `StorageLocation` | Warehouse Management |
| `hold_status` | `QualityInspectionStatus` or Stock Type | QM / MM |
| `coa_status` | Custom batch classification | Batch Master extension |

---

## 4. Supplier Invoice Entity

| Autonomi Field | Type | Description |
|---|---|---|
| `invoice_id` | String | `INV-{VENDOR_ID}-{YYYYMMDD}-{SEQ}` |
| `vendor_id` | String | Supplier reference |
| `po_number` | String | Related PO (3-way match) |
| `invoice_date` | ISO 8601 | Invoice date from vendor |
| `due_date` | ISO 8601 | Calculated from payment terms |
| `amount` | Number | Invoice total (USD) |
| `usdc_amount` | Number | Equivalent USDC at conversion rate (1:1) |
| `status` | Enum | RECEIVED / VALIDATED / APPROVED / PAID / DISPUTED |
| `three_way_match` | Boolean | PO + GR + Invoice all matched |
| `approval_level` | String | AUTO / WESTON / OPS_MANAGER / CFO |
| `payment_method` | Enum | USDC / ACH / WIRE |
| `blockchain_tx_id` | String | On-chain payment record when settled |

### 4.1 QBO Bill Mapping

| Autonomi Field | QBO Field | QBO Object |
|---|---|---|
| `invoice_id` | `DocNumber` | Bill |
| `vendor_id` | `VendorRef.value` | Bill |
| `invoice_date` | `TxnDate` | Bill |
| `due_date` | `DueDate` | Bill |
| `amount` | `TotalAmt` | Bill |
| `status` (APPROVED) | `Balance` (0) + linked BillPayment | Bill + BillPayment |
| `payment_method` (USDC) | Custom field `custfield_payment_method` | Bill |

---

## 5. Customer / Tenant Mapping

### 5.1 Tenant → ERP Customer Account

| Tenant | SAP Customer | NetSuite Customer | QBO Customer | Plan |
|---|---|---|---|---|
| PurePress Beverages | CUST-PPB-001 | NS-CUST-4421 | QBO-PPB | Enterprise |
| Cascade Drinks | CUST-CSD-001 | NS-CUST-4422 | QBO-CSD | Growth |
| VitaFlow | CUST-VTF-001 | NS-CUST-4423 | QBO-VTF | Growth |
| SunRise RTD | CUST-SUN-001 | NS-CUST-4424 | QBO-SUN | Starter |

---

## 6. ID Translation Layer

AGNT-25 maintains a translation table that maps Autonomi internal IDs to ERP-specific IDs. This table is the source of truth for all cross-system references.

```json
{
  "autonomi_id": "PO-PPB-20260404-012",
  "erp_mappings": {
    "sap": { "object_type": "PurchaseOrder", "id": "4500012847" },
    "netsuite": { "object_type": "PurchaseOrder", "internal_id": "78234" },
    "qbo": { "object_type": "PurchaseOrder", "id": "QB-PO-5521" }
  },
  "blockchain_tx_id": "0x4a7f3c8d..."
}
```

Every Autonomi record carries its ERP counterpart IDs. When a sync failure occurs, AGNT-24 uses this translation table to retry the specific record without re-syncing the full dataset.
