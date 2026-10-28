"""Online Shopping Transaction Analysis System command-line application."""
import argparse
from pathlib import Path
import pandas as pd
from src.analysis import (build_summary, prepare_transactions, status_report,
                          payment_report, monthly_order_volume, daily_order_volume,
                          product_quantity_report)
from src.data_loader import load_sample_transactions
from src.visualizations import create_charts

ROOT = Path(__file__).resolve().parent


def load_data(source: str):
    if source == "csv":
        transactions = load_sample_transactions()
        items_path = ROOT / "data" / "sample_order_items.csv"
        items = pd.read_csv(items_path, parse_dates=["order_date"])
        return transactions, items
    from src.db import load_transactions, load_item_details
    return load_transactions(), load_item_details()


def main():
    parser = argparse.ArgumentParser(description="Analyze online shopping transactions.")
    parser.add_argument("--source", choices=["csv", "mysql"], default="csv",
                        help="Use included sample CSV data (default) or query MySQL")
    args = parser.parse_args()

    try:
        transactions, items = load_data(args.source)
        tx = prepare_transactions(transactions)
    except Exception as exc:
        raise SystemExit(f"Could not load data: {exc}") from exc

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    summary = build_summary(tx)
    print("\n=== ONLINE SHOPPING TRANSACTION SUMMARY ===")
    for key, value in summary.items():
        if "value" in key or "sales" in key:
            print(f"{key.replace('_', ' ').title():32s}: ₹{value:,.2f}")
        else:
            print(f"{key.replace('_', ' ').title():32s}: {value:,}")

    reports = {
        "transaction_summary.csv": tx,
        "order_status_report.csv": status_report(tx),
        "payment_method_report.csv": payment_report(tx),
        "daily_order_volume.csv": daily_order_volume(tx),
        "monthly_order_volume.csv": monthly_order_volume(tx),
        "product_quantity_report.csv": product_quantity_report(items),
    }
    for filename, frame in reports.items():
        frame.to_csv(reports_dir / filename, index=False)
        print(f"Saved {filename}")

    charts = create_charts(tx, items, reports_dir)
    for chart in charts:
        print(f"Saved chart: {chart.relative_to(ROOT)}")
    print("\nDone. Open the reports/ folder to view generated CSV reports and PNG charts.")


if __name__ == "__main__":
    main()
