#!/usr/bin/env python3
"""A small ETL-style pipeline you can practice and extend.

Usage:
    python pipeline_practice.py
    python pipeline_practice.py --input sample_sales.csv --output cleaned_sales.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

Row = dict[str, str | int | float]


def extract(input_path: Path | None) -> list[Row]:
    """Load source data from CSV, or create a demo dataset if no input is given."""
    if input_path is None:
        return [
            {"order_id": 1001, "customer": "Ava", "product": "Book", "quantity": 2, "unit_price": 12.0},
            {"order_id": 1002, "customer": "Ben", "product": "Pen", "quantity": 10, "unit_price": 1.5},
            {"order_id": 1003, "customer": "Ava", "product": "Book", "quantity": 1, "unit_price": 12.0},
            {"order_id": 1004, "customer": "Chloe", "product": "Notebook", "quantity": 3, "unit_price": 6.0},
            {"order_id": 1005, "customer": "Ben", "product": "Pen", "quantity": 5, "unit_price": 1.5},
        ]

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: list[Row] = []
        for row in reader:
            rows.append(
                {
                    "order_id": int(row.get("order_id", 0) or 0),
                    "customer": row.get("customer", ""),
                    "product": row.get("product", ""),
                    "quantity": int(row.get("quantity", 0) or 0),
                    "unit_price": float(row.get("unit_price", 0.0) or 0.0),
                }
            )
        return rows


def transform(rows: Iterable[Row]) -> list[Row]:
    """Clean and enrich data with computed fields and summary columns."""
    transformed: list[Row] = []
    customer_totals: dict[str, float] = {}

    for row in rows:
        quantity = int(row.get("quantity", 0) or 0)
        unit_price = float(row.get("unit_price", 0.0) or 0.0)
        line_total = quantity * unit_price

        clean_row: Row = {
            "order_id": int(row.get("order_id", 0) or 0),
            "customer": str(row.get("customer", "")),
            "product": str(row.get("product", "")),
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": round(line_total, 2),
        }
        transformed.append(clean_row)

        customer = clean_row["customer"]
        customer_totals[str(customer)] = customer_totals.get(str(customer), 0.0) + line_total

    for row in transformed:
        row["customer_total"] = round(customer_totals[str(row["customer"])], 2)

    return transformed


def load(rows: list[Row], output_path: Path) -> None:
    """Write transformed data to CSV."""
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_pipeline(input_path: Path | None, output_path: Path) -> list[Row]:
    raw = extract(input_path)
    cleaned = transform(raw)
    load(cleaned, output_path)
    return cleaned


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Practice ETL-style pipeline in Python")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Optional input CSV path. If omitted, a demo dataset is used.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("pipeline_output.csv"),
        help="Output CSV path for transformed data.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_pipeline(args.input, args.output)
    print(f"Processed {len(result)} rows -> {args.output}")


if __name__ == "__main__":
    main()
