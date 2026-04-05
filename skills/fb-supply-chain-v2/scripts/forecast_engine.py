#!/usr/bin/env python3
"""
F&B Demand Forecasting Engine

Supports multiple forecasting methods with F&B-specific features:
seasonality decomposition, promotion lift modeling, and new product analogues.

Usage:
    python forecast_engine.py --file sales_data.csv --periods 12 --method ema --output forecast.json
    python forecast_engine.py --file sales_data.csv --periods 6 --method holtwinters --seasonal-period 12
"""

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timedelta
from collections import defaultdict


def load_time_series(filepath, date_col=None, value_col=None, sku_col=None):
    """Load time series data from CSV."""
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        cols = [c.strip().lower().replace(' ', '_') for c in reader.fieldnames]
        # Auto-detect columns
        if not date_col:
            for c in cols:
                if any(d in c for d in ['date', 'period', 'month', 'week', 'day']):
                    date_col = c
                    break
        if not value_col:
            for c in cols:
                if any(v in c for v in ['quantity', 'qty', 'sales', 'demand', 'units', 'volume', 'cases']):
                    value_col = c
                    break
        if not sku_col:
            for c in cols:
                if any(s in c for s in ['sku', 'product', 'item']):
                    sku_col = c
                    break

        f.seek(0)
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k.strip().lower().replace(' ', '_'): v.strip() for k, v in row.items()}
            rows.append(cleaned)

    return rows, date_col, value_col, sku_col


def parse_series(rows, date_col, value_col, sku_col=None, target_sku=None):
    """Extract a single time series (optionally filtered by SKU)."""
    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d', '%b %Y', '%B %Y',
                    '%Y-%m', '%m-%Y']
    series = []
    for row in rows:
        if sku_col and target_sku and row.get(sku_col, '') != target_sku:
            continue
        date_str = row.get(date_col, '')
        val_str = row.get(value_col, '0')
        val = float(str(val_str).replace(',', '').replace('$', ''))
        dt = None
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if dt is not None:
            series.append((dt, val))

    series.sort(key=lambda x: x[0])
    return series


# ---------------------------------------------------------------------------
# Forecasting Methods
# ---------------------------------------------------------------------------

def simple_moving_average(values, window=3):
    """Simple Moving Average."""
    if len(values) < window:
        return sum(values) / len(values) if values else 0
    return sum(values[-window:]) / window


def weighted_moving_average(values, weights=None):
    """Weighted Moving Average — more recent periods get more weight."""
    if not values:
        return 0
    n = len(values)
    if weights is None:
        # Default: linear weights (most recent = highest)
        weights = list(range(1, n + 1))
    total_weight = sum(weights[-n:])
    return sum(v * w for v, w in zip(values, weights[-n:])) / total_weight


def exponential_moving_average(values, alpha=0.3):
    """Exponential Moving Average (Single Exponential Smoothing)."""
    if not values:
        return 0
    ema = values[0]
    for v in values[1:]:
        ema = alpha * v + (1 - alpha) * ema
    return ema


def double_exponential_smoothing(values, alpha=0.3, beta=0.1, periods=1):
    """Holt's method — handles trend."""
    if len(values) < 2:
        return [values[-1] if values else 0] * periods

    level = values[0]
    trend = values[1] - values[0]
    forecasts = []

    for v in values:
        prev_level = level
        level = alpha * v + (1 - alpha) * (level + trend)
        trend = beta * (level - prev_level) + (1 - beta) * trend

    for i in range(1, periods + 1):
        forecasts.append(level + i * trend)

    return forecasts


def holt_winters(values, alpha=0.3, beta=0.1, gamma=0.3, seasonal_period=12, periods=1):
    """Holt-Winters triple exponential smoothing with additive seasonality."""
    n = len(values)
    if n < seasonal_period * 2:
        # Fall back to double exponential if not enough data for seasonality
        return double_exponential_smoothing(values, alpha, beta, periods)

    # Initialize seasonal components
    season = [0] * seasonal_period
    for i in range(seasonal_period):
        season[i] = values[i] - sum(values[:seasonal_period]) / seasonal_period

    level = sum(values[:seasonal_period]) / seasonal_period
    trend = (sum(values[seasonal_period:2*seasonal_period]) - sum(values[:seasonal_period])) / (seasonal_period ** 2)

    for i in range(n):
        si = i % seasonal_period
        prev_level = level
        level = alpha * (values[i] - season[si]) + (1 - alpha) * (level + trend)
        trend = beta * (level - prev_level) + (1 - beta) * trend
        season[si] = gamma * (values[i] - level) + (1 - gamma) * season[si]

    forecasts = []
    for i in range(1, periods + 1):
        si = (n + i - 1) % seasonal_period
        forecasts.append(level + i * trend + season[si])

    return forecasts


def seasonal_decomposition(values, period=12):
    """Decompose time series into trend, seasonal, and residual components."""
    n = len(values)
    if n < period:
        return {'trend': values, 'seasonal': [0]*n, 'residual': [0]*n}

    # Moving average for trend
    half = period // 2
    trend = [None] * n
    for i in range(half, n - half):
        window = values[max(0, i-half):min(n, i+half+1)]
        trend[i] = sum(window) / len(window)

    # Fill ends
    for i in range(half):
        trend[i] = trend[half]
    for i in range(n - half, n):
        trend[i] = trend[n - half - 1]

    # Seasonal
    detrended = [values[i] - trend[i] for i in range(n)]
    seasonal = [0] * n
    for i in range(period):
        indices = [j for j in range(i, n, period)]
        avg = sum(detrended[j] for j in indices) / len(indices)
        for j in indices:
            seasonal[j] = avg

    # Residual
    residual = [values[i] - trend[i] - seasonal[i] for i in range(n)]

    return {'trend': trend, 'seasonal': seasonal, 'residual': residual}


# ---------------------------------------------------------------------------
# Forecast Accuracy Metrics
# ---------------------------------------------------------------------------

def calculate_accuracy(actual, forecast):
    """Calculate forecast accuracy metrics."""
    n = min(len(actual), len(forecast))
    if n == 0:
        return {}

    errors = [actual[i] - forecast[i] for i in range(n)]
    abs_errors = [abs(e) for e in errors]
    pct_errors = [abs(e) / max(actual[i], 0.01) * 100 for i, e in enumerate(errors)]

    mae = sum(abs_errors) / n
    mape = sum(pct_errors) / n
    rmse = math.sqrt(sum(e**2 for e in errors) / n)
    bias = sum(errors) / n  # Positive = under-forecasting, Negative = over-forecasting

    return {
        'mae': round(mae, 2),
        'mape': round(mape, 1),
        'rmse': round(rmse, 2),
        'bias': round(bias, 2),
        'n_periods': n
    }


# ---------------------------------------------------------------------------
# Confidence Intervals
# ---------------------------------------------------------------------------

def confidence_intervals(forecast_values, historical_errors, confidence=0.95):
    """Calculate confidence intervals for forecasts."""
    if not historical_errors:
        return [(f, f, f) for f in forecast_values]

    std_error = math.sqrt(sum(e**2 for e in historical_errors) / len(historical_errors))
    z = {0.80: 1.28, 0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence, 1.96)

    intervals = []
    for i, f in enumerate(forecast_values):
        # Uncertainty grows with forecast horizon
        horizon_factor = math.sqrt(1 + i * 0.1)
        margin = z * std_error * horizon_factor
        intervals.append((round(f - margin, 1), round(f, 1), round(f + margin, 1)))

    return intervals


# ---------------------------------------------------------------------------
# F&B-Specific Features
# ---------------------------------------------------------------------------

def detect_seasonality(values, max_period=52):
    """Auto-detect seasonal period using autocorrelation."""
    n = len(values)
    if n < 24:
        return None

    mean = sum(values) / n
    var = sum((v - mean)**2 for v in values) / n
    if var == 0:
        return None

    best_period = None
    best_corr = 0

    for period in range(4, min(max_period, n // 2)):
        corr = sum((values[i] - mean) * (values[i + period] - mean)
                   for i in range(n - period)) / ((n - period) * var)
        if corr > best_corr and corr > 0.3:  # Minimum correlation threshold
            best_corr = corr
            best_period = period

    return best_period


def adjust_for_promotions(values, promo_flags, lift_estimate=0.15):
    """Remove promotion lift from historical data to get baseline demand."""
    adjusted = []
    for v, promo in zip(values, promo_flags):
        if promo:
            adjusted.append(v / (1 + lift_estimate))
        else:
            adjusted.append(v)
    return adjusted


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='F&B Demand Forecasting Engine')
    parser.add_argument('--file', required=True, help='CSV file with time series data')
    parser.add_argument('--periods', type=int, default=6, help='Number of periods to forecast')
    parser.add_argument('--method', choices=['sma', 'wma', 'ema', 'holt', 'holtwinters'],
                        default='ema', help='Forecasting method')
    parser.add_argument('--seasonal-period', type=int, default=None,
                        help='Seasonal period (auto-detected if not specified)')
    parser.add_argument('--alpha', type=float, default=0.3, help='Smoothing parameter')
    parser.add_argument('--sku', default=None, help='Filter to specific SKU')
    parser.add_argument('--output', default='forecast.json', help='Output file')
    parser.add_argument('--confidence', type=float, default=0.95, help='Confidence level')

    args = parser.parse_args()

    # Load data
    rows, date_col, value_col, sku_col = load_time_series(args.file)
    if not date_col or not value_col:
        print("Error: Could not detect date and value columns", file=sys.stderr)
        sys.exit(1)

    print(f"Detected: date={date_col}, value={value_col}, sku={sku_col}")

    # Get unique SKUs
    if sku_col and not args.sku:
        skus = sorted(set(r.get(sku_col, '') for r in rows))
        print(f"Found {len(skus)} SKUs. Forecasting all.")
    elif args.sku:
        skus = [args.sku]
    else:
        skus = [None]

    results = {}
    for sku in skus:
        series = parse_series(rows, date_col, value_col, sku_col, sku)
        if not series:
            continue

        values = [v for _, v in series]
        dates = [d for d, _ in series]
        label = sku or 'all'

        # Auto-detect seasonality
        sp = args.seasonal_period or detect_seasonality(values)
        if sp:
            print(f"  {label}: detected seasonal period = {sp}")

        # Generate forecast
        if args.method == 'sma':
            window = min(6, len(values))
            base = simple_moving_average(values, window)
            forecast = [base] * args.periods
        elif args.method == 'wma':
            base = weighted_moving_average(values[-12:])
            forecast = [base] * args.periods
        elif args.method == 'ema':
            base = exponential_moving_average(values, args.alpha)
            forecast = [base] * args.periods
        elif args.method == 'holt':
            forecast = double_exponential_smoothing(values, args.alpha, periods=args.periods)
        elif args.method == 'holtwinters':
            if sp and sp >= 4:
                forecast = holt_winters(values, seasonal_period=sp, periods=args.periods)
            else:
                forecast = double_exponential_smoothing(values, args.alpha, periods=args.periods)

        # Ensure no negative forecasts (demand can't be negative)
        forecast = [max(0, f) for f in forecast]

        # Backtest: use last 20% of data as holdout
        holdout_n = max(1, len(values) // 5)
        train = values[:-holdout_n]
        holdout = values[-holdout_n:]

        if args.method == 'holtwinters' and sp and sp >= 4 and len(train) >= sp * 2:
            backtest = holt_winters(train, seasonal_period=sp, periods=holdout_n)
        elif args.method == 'holt':
            backtest = double_exponential_smoothing(train, periods=holdout_n)
        else:
            base = exponential_moving_average(train, args.alpha)
            backtest = [base] * holdout_n

        accuracy = calculate_accuracy(holdout, backtest)
        errors = [holdout[i] - backtest[i] for i in range(min(len(holdout), len(backtest)))]
        ci = confidence_intervals(forecast, errors, args.confidence)

        # Decomposition
        decomp = None
        if sp and len(values) >= sp:
            decomp = seasonal_decomposition(values, sp)
            # Summarize seasonal indices
            decomp_summary = {
                'seasonal_period': sp,
                'peak_season_index': max(range(sp), key=lambda i: decomp['seasonal'][i]),
                'trough_season_index': min(range(sp), key=lambda i: decomp['seasonal'][i]),
            }
        else:
            decomp_summary = None

        # Generate forecast dates
        if len(dates) >= 2:
            interval = dates[-1] - dates[-2]
        else:
            interval = timedelta(days=30)

        forecast_dates = [(dates[-1] + interval * (i + 1)).strftime('%Y-%m-%d')
                          for i in range(args.periods)]

        results[label] = {
            'method': args.method,
            'n_historical': len(values),
            'historical_mean': round(sum(values) / len(values), 1),
            'historical_std': round((sum((v - sum(values)/len(values))**2 for v in values) / max(len(values)-1, 1))**0.5, 1),
            'forecast': [{'date': d, 'value': round(f, 1), 'lower': ci[i][0], 'upper': ci[i][2]}
                         for i, (d, f) in enumerate(zip(forecast_dates, forecast))],
            'accuracy': accuracy,
            'seasonality': decomp_summary,
        }

        print(f"  {label}: forecast next {args.periods} periods, MAPE={accuracy.get('mape', 'N/A')}%")

    # Write output
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nForecast saved to {args.output}")


if __name__ == '__main__':
    main()
