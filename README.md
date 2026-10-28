# Project 8: Online Shopping Transaction Analysis System

An intermediate-level Python and MySQL project that analyzes order-level activity in an online store. It reports order composition, order values, payment methods, order status, daily/monthly order volume, and product units sold.

## Features

- MySQL schema for `products`, `orders`, and `order_items`.
- Order totals calculated from `quantity * unit_price` in order items, not stored as a manually maintained order total.
- Pandas aggregation and NumPy statistics.
- Matplotlib charts for payment methods, order status, monthly order volume, and product quantities.
- CSV report exports and a sample CSV data source that runs without MySQL.
- Automated tests for sales-status treatment and monthly order counts.

## Order status and sales policy

- **Delivered:** included in delivered sales and average delivered order value.
- **Cancelled:** excluded from delivered sales; still visible in total order count and status reports.
- **Refunded:** excluded from delivered sales and average delivered order value; shown separately in status reports.
- **Pending, Processing, Shipped:** included in order volume and gross order value, but not counted as delivered sales.
- `gross_order_value` is the sum of all order totals regardless of status, so it is not the same as recognized/delivered sales.
- Product units-sold charts include delivered orders only. The raw transaction and daily/monthly order-volume reports retain all statuses.

This is a transaction-level analysis project. It intentionally does not implement customer segmentation or an executive KPI dashboard.

## Requirements

- Python 3.10 or newer
- Optional: MySQL Server 8.0 or newer for database mode
- Git for version control and GitHub upload

## Quick start (CSV mode — no MySQL needed)

### Windows PowerShell

```powershell
cd online-shopping-transaction-analysis
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
cd online-shopping-transaction-analysis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The default source is the included sample CSV data. Generated CSV reports and PNG charts appear in `reports/`.

## MySQL setup (optional)

1. Start MySQL Server.
2. Open a MySQL client and run the schema and sample inserts:

   ```bash
   mysql -u root -p < database/schema.sql
   mysql -u root -p online_shopping < database/seed.sql
   ```

3. Copy `.env.example` to `.env` and update the connection values. Do not commit `.env` or share its password.

   Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```

   macOS / Linux:
   ```bash
   cp .env.example .env
   ```

4. Run the database-backed analysis:

   ```bash
   python app.py --source mysql
   ```

The database user must have permission to read the `online_shopping` tables. For local development, use a dedicated user instead of placing root credentials in `.env`.

## Run tests

```bash
python -m pytest -q
```

## Reports created

- `transaction_summary.csv`
- `order_status_report.csv`
- `payment_method_report.csv`
- `daily_order_volume.csv`
- `monthly_order_volume.csv`
- `product_quantity_report.csv`
- `payment_method.png`
- `monthly_order_volume.png`
- `product_quantity.png`
- `order_status.png`

## Git and GitHub

1. Create a new, empty GitHub repository named `online-shopping-transaction-analysis` (do not initialize it with a README if you already have this project README).
2. In the project directory:

   ```bash
   git init
   git add .
   git commit -m "Build online shopping transaction analysis system"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/online-shopping-transaction-analysis.git
   git push -u origin main
   ```

3. Replace `YOUR-USERNAME` with your GitHub username. If Git reports that `origin` already exists, use `git remote set-url origin https://github.com/YOUR-USERNAME/online-shopping-transaction-analysis.git`.
4. Authenticate when Git prompts you (GitHub CLI or a browser-based credential manager is recommended). Do not put a password or token in the remote URL.

## Troubleshooting

- `python` is not recognized on Windows: install Python and enable “Add Python to PATH”, then reopen the terminal.
- PowerShell activation blocked: use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for the current terminal, then activate again.
- MySQL connection error: verify the server is running and `.env` host, port, username, password, and database name are correct.
- Module not found: activate the virtual environment and run `pip install -r requirements.txt`.
