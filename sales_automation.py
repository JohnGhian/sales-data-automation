import csv
from collections import defaultdict

INPUT_FILE = "sales_data.csv"
REPORT_FILE = "sales_report.csv"

def read_sales_data():
    sales = []

    with open(INPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                quantity = int(row["Quantity"])
                price = float(row["Price"])

                if quantity < 0 or price < 0:
                    continue
                
                sales.append({
                    "date": row["Date"],
                    "product": row["Product"],
                    "category": row["Category"],
                    "quantity": quantity,
                    "price": price,
                    "total": quantity * price
                })

            except ValueError:
                print("Skipped invalid record")

    return sales

def calculate_summary(sales):
    total_sales = sum(item["total"] for item in sales)
    total_quantity = sum(item["quantity"] for item in sales)
    product_sales = defaultdict(float)

    for item in sales:
        product_sales[item["product"]] += item["total"]

    best_product = max(
        product_sales, key=product_sales.get
    ) if product_sales else "None"

    return total_sales, total_quantity, best_product, product_sales

def display_report(sales):
    total_sales, total_quantity, best_product, product_sales = calculate_summary(sales)

    print("============================")
    print("            SALES REPORT")
    print("============================")

    print(f"Total sales: ₱ {total_sales:,.2f}")
    print(f"Total items sold: {total_quantity}")
    print(f"Best-selling product: {best_product}")

    print("\n===== SALES BY PRODUCT =====")

    for product, amount in sorted(product_sales.items(),
                                   key=lambda item: item[1], reverse=True):
        print(f"{product}: ₱ {amount:,.2f}") 

def save_report(sales):
    with open(REPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Product",
            "Category",
            "Quantity",
            "Price",
            "Total Sales"
        ])
        for item in sales:
            writer.writerow([
                item["date"],
                item["product"],
                item["category"],
                item["quantity"],
                item["price"],
                item["total"]
            ])

    print(f"\nReport saved to {REPORT_FILE}")

def main():
    print("===== SALES DATA AUTOMATION =====")

    sales = read_sales_data()

    if not sales:
        print("No valid sales data found.")
        return

    display_report(sales)
    save_report(sales)

    print("\nAutomation completed successfully!")

if __name__ == "__main__":
    main()
