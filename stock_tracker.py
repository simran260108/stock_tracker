# stock_tracker.py
import csv
import sys

STOCK_PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 120.0,
    "MSFT": 300.0,
    "AMZN": 140.0
}

def get_user_portfolio():
    print("Enter your stocks and quantities one per line (e.g. AAPL 2).")
    print("Press Enter on an empty line when done.\n")

    portfolio = {}
    while True:
        line = input("> ").strip()
        if line == "":
            break
        parts = line.split()
        if len(parts) != 2:
            print("Invalid input. Use format: SYMBOL QUANTITY  (e.g. AAPL 2)")
            continue
        symbol, qty_str = parts[0].upper(), parts[1]
        try:
            qty = int(qty_str)
            if qty < 0:
                print("Quantity cannot be negative.")
                continue
        except ValueError:
            print("Quantity must be an integer.")
            continue
        portfolio[symbol] = portfolio.get(symbol, 0) + qty
    return portfolio

def calculate_investment(portfolio, prices):
    rows = []
    grand_total = 0.0
    for symbol, qty in portfolio.items():
        price = prices.get(symbol)
        if price is None:
            rows.append({
                "symbol": symbol,
                "quantity": qty,
                "price": None,
                "total": None
            })
            continue
        total = price * qty
        grand_total += total
        rows.append({
            "symbol": symbol,
            "quantity": qty,
            "price": price,
            "total": total
        })
    return rows, grand_total

def print_report(rows, grand_total):
    print("\nPortfolio Report:")
    print(f"{'Symbol':<8} {'Qty':>5} {'Price':>10} {'Total':>12}")
    print("-" * 40)
    for r in rows:
        if r["price"] is None:
            print(f"{r['symbol']:<8} {r['quantity']:>5} {'N/A':>10} {'N/A':>12}")
        else:
            print(f"{r['symbol']:<8} {r['quantity']:>5} {r['price']:>10.2f} {r['total']:>12.2f}")
    print("-" * 40)
    print(f"{'TOTAL INVESTMENT':<8} {'':>5} {'':>10} {grand_total:>12.2f}\n")

def save_to_csv(rows, grand_total, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Quantity", "Price", "Total"])
        for r in rows:
            writer.writerow([
                r["symbol"],
                r["quantity"],
                "" if r["price"] is None else f"{r['price']:.2f}",
                "" if r["total"] is None else f"{r['total']:.2f}"
            ])
        writer.writerow([])
        writer.writerow(["", "", "Grand Total", f"{grand_total:.2f}"])
    print(f"Saved portfolio to '{filename}'.")

def main():
    print("=== Simple Stock Portfolio Tracker ===")
    print("Known stocks:", ", ".join(f"{k}({v})" for k,v in STOCK_PRICES.items()))
    portfolio = get_user_portfolio()
    if not portfolio:
        print("No stocks entered. Exiting.")
        return

    rows, grand_total = calculate_investment(portfolio, STOCK_PRICES)
    print_report(rows, grand_total)

    while True:
        ans = input("Save report to CSV file? (y/n): ").strip().lower()
        if ans in ("y", "n"):
            break
    if ans == "y":
        filename = input("Enter filename (default: portfolio.csv): ").strip()
        if filename == "":
            filename = "portfolio.csv"
        save_to_csv(rows, grand_total, filename)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        print("\nInterrupted. Bye.")
        sys.exit(0)
