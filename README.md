# Python Pipeline Practice

This repo contains a beginner-friendly ETL-style Python pipeline you can practice with.

## What it does

- **Extract**: reads sales rows from a CSV file (or built-in sample data).
- **Transform**: computes `line_total` and each customer's `customer_total`.
- **Load**: writes transformed rows to an output CSV.

## Run

```bash
python3 pipeline_practice.py
```

Optional input/output:

```bash
python3 pipeline_practice.py --input sample_sales.csv --output cleaned_sales.csv
```

The default output file is `pipeline_output.csv`.
