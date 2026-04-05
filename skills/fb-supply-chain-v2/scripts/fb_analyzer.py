#!/usr/bin/env python3
"""
F&B Supply Chain Analyzer — Core analysis engine.

Handles data loading, cleaning, KPI calculations, and chart generation
across all five supply chain modules (procurement, inventory, logistics,
production, recipe/formulation).

Usage:
    python fb_analyzer.py --help
    python fb_analyzer.py inventory --file data.csv --output report.html
    python fb_analyzer.py procurement --file suppliers.xlsx --output dashboard.html
    python fb_analyzer.py production --file batches.csv --output analysis.html
"""

import argparse
import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict
import csv
import math

# ---------------------------------------------------------------------------
# Data Loading & Cleaning
# ---------------------------------------------------------------------------

def load_csv(filepath):
    """Load a CSV file and return list of dicts with basic cleaning."""
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {}
            for k, v in row.items():
                k = k.strip().lower().replace(' ', '_')
                v = v.strip() if isinstance(v, str) else v
                cleaned[k] = v
            rows.append(cleaned)
    return rows


def try_parse_number(val):
    """Attempt to parse a string as a number."""
    if val is None or val == '':
        return None
    try:
        val = str(val).replace(',', '').replace('$', '').replace('%', '').strip()
        if '.' in val:
            return float(val)
        return int(val)
    except (ValueError, TypeError):
        return None


def try_parse_date(val, formats=None):
    """Attempt to parse a string as a date."""
    if val is None or val == '':
        return None
    if formats is None:
        formats = [
            '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S',
            '%Y/%m/%d', '%d-%m-%Y', '%b %d, %Y', '%B %d, %Y'
        ]
    for fmt in formats:
        try:
            return datetime.strptime(str(val).strip(), fmt)
        except (ValueError, TypeError):
            continue
    return None


def detect_columns(rows, role):
    """
    Auto-detect column roles based on common F&B naming patterns.
    role: 'date', 'quantity', 'cost', 'sku', 'supplier', 'lot', 'expiration'
    Returns the best-matching column name or None.
    """
    patterns = {
        'date': ['date', 'order_date', 'po_date', 'ship_date', 'delivery_date',
                 'production_date', 'received_date', 'created_at', 'timestamp'],
        'quantity': ['quantity', 'qty', 'amount', 'units', 'cases', 'volume',
                     'order_qty', 'received_qty', 'shipped_qty', 'on_hand'],
        'cost': ['cost', 'price', 'unit_cost', 'unit_price', 'total_cost',
                 'amount', 'spend', 'value', 'cogs'],
        'sku': ['sku', 'item', 'product', 'item_code', 'product_code',
                'material', 'ingredient', 'item_number', 'product_name'],
        'supplier': ['supplier', 'vendor', 'supplier_name', 'vendor_name',
                     'source', 'manufacturer'],
        'lot': ['lot', 'lot_number', 'batch', 'batch_id', 'batch_number',
                'lot_id', 'lot_no'],
        'expiration': ['expiration', 'expiry', 'exp_date', 'expiration_date',
                       'best_by', 'best_before', 'use_by', 'shelf_life_end',
                       'bb_date']
    }
    if role not in patterns:
        return None
    if not rows:
        return None
    cols = list(rows[0].keys())
    for pattern in patterns[role]:
        for col in cols:
            if col == pattern or col.startswith(pattern):
                return col
    return None


def clean_dataset(rows):
    """Clean a dataset: parse numbers, dates, strip whitespace."""
    if not rows:
        return rows
    # Detect which columns are numeric vs date vs text
    sample = rows[:min(50, len(rows))]
    col_types = {}
    for col in rows[0].keys():
        nums = sum(1 for r in sample if try_parse_number(r.get(col)) is not None)
        dates = sum(1 for r in sample if try_parse_date(r.get(col)) is not None)
        non_empty = sum(1 for r in sample if r.get(col, '').strip() != '')
        if non_empty == 0:
            col_types[col] = 'empty'
        elif dates > non_empty * 0.7:
            col_types[col] = 'date'
        elif nums > non_empty * 0.7:
            col_types[col] = 'number'
        else:
            col_types[col] = 'text'

    cleaned = []
    for row in rows:
        r = {}
        for col, val in row.items():
            ctype = col_types.get(col, 'text')
            if ctype == 'number':
                r[col] = try_parse_number(val)
            elif ctype == 'date':
                r[col] = try_parse_date(val)
            else:
                r[col] = val
            # Keep original string version too
            r[f'_raw_{col}'] = val
        cleaned.append(r)
    return cleaned


# ---------------------------------------------------------------------------
# Inventory Analysis
# ---------------------------------------------------------------------------

def inventory_kpis(rows, qty_col=None, cost_col=None, date_col=None, exp_col=None, sku_col=None):
    """Calculate inventory KPIs from inventory data."""
    if not qty_col:
        qty_col = detect_columns(rows, 'quantity') or 'quantity'
    if not cost_col:
        cost_col = detect_columns(rows, 'cost') or 'cost'
    if not sku_col:
        sku_col = detect_columns(rows, 'sku') or 'sku'
    if not exp_col:
        exp_col = detect_columns(rows, 'expiration')

    today = datetime.now()
    results = {
        'total_skus': 0,
        'total_units': 0,
        'total_value': 0,
        'avg_value_per_sku': 0,
        'expiring_soon': [],  # Within 30 days
        'expired': [],
        'zero_stock': [],
        'abc_classification': {},
        'dte_distribution': {'green': 0, 'yellow': 0, 'red': 0, 'expired': 0},
    }

    sku_values = defaultdict(float)
    sku_qtys = defaultdict(float)

    for row in rows:
        sku = row.get(sku_col, 'Unknown')
        qty = try_parse_number(row.get(qty_col, 0)) or 0
        cost = try_parse_number(row.get(cost_col, 0)) or 0
        value = qty * cost

        sku_values[sku] += value
        sku_qtys[sku] += qty
        results['total_units'] += qty
        results['total_value'] += value

        # Shelf-life analysis
        if exp_col and row.get(exp_col):
            exp_date = row[exp_col] if isinstance(row[exp_col], datetime) else try_parse_date(row.get(exp_col))
            if exp_date:
                dte = (exp_date - today).days
                if dte < 0:
                    results['expired'].append({'sku': sku, 'dte': dte, 'qty': qty})
                    results['dte_distribution']['expired'] += qty
                elif dte <= 30:
                    results['expiring_soon'].append({'sku': sku, 'dte': dte, 'qty': qty})
                    results['dte_distribution']['red'] += qty
                elif dte <= 90:
                    results['dte_distribution']['yellow'] += qty
                else:
                    results['dte_distribution']['green'] += qty

    results['total_skus'] = len(sku_values)
    results['avg_value_per_sku'] = results['total_value'] / max(len(sku_values), 1)

    # ABC classification
    sorted_skus = sorted(sku_values.items(), key=lambda x: x[1], reverse=True)
    cumulative = 0
    for sku, val in sorted_skus:
        cumulative += val
        pct = cumulative / max(results['total_value'], 0.01) * 100
        if pct <= 80:
            results['abc_classification'][sku] = 'A'
        elif pct <= 95:
            results['abc_classification'][sku] = 'B'
        else:
            results['abc_classification'][sku] = 'C'

    # Zero stock
    for sku, qty in sku_qtys.items():
        if qty <= 0:
            results['zero_stock'].append(sku)

    return results


def safety_stock_calculation(avg_demand, demand_std, avg_lead_time, lead_time_std,
                              service_level=0.95, shelf_life_days=None,
                              retailer_min_pct=None, production_lead_days=0):
    """
    Calculate safety stock with F&B shelf-life constraint.

    Args:
        avg_demand: Average daily demand
        demand_std: Standard deviation of daily demand
        avg_lead_time: Average lead time in days
        lead_time_std: Standard deviation of lead time in days
        service_level: Desired service level (default 95%)
        shelf_life_days: Product shelf life in days (None = no constraint)
        retailer_min_pct: Retailer minimum remaining shelf life % (e.g., 0.75)
        production_lead_days: Days from order to production completion
    """
    # Z-score for service level
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.97: 1.88, 0.98: 2.05, 0.99: 2.33}
    z = z_scores.get(service_level, 1.65)

    # Standard safety stock formula
    ss = z * math.sqrt(avg_lead_time * demand_std**2 + avg_demand**2 * lead_time_std**2)

    # F&B shelf-life cap
    max_useful_ss = None
    if shelf_life_days:
        min_dte = 0
        if retailer_min_pct:
            min_dte = shelf_life_days * retailer_min_pct
        usable_days = shelf_life_days - min_dte - production_lead_days
        max_useful_ss = avg_demand * max(usable_days, 0)
        ss = min(ss, max_useful_ss)

    return {
        'safety_stock_units': round(ss, 1),
        'safety_stock_days': round(ss / max(avg_demand, 0.01), 1),
        'z_score': z,
        'service_level': service_level,
        'shelf_life_cap_applied': max_useful_ss is not None and ss >= (max_useful_ss - 0.1),
        'max_useful_safety_stock': round(max_useful_ss, 1) if max_useful_ss else None
    }


# ---------------------------------------------------------------------------
# Procurement Analysis
# ---------------------------------------------------------------------------

def supplier_scorecard(rows, supplier_col=None, ontime_col=None, quality_col=None, cost_col=None):
    """Generate supplier scorecards from PO/delivery data."""
    if not supplier_col:
        supplier_col = detect_columns(rows, 'supplier') or 'supplier'

    suppliers = defaultdict(lambda: {
        'total_orders': 0, 'on_time': 0, 'quality_pass': 0,
        'total_spend': 0, 'lead_times': []
    })

    date_col = detect_columns(rows, 'date')
    cost_col = cost_col or detect_columns(rows, 'cost')

    for row in rows:
        s = row.get(supplier_col, 'Unknown')
        suppliers[s]['total_orders'] += 1

        # On-time (look for on_time, late, or compare dates)
        if ontime_col and row.get(ontime_col):
            val = str(row[ontime_col]).lower()
            if val in ('yes', 'true', '1', 'on time', 'on_time'):
                suppliers[s]['on_time'] += 1
        elif 'on_time' in row:
            val = str(row.get('on_time', '')).lower()
            if val in ('yes', 'true', '1'):
                suppliers[s]['on_time'] += 1

        # Quality
        if quality_col and row.get(quality_col):
            val = str(row[quality_col]).lower()
            if val in ('pass', 'accepted', 'yes', 'true', '1', 'good'):
                suppliers[s]['quality_pass'] += 1
        elif 'quality' in row:
            val = str(row.get('quality', '')).lower()
            if val in ('pass', 'accepted', 'yes', 'true', '1', 'good'):
                suppliers[s]['quality_pass'] += 1

        # Spend
        if cost_col:
            spend = try_parse_number(row.get(cost_col, 0)) or 0
            suppliers[s]['total_spend'] += spend

        # Lead time
        if 'lead_time' in row or 'lead_time_days' in row:
            lt = try_parse_number(row.get('lead_time') or row.get('lead_time_days'))
            if lt is not None:
                suppliers[s]['lead_times'].append(lt)

    scorecards = []
    for name, data in suppliers.items():
        total = max(data['total_orders'], 1)
        lt = data['lead_times']
        card = {
            'supplier': name,
            'total_orders': data['total_orders'],
            'on_time_rate': round(data['on_time'] / total * 100, 1),
            'quality_rate': round(data['quality_pass'] / total * 100, 1),
            'total_spend': round(data['total_spend'], 2),
            'avg_lead_time': round(sum(lt) / max(len(lt), 1), 1) if lt else None,
            'lead_time_std': round((sum((x - sum(lt)/len(lt))**2 for x in lt) / max(len(lt)-1, 1))**0.5, 1) if len(lt) > 1 else None,
        }
        # Composite score (weighted)
        otw = 0.35  # on-time weight
        qw = 0.40   # quality weight
        cw = 0.25   # cost/lead time weight (lower lead time std = better)
        ot_score = card['on_time_rate']
        q_score = card['quality_rate']
        lt_score = max(0, 100 - (card['lead_time_std'] or 0) * 10)  # penalize variability
        card['composite_score'] = round(ot_score * otw + q_score * qw + lt_score * cw, 1)
        card['tier'] = (
            'Strategic' if card['composite_score'] >= 85 else
            'Preferred' if card['composite_score'] >= 70 else
            'Approved' if card['composite_score'] >= 55 else
            'Probationary'
        )
        scorecards.append(card)

    return sorted(scorecards, key=lambda x: x['composite_score'], reverse=True)


def spend_analysis(rows, supplier_col=None, cost_col=None, category_col=None):
    """Perform Pareto spend analysis."""
    supplier_col = supplier_col or detect_columns(rows, 'supplier') or 'supplier'
    cost_col = cost_col or detect_columns(rows, 'cost') or 'cost'

    by_supplier = defaultdict(float)
    by_category = defaultdict(float)
    total_spend = 0

    for row in rows:
        spend = try_parse_number(row.get(cost_col, 0)) or 0
        supplier = row.get(supplier_col, 'Unknown')
        category = row.get(category_col, 'Uncategorized') if category_col else 'Uncategorized'
        by_supplier[supplier] += spend
        by_category[category] += spend
        total_spend += spend

    # Pareto by supplier
    sorted_suppliers = sorted(by_supplier.items(), key=lambda x: x[1], reverse=True)
    cumulative = 0
    pareto = []
    for supplier, spend in sorted_suppliers:
        cumulative += spend
        pareto.append({
            'supplier': supplier,
            'spend': round(spend, 2),
            'pct_of_total': round(spend / max(total_spend, 0.01) * 100, 1),
            'cumulative_pct': round(cumulative / max(total_spend, 0.01) * 100, 1)
        })

    return {
        'total_spend': round(total_spend, 2),
        'supplier_count': len(by_supplier),
        'top_20pct_spend': round(
            sum(s for _, s in sorted_suppliers[:max(1, len(sorted_suppliers)//5)]) / max(total_spend, 0.01) * 100, 1
        ),
        'by_supplier': pareto,
        'by_category': dict(by_category)
    }


# ---------------------------------------------------------------------------
# Production Analysis
# ---------------------------------------------------------------------------

def production_kpis(rows):
    """Calculate production KPIs from batch/production log data."""
    results = {
        'total_batches': len(rows),
        'total_output': 0,
        'total_input': 0,
        'avg_yield': 0,
        'oee': None,
        'by_product': defaultdict(lambda: {'batches': 0, 'output': 0, 'input': 0, 'yields': []}),
        'by_line': defaultdict(lambda: {'batches': 0, 'runtime_hrs': 0, 'downtime_hrs': 0}),
    }

    yields = []
    sku_col = detect_columns(rows, 'sku') or 'product'

    for row in rows:
        product = row.get(sku_col, row.get('product', 'Unknown'))
        actual = try_parse_number(row.get('actual_output') or row.get('output') or row.get('produced')) or 0
        theoretical = try_parse_number(row.get('theoretical_output') or row.get('planned') or row.get('target')) or 0
        input_qty = try_parse_number(row.get('input') or row.get('raw_material') or row.get('input_qty')) or 0

        results['total_output'] += actual
        results['total_input'] += input_qty
        results['by_product'][product]['batches'] += 1
        results['by_product'][product]['output'] += actual
        results['by_product'][product]['input'] += input_qty

        if theoretical > 0:
            y = actual / theoretical * 100
            yields.append(y)
            results['by_product'][product]['yields'].append(y)

        # OEE components
        line = row.get('line', row.get('equipment', 'Unknown'))
        runtime = try_parse_number(row.get('runtime') or row.get('run_time_hrs')) or 0
        downtime = try_parse_number(row.get('downtime') or row.get('downtime_hrs')) or 0
        results['by_line'][line]['batches'] += 1
        results['by_line'][line]['runtime_hrs'] += runtime
        results['by_line'][line]['downtime_hrs'] += downtime

    if yields:
        results['avg_yield'] = round(sum(yields) / len(yields), 1)

    if results['total_input'] > 0:
        results['waste_rate'] = round((1 - results['total_output'] / results['total_input']) * 100, 1)

    # Calculate OEE by line
    for line, data in results['by_line'].items():
        total_time = data['runtime_hrs'] + data['downtime_hrs']
        if total_time > 0:
            data['availability'] = round(data['runtime_hrs'] / total_time * 100, 1)

    # Convert defaultdicts to regular dicts for JSON serialization
    results['by_product'] = dict(results['by_product'])
    results['by_line'] = dict(results['by_line'])

    return results


# ---------------------------------------------------------------------------
# Recipe / BOM Analysis
# ---------------------------------------------------------------------------

def recipe_cost(bom_rows, cost_col=None, qty_col=None, yield_col=None):
    """Calculate recipe cost from BOM data."""
    cost_col = cost_col or detect_columns(bom_rows, 'cost') or 'cost_per_unit'
    qty_col = qty_col or detect_columns(bom_rows, 'quantity') or 'quantity'

    total_cost = 0
    ingredients = []

    for row in bom_rows:
        cost = try_parse_number(row.get(cost_col, 0)) or 0
        qty = try_parse_number(row.get(qty_col, 0)) or 0
        yield_factor = try_parse_number(row.get(yield_col or 'yield_factor', 1)) or 1
        if yield_factor == 0:
            yield_factor = 1

        ingredient_cost = qty * cost / yield_factor
        total_cost += ingredient_cost

        ingredient = row.get('ingredient', row.get('item', row.get('material', 'Unknown')))
        ingredients.append({
            'ingredient': ingredient,
            'quantity': qty,
            'unit_cost': cost,
            'yield_factor': yield_factor,
            'extended_cost': round(ingredient_cost, 4),
            'pct_of_total': 0  # calculated below
        })

    for ing in ingredients:
        ing['pct_of_total'] = round(ing['extended_cost'] / max(total_cost, 0.01) * 100, 1)

    return {
        'total_recipe_cost': round(total_cost, 4),
        'ingredient_count': len(ingredients),
        'ingredients': sorted(ingredients, key=lambda x: x['extended_cost'], reverse=True),
        'top_cost_driver': ingredients[0]['ingredient'] if ingredients else None
    }


def allergen_matrix(recipe_rows):
    """Build allergen matrix from recipe/ingredient data."""
    allergens = ['milk', 'eggs', 'fish', 'shellfish', 'tree_nuts', 'peanuts',
                 'wheat', 'soy', 'sesame']
    matrix = defaultdict(lambda: {a: False for a in allergens})

    recipe_col = detect_columns(recipe_rows, 'sku') or 'recipe'
    for row in recipe_rows:
        recipe = row.get(recipe_col, row.get('recipe', row.get('product', 'Unknown')))
        allergen_val = row.get('allergens', row.get('allergen', ''))
        if allergen_val:
            for a in allergens:
                if a.replace('_', ' ') in str(allergen_val).lower() or a in str(allergen_val).lower():
                    matrix[recipe][a] = True

    return dict(matrix)


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_html_report(title, sections):
    """
    Generate a standalone HTML report.

    sections: list of dicts with 'title', 'content' (HTML string), optional 'chart_data'
    """
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #f5f7fa; color: #1a1a2e; line-height: 1.6; }}
  .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
             color: white; padding: 2rem; }}
  .header h1 {{ font-size: 1.8rem; font-weight: 600; }}
  .header .subtitle {{ opacity: 0.8; margin-top: 0.3rem; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 1.5rem; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
               gap: 1rem; margin: 1.5rem 0; }}
  .kpi-card {{ background: white; border-radius: 12px; padding: 1.2rem;
               box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
  .kpi-card .label {{ font-size: 0.8rem; color: #666; text-transform: uppercase;
                      letter-spacing: 0.05em; }}
  .kpi-card .value {{ font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0.3rem 0; }}
  .kpi-card .detail {{ font-size: 0.85rem; color: #888; }}
  .section {{ background: white; border-radius: 12px; padding: 1.5rem;
              box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 1.5rem; }}
  .section h2 {{ font-size: 1.2rem; margin-bottom: 1rem; color: #1a1a2e; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  th {{ background: #f0f2f5; padding: 0.7rem; text-align: left; font-weight: 600;
        border-bottom: 2px solid #ddd; }}
  td {{ padding: 0.7rem; border-bottom: 1px solid #eee; }}
  tr:hover {{ background: #f8f9fb; }}
  .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px;
            font-size: 0.75rem; font-weight: 600; }}
  .badge-green {{ background: #d4edda; color: #155724; }}
  .badge-yellow {{ background: #fff3cd; color: #856404; }}
  .badge-red {{ background: #f8d7da; color: #721c24; }}
  .badge-blue {{ background: #cce5ff; color: #004085; }}
  .alert {{ padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
  .alert-warning {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
  .alert-danger {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
  .alert-info {{ background: #cce5ff; border-left: 4px solid #0d6efd; }}
  .timestamp {{ text-align: center; color: #999; padding: 1rem; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="header">
  <h1>{title}</h1>
  <div class="subtitle">Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
</div>
<div class="container">
"""
    for section in sections:
        html += f'<div class="section"><h2>{section["title"]}</h2>{section["content"]}</div>\n'

    html += f"""
<div class="timestamp">Report generated by F&B Supply Chain Agent</div>
</div>
</body>
</html>"""
    return html


def kpi_card_html(label, value, detail=''):
    """Generate HTML for a single KPI card."""
    return f'''<div class="kpi-card">
  <div class="label">{label}</div>
  <div class="value">{value}</div>
  <div class="detail">{detail}</div>
</div>'''


def table_html(headers, rows_data, formatters=None):
    """Generate an HTML table."""
    html = '<table><thead><tr>'
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for row in rows_data:
        html += '<tr>'
        for i, cell in enumerate(row):
            if formatters and i in formatters:
                cell = formatters[i](cell)
            html += f'<td>{cell}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def badge(text, color):
    """Generate a colored badge."""
    return f'<span class="badge badge-{color}">{text}</span>'


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='F&B Supply Chain Analyzer')
    subparsers = parser.add_subparsers(dest='module', help='Analysis module')

    # Inventory
    inv_parser = subparsers.add_parser('inventory', help='Inventory analysis')
    inv_parser.add_argument('--file', required=True, help='CSV/Excel file path')
    inv_parser.add_argument('--output', default='inventory_report.html', help='Output file')

    # Procurement
    proc_parser = subparsers.add_parser('procurement', help='Procurement analysis')
    proc_parser.add_argument('--file', required=True, help='CSV/Excel file path')
    proc_parser.add_argument('--output', default='procurement_report.html', help='Output file')

    # Production
    prod_parser = subparsers.add_parser('production', help='Production analysis')
    prod_parser.add_argument('--file', required=True, help='CSV/Excel file path')
    prod_parser.add_argument('--output', default='production_report.html', help='Output file')

    # Recipe
    rec_parser = subparsers.add_parser('recipe', help='Recipe/BOM analysis')
    rec_parser.add_argument('--file', required=True, help='CSV/Excel file path')
    rec_parser.add_argument('--output', default='recipe_report.html', help='Output file')

    # KPIs (JSON output)
    kpi_parser = subparsers.add_parser('kpis', help='Calculate KPIs and output JSON')
    kpi_parser.add_argument('--file', required=True)
    kpi_parser.add_argument('--type', choices=['inventory', 'procurement', 'production', 'recipe'], required=True)

    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        sys.exit(1)

    # Load data
    data = load_csv(args.file)
    if not data:
        print(f"Error: No data loaded from {args.file}", file=sys.stderr)
        sys.exit(1)

    data = clean_dataset(data)
    print(f"Loaded {len(data)} rows from {args.file}")

    if args.module == 'kpis':
        if args.type == 'inventory':
            result = inventory_kpis(data)
        elif args.type == 'procurement':
            result = supplier_scorecard(data)
        elif args.type == 'production':
            result = production_kpis(data)
        elif args.type == 'recipe':
            result = recipe_cost(data)
        print(json.dumps(result, indent=2, default=str))
        return

    if args.module == 'inventory':
        kpis = inventory_kpis(data)
        sections = []
        # KPI cards
        kpi_html = '<div class="kpi-grid">'
        kpi_html += kpi_card_html('Total SKUs', f"{kpis['total_skus']:,}", '')
        kpi_html += kpi_card_html('Total Units', f"{kpis['total_units']:,.0f}", '')
        kpi_html += kpi_card_html('Total Value', f"${kpis['total_value']:,.0f}", f"Avg ${kpis['avg_value_per_sku']:,.0f}/SKU")
        kpi_html += kpi_card_html('Zero Stock SKUs', str(len(kpis['zero_stock'])), 'Potential stockouts')
        kpi_html += '</div>'
        sections.append({'title': 'Inventory Overview', 'content': kpi_html})

        # Shelf life
        if kpis['expired'] or kpis['expiring_soon']:
            alerts = ''
            if kpis['expired']:
                alerts += f'<div class="alert alert-danger"><strong>{len(kpis["expired"])} SKUs have expired inventory</strong> — total {sum(e["qty"] for e in kpis["expired"]):,.0f} units need disposal</div>'
            if kpis['expiring_soon']:
                alerts += f'<div class="alert alert-warning"><strong>{len(kpis["expiring_soon"])} SKUs expiring within 30 days</strong> — prioritize for shipment or markdown</div>'
            sections.append({'title': 'Shelf Life Alerts', 'content': alerts})

        # ABC
        abc_counts = defaultdict(int)
        for cls in kpis['abc_classification'].values():
            abc_counts[cls] += 1
        abc_html = f'<p>{badge(f"A: {abc_counts.get(\"A\", 0)} SKUs", "green")} '
        abc_html += f'{badge(f"B: {abc_counts.get(\"B\", 0)} SKUs", "yellow")} '
        abc_html += f'{badge(f"C: {abc_counts.get(\"C\", 0)} SKUs", "red")}</p>'
        sections.append({'title': 'ABC Classification', 'content': abc_html})

        report = generate_html_report('Inventory Analysis Report', sections)
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")

    elif args.module == 'procurement':
        scorecards = supplier_scorecard(data)
        spend = spend_analysis(data)
        sections = []

        # Spend overview
        kpi_html = '<div class="kpi-grid">'
        kpi_html += kpi_card_html('Total Spend', f"${spend['total_spend']:,.0f}", '')
        kpi_html += kpi_card_html('Suppliers', str(spend['supplier_count']), '')
        kpi_html += kpi_card_html('Top 20% Concentration', f"{spend['top_20pct_spend']}%", 'of total spend')
        kpi_html += '</div>'
        sections.append({'title': 'Spend Overview', 'content': kpi_html})

        # Scorecards table
        headers = ['Supplier', 'Orders', 'On-Time %', 'Quality %', 'Spend', 'Avg Lead Time', 'Score', 'Tier']
        rows_data = []
        for sc in scorecards:
            tier_color = {'Strategic': 'green', 'Preferred': 'blue', 'Approved': 'yellow', 'Probationary': 'red'}
            rows_data.append([
                sc['supplier'], sc['total_orders'],
                f"{sc['on_time_rate']}%", f"{sc['quality_rate']}%",
                f"${sc['total_spend']:,.0f}",
                f"{sc['avg_lead_time']} days" if sc['avg_lead_time'] else 'N/A',
                f"{sc['composite_score']}",
                badge(sc['tier'], tier_color.get(sc['tier'], 'blue'))
            ])
        sections.append({'title': 'Supplier Scorecards', 'content': table_html(headers, rows_data)})

        report = generate_html_report('Procurement Analysis Report', sections)
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")

    elif args.module == 'production':
        kpis = production_kpis(data)
        sections = []

        kpi_html = '<div class="kpi-grid">'
        kpi_html += kpi_card_html('Total Batches', str(kpis['total_batches']), '')
        kpi_html += kpi_card_html('Avg Yield', f"{kpis['avg_yield']}%", '')
        kpi_html += kpi_card_html('Total Output', f"{kpis['total_output']:,.0f}", 'units')
        waste = kpis.get('waste_rate', 'N/A')
        kpi_html += kpi_card_html('Waste Rate', f"{waste}%" if isinstance(waste, (int, float)) else waste, '')
        kpi_html += '</div>'
        sections.append({'title': 'Production Overview', 'content': kpi_html})

        report = generate_html_report('Production Analysis Report', sections)
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")

    elif args.module == 'recipe':
        costs = recipe_cost(data)
        sections = []

        kpi_html = '<div class="kpi-grid">'
        kpi_html += kpi_card_html('Recipe Cost', f"${costs['total_recipe_cost']:.4f}", 'per unit')
        kpi_html += kpi_card_html('Ingredients', str(costs['ingredient_count']), '')
        kpi_html += kpi_card_html('Top Cost Driver', costs['top_cost_driver'] or 'N/A', '')
        kpi_html += '</div>'
        sections.append({'title': 'Recipe Cost Summary', 'content': kpi_html})

        headers = ['Ingredient', 'Quantity', 'Unit Cost', 'Yield', 'Extended Cost', '% of Total']
        rows_data = [[
            i['ingredient'], i['quantity'], f"${i['unit_cost']:.4f}",
            f"{i['yield_factor']:.2f}", f"${i['extended_cost']:.4f}", f"{i['pct_of_total']}%"
        ] for i in costs['ingredients']]
        sections.append({'title': 'Ingredient Breakdown', 'content': table_html(headers, rows_data)})

        report = generate_html_report('Recipe Cost Analysis', sections)
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")


if __name__ == '__main__':
    main()
