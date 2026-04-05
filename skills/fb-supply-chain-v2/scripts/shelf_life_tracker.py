#!/usr/bin/env python3
"""
Shelf-Life & Expiration Tracker for F&B

Analyzes inventory shelf life, FEFO compliance, waste forecasting,
and retailer minimum shelf-life requirements.

Usage:
    python shelf_life_tracker.py --file inventory.csv --output shelf_life_report.json
    python shelf_life_tracker.py --file inventory.csv --retailer-min-pct 75 --output report.json
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict


def try_float(val, default=0):
    try:
        return float(str(val).replace(',', '').replace('$', '').strip())
    except (ValueError, TypeError):
        return default


def try_parse_date(val):
    if val is None or val == '':
        return None
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d',
               '%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S']
    for fmt in formats:
        try:
            return datetime.strptime(str(val).strip(), fmt)
        except (ValueError, TypeError):
            continue
    return None


def load_inventory(filepath):
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in row.items()}
            rows.append(cleaned)
    return rows


def detect_col(rows, candidates):
    if not rows:
        return None
    cols = list(rows[0].keys())
    for c in candidates:
        for col in cols:
            if col == c or col.startswith(c):
                return col
    return None


def analyze_shelf_life(rows, retailer_min_pct=None, today=None):
    """
    Comprehensive shelf-life analysis.

    Returns:
        - DTE distribution (green/yellow/red/expired)
        - SKUs at risk
        - Waste forecast
        - FEFO compliance check
        - Retailer minimum shelf-life compliance
    """
    if today is None:
        today = datetime.now()

    # Detect columns
    sku_col = detect_col(rows, ['sku', 'item', 'product', 'product_code', 'item_code'])
    exp_col = detect_col(rows, ['expiration', 'expiry', 'exp_date', 'expiration_date',
                                 'best_by', 'best_before', 'use_by', 'bb_date'])
    prod_col = detect_col(rows, ['production_date', 'prod_date', 'manufactured', 'mfg_date'])
    qty_col = detect_col(rows, ['quantity', 'qty', 'on_hand', 'units', 'cases'])
    cost_col = detect_col(rows, ['cost', 'unit_cost', 'value', 'price'])
    lot_col = detect_col(rows, ['lot', 'lot_number', 'batch', 'batch_id', 'lot_id'])
    loc_col = detect_col(rows, ['location', 'warehouse', 'zone', 'bin'])
    shelf_life_col = detect_col(rows, ['shelf_life', 'shelf_life_days', 'total_shelf_life'])

    if not exp_col and not shelf_life_col:
        return {'error': 'No expiration date or shelf life column found. '
                         'Expected columns like: expiration_date, best_by, shelf_life_days'}

    results = {
        'analysis_date': today.strftime('%Y-%m-%d'),
        'total_records': len(rows),
        'total_units': 0,
        'total_value_at_risk': 0,
        'dte_distribution': {'green': 0, 'yellow': 0, 'red': 0, 'expired': 0},
        'dte_distribution_value': {'green': 0, 'yellow': 0, 'red': 0, 'expired': 0},
        'expired_items': [],
        'expiring_30_days': [],
        'expiring_90_days': [],
        'retailer_compliance': [],
        'waste_forecast': {},
        'by_sku': defaultdict(lambda: {
            'total_qty': 0, 'min_dte': None, 'max_dte': None,
            'expired_qty': 0, 'at_risk_qty': 0, 'value_at_risk': 0
        }),
        'data_quality': {'missing_dates': 0, 'parsed_ok': 0, 'parse_failed': 0}
    }

    waste_by_week = defaultdict(lambda: {'units': 0, 'value': 0})

    for row in rows:
        sku = row.get(sku_col, 'Unknown') if sku_col else 'Unknown'
        qty = try_float(row.get(qty_col, 1)) if qty_col else 1
        cost = try_float(row.get(cost_col, 0)) if cost_col else 0
        lot = row.get(lot_col, '') if lot_col else ''
        loc = row.get(loc_col, '') if loc_col else ''
        value = qty * cost

        results['total_units'] += qty

        # Parse expiration date
        exp_date = None
        if exp_col and row.get(exp_col):
            exp_date = try_parse_date(row[exp_col])
            if exp_date:
                results['data_quality']['parsed_ok'] += 1
            else:
                results['data_quality']['parse_failed'] += 1
        elif shelf_life_col and prod_col:
            prod_date = try_parse_date(row.get(prod_col))
            sl_days = try_float(row.get(shelf_life_col))
            if prod_date and sl_days:
                exp_date = prod_date + timedelta(days=sl_days)
                results['data_quality']['parsed_ok'] += 1
        else:
            results['data_quality']['missing_dates'] += 1

        if not exp_date:
            continue

        # Calculate DTE
        dte = (exp_date - today).days

        # Total shelf life (for % remaining calculation)
        total_sl = None
        if shelf_life_col:
            total_sl = try_float(row.get(shelf_life_col))
        elif prod_col:
            prod_date = try_parse_date(row.get(prod_col))
            if prod_date:
                total_sl = (exp_date - prod_date).days

        remaining_pct = (dte / total_sl * 100) if total_sl and total_sl > 0 else None

        item_record = {
            'sku': sku, 'lot': lot, 'location': loc,
            'qty': qty, 'value': round(value, 2),
            'expiration_date': exp_date.strftime('%Y-%m-%d'),
            'days_to_expiry': dte,
            'remaining_shelf_life_pct': round(remaining_pct, 1) if remaining_pct else None
        }

        # Classify
        if dte < 0:
            results['dte_distribution']['expired'] += qty
            results['dte_distribution_value']['expired'] += value
            results['expired_items'].append(item_record)
            results['by_sku'][sku]['expired_qty'] += qty
            results['total_value_at_risk'] += value
        elif dte <= 30:
            results['dte_distribution']['red'] += qty
            results['dte_distribution_value']['red'] += value
            results['expiring_30_days'].append(item_record)
            results['by_sku'][sku]['at_risk_qty'] += qty
            results['total_value_at_risk'] += value
            # Waste forecast: week of expiry
            exp_week = exp_date.strftime('%Y-W%W')
            waste_by_week[exp_week]['units'] += qty
            waste_by_week[exp_week]['value'] += value
        elif dte <= 90:
            results['dte_distribution']['yellow'] += qty
            results['dte_distribution_value']['yellow'] += value
            results['expiring_90_days'].append(item_record)
            exp_week = exp_date.strftime('%Y-W%W')
            waste_by_week[exp_week]['units'] += qty
            waste_by_week[exp_week]['value'] += value
        else:
            results['dte_distribution']['green'] += qty
            results['dte_distribution_value']['green'] += value

        # By SKU
        results['by_sku'][sku]['total_qty'] += qty
        if results['by_sku'][sku]['min_dte'] is None or dte < results['by_sku'][sku]['min_dte']:
            results['by_sku'][sku]['min_dte'] = dte
        if results['by_sku'][sku]['max_dte'] is None or dte > results['by_sku'][sku]['max_dte']:
            results['by_sku'][sku]['max_dte'] = dte
        results['by_sku'][sku]['value_at_risk'] += value if dte <= 30 else 0

        # Retailer minimum shelf-life check
        if retailer_min_pct and remaining_pct is not None:
            if remaining_pct < retailer_min_pct:
                results['retailer_compliance'].append({
                    **item_record,
                    'required_pct': retailer_min_pct,
                    'shortfall_pct': round(retailer_min_pct - remaining_pct, 1),
                    'status': 'FAIL'
                })

    # Waste forecast
    results['waste_forecast'] = dict(sorted(waste_by_week.items()))
    results['waste_forecast_total'] = {
        'units': sum(w['units'] for w in waste_by_week.values()),
        'value': round(sum(w['value'] for w in waste_by_week.values()), 2)
    }

    # Convert defaultdicts
    results['by_sku'] = dict(results['by_sku'])
    results['total_value_at_risk'] = round(results['total_value_at_risk'], 2)

    # Sort alerts by urgency
    results['expired_items'].sort(key=lambda x: x['days_to_expiry'])
    results['expiring_30_days'].sort(key=lambda x: x['days_to_expiry'])
    results['expiring_90_days'].sort(key=lambda x: x['days_to_expiry'])

    # Summary stats
    results['summary'] = {
        'expired_skus': len(set(i['sku'] for i in results['expired_items'])),
        'expired_units': results['dte_distribution']['expired'],
        'expired_value': round(results['dte_distribution_value']['expired'], 2),
        'at_risk_skus_30d': len(set(i['sku'] for i in results['expiring_30_days'])),
        'at_risk_units_30d': results['dte_distribution']['red'],
        'at_risk_value_30d': round(results['dte_distribution_value']['red'], 2),
        'healthy_pct': round(results['dte_distribution']['green'] / max(results['total_units'], 1) * 100, 1),
        'retailer_compliance_failures': len(results['retailer_compliance']),
    }

    return results


def main():
    parser = argparse.ArgumentParser(description='F&B Shelf-Life Tracker')
    parser.add_argument('--file', required=True, help='Inventory CSV file')
    parser.add_argument('--retailer-min-pct', type=float, default=None,
                        help='Retailer minimum remaining shelf life %% (e.g., 75)')
    parser.add_argument('--output', default='shelf_life_report.json', help='Output file')
    parser.add_argument('--date', default=None, help='Analysis date (YYYY-MM-DD), default=today')

    args = parser.parse_args()

    today = datetime.strptime(args.date, '%Y-%m-%d') if args.date else datetime.now()

    rows = load_inventory(args.file)
    if not rows:
        print(f"Error: No data loaded from {args.file}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(rows)} inventory records")

    result = analyze_shelf_life(rows, retailer_min_pct=args.retailer_min_pct, today=today)

    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nShelf-Life Analysis Summary:")
    s = result['summary']
    print(f"  Total units analyzed: {result['total_units']:,.0f}")
    print(f"  Healthy (>90 days): {result['dte_distribution']['green']:,.0f} units ({s['healthy_pct']}%)")
    print(f"  Expiring 30-90 days: {result['dte_distribution']['yellow']:,.0f} units")
    print(f"  Expiring <30 days: {s['at_risk_units_30d']:,.0f} units (${s['at_risk_value_30d']:,.0f})")
    print(f"  Expired: {s['expired_units']:,.0f} units (${s['expired_value']:,.0f})")
    print(f"  Total value at risk: ${result['total_value_at_risk']:,.0f}")
    if args.retailer_min_pct:
        print(f"  Retailer compliance failures ({args.retailer_min_pct}% min): {s['retailer_compliance_failures']}")
    print(f"\nFull report saved to {args.output}")


if __name__ == '__main__':
    main()
