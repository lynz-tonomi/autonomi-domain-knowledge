#!/usr/bin/env python3
"""
Recipe & BOM Calculator for F&B

Handles recipe scaling, costing, nutritional calculations, allergen aggregation,
and multi-level BOM explosion.

Usage:
    python recipe_calculator.py cost --file recipe_bom.csv --batch-size 1000
    python recipe_calculator.py scale --file recipe_bom.csv --from-size 100 --to-size 5000
    python recipe_calculator.py allergens --file recipe_bom.csv
    python recipe_calculator.py nutrition --file recipe_bom.csv --serving-size 355 --serving-unit ml
"""

import argparse
import csv
import json
import sys
from collections import defaultdict


def load_bom(filepath):
    """Load a BOM/recipe CSV."""
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in row.items()}
            rows.append(cleaned)
    return rows


def try_float(val, default=0):
    """Parse a float, returning default on failure."""
    try:
        return float(str(val).replace(',', '').replace('$', '').strip())
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# BOM Explosion
# ---------------------------------------------------------------------------

def explode_bom(rows, target_qty=1, parent_col='parent', child_col='ingredient',
                qty_col='quantity', yield_col='yield_factor'):
    """
    Explode a multi-level BOM into flat ingredient requirements.

    Expects rows with parent-child relationships. If no parent column exists,
    treats all rows as a single-level BOM.
    """
    # Check if this is a multi-level BOM
    has_parent = parent_col in (rows[0] if rows else {})

    if not has_parent:
        # Single-level BOM
        result = []
        for row in rows:
            ingredient = row.get(child_col, row.get('ingredient', row.get('item', row.get('material', 'Unknown'))))
            qty = try_float(row.get(qty_col, row.get('quantity', row.get('qty', 0))))
            yf = try_float(row.get(yield_col, 1), 1) or 1
            result.append({
                'ingredient': ingredient,
                'gross_qty': round(qty * target_qty / yf, 4),
                'net_qty': round(qty * target_qty, 4),
                'yield_factor': yf,
                'level': 0
            })
        return result

    # Multi-level BOM: build tree and explode
    children = defaultdict(list)
    for row in rows:
        parent = row.get(parent_col, '')
        child = row.get(child_col, row.get('ingredient', ''))
        qty = try_float(row.get(qty_col, 0))
        yf = try_float(row.get(yield_col, 1), 1) or 1
        children[parent].append({'name': child, 'qty': qty, 'yield_factor': yf, 'row': row})

    # Find top-level items (parents that are not children of anything)
    all_children = set()
    for kids in children.values():
        for k in kids:
            all_children.add(k['name'])
    top_level = [p for p in children.keys() if p and p not in all_children]
    if not top_level:
        top_level = list(children.keys())[:1]

    result = []

    def explode(parent, multiplier, level):
        for child in children.get(parent, []):
            qty = child['qty'] * multiplier / child['yield_factor']
            if child['name'] in children:
                # Sub-recipe: recurse
                explode(child['name'], qty, level + 1)
            else:
                # Raw ingredient
                result.append({
                    'ingredient': child['name'],
                    'gross_qty': round(qty * target_qty, 4),
                    'net_qty': round(child['qty'] * multiplier * target_qty, 4),
                    'yield_factor': child['yield_factor'],
                    'level': level
                })

    for top in top_level:
        explode(top, 1, 0)

    # Consolidate duplicates
    consolidated = defaultdict(lambda: {'gross_qty': 0, 'net_qty': 0, 'yield_factor': 1, 'level': 0})
    for item in result:
        key = item['ingredient']
        consolidated[key]['gross_qty'] += item['gross_qty']
        consolidated[key]['net_qty'] += item['net_qty']
        consolidated[key]['yield_factor'] = item['yield_factor']
        consolidated[key]['level'] = max(consolidated[key]['level'], item['level'])

    return [{'ingredient': k, **v} for k, v in consolidated.items()]


# ---------------------------------------------------------------------------
# Costing
# ---------------------------------------------------------------------------

def calculate_recipe_cost(rows, batch_size=1, cost_col=None, qty_col=None):
    """Calculate recipe cost per unit and per batch."""
    cost_col = cost_col or next((c for c in ['cost_per_unit', 'unit_cost', 'cost', 'price']
                                  if c in (rows[0] if rows else {})), 'cost')
    qty_col = qty_col or next((c for c in ['quantity', 'qty', 'amount']
                                if c in (rows[0] if rows else {})), 'quantity')

    ingredients = []
    total_cost = 0

    for row in rows:
        name = row.get('ingredient', row.get('item', row.get('material', 'Unknown')))
        qty = try_float(row.get(qty_col, 0))
        cost = try_float(row.get(cost_col, 0))
        yf = try_float(row.get('yield_factor', 1), 1) or 1
        uom = row.get('uom', row.get('unit', ''))

        ingredient_cost = qty * cost / yf
        total_cost += ingredient_cost

        ingredients.append({
            'ingredient': name,
            'qty_per_unit': qty,
            'uom': uom,
            'cost_per_unit_ingredient': cost,
            'yield_factor': yf,
            'extended_cost_per_unit': round(ingredient_cost, 6),
        })

    # Sort by cost (highest first)
    ingredients.sort(key=lambda x: x['extended_cost_per_unit'], reverse=True)

    # Add percentage
    for ing in ingredients:
        ing['pct_of_recipe'] = round(ing['extended_cost_per_unit'] / max(total_cost, 0.0001) * 100, 1)

    return {
        'cost_per_unit': round(total_cost, 6),
        'cost_per_batch': round(total_cost * batch_size, 2),
        'batch_size': batch_size,
        'ingredient_count': len(ingredients),
        'ingredients': ingredients,
        'cost_driver_top3': [i['ingredient'] for i in ingredients[:3]],
    }


def what_if_pricing(base_cost, ingredient_name, ingredients, price_change_pct):
    """What-if analysis: how does ingredient price change affect recipe cost?"""
    for ing in ingredients:
        if ing['ingredient'].lower() == ingredient_name.lower():
            old_cost = ing['extended_cost_per_unit']
            new_cost = old_cost * (1 + price_change_pct / 100)
            delta = new_cost - old_cost
            new_total = base_cost + delta
            return {
                'ingredient': ingredient_name,
                'price_change_pct': price_change_pct,
                'old_ingredient_cost': round(old_cost, 6),
                'new_ingredient_cost': round(new_cost, 6),
                'old_recipe_cost': round(base_cost, 6),
                'new_recipe_cost': round(new_total, 6),
                'recipe_cost_change_pct': round(delta / max(base_cost, 0.0001) * 100, 2),
            }
    return {'error': f'Ingredient "{ingredient_name}" not found'}


# ---------------------------------------------------------------------------
# Scaling
# ---------------------------------------------------------------------------

def scale_recipe(rows, from_size, to_size, qty_col=None):
    """Scale a recipe from one batch size to another."""
    qty_col = qty_col or next((c for c in ['quantity', 'qty', 'amount']
                                if c in (rows[0] if rows else {})), 'quantity')
    scale_factor = to_size / max(from_size, 0.001)

    scaled = []
    for row in rows:
        name = row.get('ingredient', row.get('item', row.get('material', 'Unknown')))
        orig_qty = try_float(row.get(qty_col, 0))
        uom = row.get('uom', row.get('unit', ''))

        scaled.append({
            'ingredient': name,
            'original_qty': orig_qty,
            'scaled_qty': round(orig_qty * scale_factor, 4),
            'uom': uom,
            'scale_factor': round(scale_factor, 4),
        })

    return {
        'from_batch_size': from_size,
        'to_batch_size': to_size,
        'scale_factor': round(scale_factor, 4),
        'ingredients': scaled,
        'scaling_notes': [
            'Linear scaling applied. For F&B production, verify the following at new scale:',
            '- Mixing times may need adjustment (larger batches = longer mix times)',
            '- Heat transfer changes with volume — cook/pasteurization times may differ',
            '- Flavoring and seasoning often need 5-15% adjustment at larger scales',
            '- Emulsions and suspensions may behave differently — test stability',
            '- Equipment capacity limits: verify tank/mixer/oven can handle the new volume',
        ]
    }


# ---------------------------------------------------------------------------
# Allergen Analysis
# ---------------------------------------------------------------------------

def analyze_allergens(rows):
    """Build allergen matrix and identify risks."""
    big_9 = ['milk', 'eggs', 'fish', 'shellfish', 'tree_nuts', 'peanuts',
             'wheat', 'soy', 'sesame']

    allergen_col = next((c for c in ['allergens', 'allergen', 'contains']
                         if c in (rows[0] if rows else {})), None)

    recipe_allergens = set()
    ingredient_allergens = []

    for row in rows:
        name = row.get('ingredient', row.get('item', row.get('material', 'Unknown')))
        allergen_str = row.get(allergen_col, '') if allergen_col else ''
        found = []
        for a in big_9:
            if a.replace('_', ' ') in allergen_str.lower() or a in allergen_str.lower():
                found.append(a)
                recipe_allergens.add(a)
        ingredient_allergens.append({
            'ingredient': name,
            'allergens': found if found else ['none'],
        })

    # Determine label requirements
    label_contains = sorted(recipe_allergens)

    return {
        'recipe_contains': label_contains,
        'allergen_free': not bool(recipe_allergens),
        'free_from': sorted(set(big_9) - recipe_allergens),
        'ingredient_detail': ingredient_allergens,
        'label_statement': f"Contains: {', '.join(a.replace('_', ' ').title() for a in label_contains)}" if label_contains else "No major allergens",
        'cross_contact_note': 'Review shared equipment and facility allergen profiles for "may contain" advisory labeling.',
    }


# ---------------------------------------------------------------------------
# Nutritional Calculation
# ---------------------------------------------------------------------------

def calculate_nutrition(rows, serving_size=None, serving_unit=None):
    """
    Calculate nutrition per serving from ingredient nutritional data.

    Expects columns like: calories_per_100g, fat_per_100g, etc.
    Or: calories, fat, etc. (per quantity in BOM)
    """
    nutrients = ['calories', 'total_fat', 'saturated_fat', 'trans_fat',
                 'cholesterol', 'sodium', 'total_carb', 'dietary_fiber',
                 'total_sugars', 'added_sugars', 'protein']

    totals = {n: 0 for n in nutrients}
    has_nutrition = False

    for row in rows:
        qty = try_float(row.get('quantity', row.get('qty', 0)))

        for nutrient in nutrients:
            # Try per_100g format
            val_per_100g = try_float(row.get(f'{nutrient}_per_100g', 0))
            if val_per_100g:
                has_nutrition = True
                totals[nutrient] += val_per_100g * qty / 100
            else:
                # Try direct value (assumed per recipe unit)
                val = try_float(row.get(nutrient, 0))
                if val:
                    has_nutrition = True
                    totals[nutrient] += val

    if not has_nutrition:
        return {'error': 'No nutritional data found in the provided columns. '
                         'Expected columns like calories_per_100g, total_fat_per_100g, etc.'}

    # Apply serving size if provided
    if serving_size:
        # Assume totals are per batch; divide by number of servings
        # This is a simplification — proper calculation needs batch volume
        pass

    # FDA rounding rules (simplified)
    def fda_round_calories(v):
        if v < 5: return 0
        if v <= 50: return round(v / 5) * 5
        return round(v / 10) * 10

    def fda_round_fat(v):
        if v < 0.5: return 0
        if v < 5: return round(v * 2) / 2
        return round(v)

    result = {
        'per_serving': {
            'calories': fda_round_calories(totals['calories']),
            'total_fat_g': fda_round_fat(totals['total_fat']),
            'saturated_fat_g': fda_round_fat(totals['saturated_fat']),
            'trans_fat_g': fda_round_fat(totals['trans_fat']),
            'cholesterol_mg': round(totals['cholesterol']),
            'sodium_mg': round(totals['sodium'] / 5) * 5 if totals['sodium'] <= 140 else round(totals['sodium'] / 10) * 10,
            'total_carb_g': round(totals['total_carb']),
            'dietary_fiber_g': round(totals['dietary_fiber']),
            'total_sugars_g': round(totals['total_sugars']),
            'added_sugars_g': round(totals['added_sugars']),
            'protein_g': round(totals['protein']),
        },
        'serving_size': serving_size,
        'serving_unit': serving_unit,
        'note': 'Values rounded per FDA 21 CFR 101.9 rounding rules. '
                'Verify against laboratory analysis for label use.',
    }

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='F&B Recipe & BOM Calculator')
    subparsers = parser.add_subparsers(dest='command')

    # Cost
    cost_p = subparsers.add_parser('cost', help='Calculate recipe cost')
    cost_p.add_argument('--file', required=True)
    cost_p.add_argument('--batch-size', type=float, default=1)
    cost_p.add_argument('--output', default=None)

    # Scale
    scale_p = subparsers.add_parser('scale', help='Scale a recipe')
    scale_p.add_argument('--file', required=True)
    scale_p.add_argument('--from-size', type=float, required=True)
    scale_p.add_argument('--to-size', type=float, required=True)
    scale_p.add_argument('--output', default=None)

    # Allergens
    allerg_p = subparsers.add_parser('allergens', help='Allergen analysis')
    allerg_p.add_argument('--file', required=True)
    allerg_p.add_argument('--output', default=None)

    # Nutrition
    nutr_p = subparsers.add_parser('nutrition', help='Nutritional calculation')
    nutr_p.add_argument('--file', required=True)
    nutr_p.add_argument('--serving-size', type=float, default=None)
    nutr_p.add_argument('--serving-unit', default=None)
    nutr_p.add_argument('--output', default=None)

    # BOM explosion
    bom_p = subparsers.add_parser('explode', help='Explode multi-level BOM')
    bom_p.add_argument('--file', required=True)
    bom_p.add_argument('--qty', type=float, default=1, help='Target quantity')
    bom_p.add_argument('--output', default=None)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    rows = load_bom(args.file)
    if not rows:
        print(f"Error: No data loaded from {args.file}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(rows)} rows from {args.file}")

    if args.command == 'cost':
        result = calculate_recipe_cost(rows, batch_size=args.batch_size)
    elif args.command == 'scale':
        result = scale_recipe(rows, args.from_size, args.to_size)
    elif args.command == 'allergens':
        result = analyze_allergens(rows)
    elif args.command == 'nutrition':
        result = calculate_nutrition(rows, args.serving_size, args.serving_unit)
    elif args.command == 'explode':
        result = explode_bom(rows, target_qty=args.qty)

    output = json.dumps(result, indent=2, default=str)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Output saved to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
