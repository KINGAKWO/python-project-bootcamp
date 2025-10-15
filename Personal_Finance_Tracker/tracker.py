import csv
import os
import json
import re
from datetime import datetime
from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt

DATA_FILE = "Personal_Finance_Tracker/finance_data.json"
EXPORT_DIR = "exports"


def load_transactions(filename=DATA_FILE):
    """load transactions from JSON file"""
    if not os.path.exists(filename):
        print("No saved data found - starting fresh")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: file is corrupted or invalid JSON.")
        return []


def save_transactions(transactions, filename=DATA_FILE):
    """Save all transactions to the JSON file."""
    # Ensure the directory exists before writing
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)


def print_menu():
    """Display the main menu options."""
    print("\nPersonal Finance Tracker")
    print("-" * 30)
    print("1. Add transaction")
    print("2. View transactions")
    print("3. Show summary")
    print("4. Search transactions")
    print("5. Monthly Summary")
    print("6. Visualize finances")
    print("7. Export to CSV")
    print("8. Export to JSON")
    print("9. Exit")
    print("-" * 30)


def add_transaction(transactions):
    """Add a new income or expense entry."""

    print("Add transaction!")
    print("1. income")
    print("2. expense")
    choice = input("Enter your choice: ").strip().lower()
    if choice not in {"income", "expense", "1", "2"}:
        print("Invalid choice. Please enter 'income', 'expense', 1, or 2.")
        return

    if choice in {"income", "1"}:
        choice = "income"
        print("Add income!")

    if choice in {"expense", "2"}:
        choice = "expense"
        print("Add expense!")

    description = str(input("Description: ").strip())
    if not description:
        print("Description can't be empty")
        return

    try:
        amount = float(input("Enter Amount: ").strip())
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")
    except ValueError as e:
        print(f"invalid input {e}")
        return

    # Three different variables depending on type
    income_amount = amount if choice == "income" else 0
    expense_amount = amount if choice == "expense" else 0
    net_amount = income_amount - expense_amount

    while True:
        date_input = input("Date (DD-MM-YYYY) [press enter for today]: ").strip()
        if not date_input:
            date_input = datetime.now().strftime("%d-%m-%Y")
            break
        try:
            transaction_date = datetime.strptime(date_input, "%d-%m-%Y")
            if transaction_date > datetime.now():
                print("Date cannot be in the future. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")
            return

    transaction = {
        "type": choice,
        "description": description,
        "income_amount": income_amount,
        "expense_amount": expense_amount,
        "net_amount": net_amount,
        "date": date_input
    }
    transactions.append(transaction)
    save_transactions(transactions)

    print("Transaction added successfully!")
    print(f"Transaction added:{description} ({choice}) — {amount:.2f}xaf on {date_input}")


def view_transactions(transactions):
    """Display all transactions in a formatted table with totals."""
    print("\n Transaction History")
    print("_" * 50)

    if not transactions:
        print("No transactions recorded yet. ")
        return

    total_income = 0
    total_expense = 0

    # table header
    print(f"{'Date':<12} | {'Type':<8} | {'Description':<20} | {'Amount':>10}")
    print("-" * 50)

    for transaction in sorted(transactions, key=lambda x: x['date']):
        income_amount = transaction.get("income_amount", 0)
        expense_amount = transaction.get("expense_amount", 0)
        # Show the actual transaction amount, not running net balance
        amount = income_amount if income_amount else -expense_amount

        total_income += income_amount
        total_expense += expense_amount

        print(f"{transaction['date']:<12} | {transaction['type']:<8} | {transaction['description']:<20} | {amount:>9.2f}xaf")

    # totals
    print("-" * 50)
    print(f"{'Total Income':<30}  {total_income:>9.2f}xaf")
    print(f"{'Total Expense':<30}  {total_expense:>9.2f}xaf")
    print(f"{'Net Balance':<30}  {(total_income - total_expense):>9.2f}xaf")


def show_summary(transactions):
    """Display summary of income, expenses,
    and balance """
    print("\n financial summary")
    print("_" * 40)

    if not transactions:
        print("No transactions found. Add some first")
        return

    total_income = sum(transaction["income_amount"] for transaction in
                       transactions if transaction["type"] == "income")
    total_expense = sum(transaction["expense_amount"] for transaction in
                        transactions if transaction["type"] == "expense")
    net_balance = total_income - total_expense

    num_expenses = sum(1 for transaction in transactions if transaction["type"]
                       == "expense")
    avg_expense = total_expense / num_expenses if num_expenses > 0 else 0

    # Display
    print(f"{'Total Income:':<20} {total_income:>10.2f}xaf")
    print(f"{'Total Expense:':<20} {total_expense:>10.2f}xaf")
    print(f"{'Net Balance:':<20} {net_balance:>10.2f}xaf")
    print(f"{'Avg Expense:':<20} {avg_expense:>10.2f}xaf")

    if net_balance > 0:
        print("\n you're in profit. Great job managing your money!")
    elif net_balance < 0:
        print("\n you're spending more than you're earning. Review your expenses.")
    else:
        print("\n Balanced - break even this period")


def search_transactions(transactions):
    """search or filter transactions by keyword, or date range"""
    if not transactions:
        print("No transactions to search")
        return

    print("\n search options:")
    print("1. Search by keyword")
    print("2. filter by date range")
    print("3. filter by type (income/expense)")
    print("4. Back to main menu")

    choice = input("choose an option: ").strip()
    results = []

    if choice == "1":
        keyword = input("Enter keyword: ").lower()
        if not keyword:
            print("keyword cannot be empty. ")
            return
        results = [transaction for transaction in transactions
                   if keyword in transaction["description"].lower()]

    elif choice == "2":
        try:
            start_date_str = input("Enter start date (DD-MM-YYYY): ").strip()
            end_date_str = input("Enter end date (DD-MM-YYYY): ").strip()

            start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

            if start_date > end_date:
                print("start date cannot be after end date")
                return

            results = [
                transaction for transaction in transactions
                if start_date <= datetime.strptime(transaction["date"], "%d-%m-%Y") <= end_date
            ]
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")
            return

    elif choice == "3":
        transaction_type = input("Enter type (income/expense): ").strip().lower()
        if transaction_type in ("income", "1"):
            results = [transaction for transaction in transactions if
                       transaction["type"] == "income"]
        elif transaction_type in ("expense", "2"):
            results = [transaction for transaction in transactions if
                       transaction["type"] == "expense"]
        else:
            print("Invalid type. Please enter 'income' or 'expense'.")
            return

    elif choice == "4":
        return

    else:
        print("Invalid choice. Please enter 1-4.")
        return

    # Display results
    if results:
        print("\nSearch Results")
        print("-" * 50)
        print(f"{'Date':<12} | {'Type':<8} | {'Description':<20} | {'Amount':>10}")
        print("-" * 50)
        for transaction in results:
            income_amount = transaction.get("income_amount", 0)
            expense_amount = transaction.get("expense_amount", 0)
            amount = income_amount if income_amount else -expense_amount
            print(f"{transaction['date']:<12} | {transaction['type']:<8} | {transaction['description']:<20} | {amount:>9.2f}xaf")
        print("-" * 50)
        print(f"Total matches: {len(results)}")
    else:
        print("No matching transactions found.")


def monthly_summary(transactions):
    """
    Summarize all transactions for a given month (YYYY-MM).
    Shows income, expenses, savings rate, and top categories by frequency.
    Args:
        transactions (list): List of transaction dictionaries.
    """
    #  Validate format and allow re-entry
    while True:
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            target_month = datetime.strptime(month, "%Y-%m")
            break
        except ValueError:
            print("Invalid format. Please use YYYY-MM (e.g., 2025-10).")

    #  Use datetime for filtering
    monthly_transactions = []
    for transaction in transactions:
        try:
            tx_date = datetime.strptime(transaction.get("date", ""), "%d-%m-%Y")
            if tx_date.year == target_month.year and tx_date.month == target_month.month:
                monthly_transactions.append(transaction)
        except ValueError:
            continue  # skip malformed or missing dates

    if not monthly_transactions:
        print("No transactions found for this month.")
        return

    #  Use .get for safe access
    income = sum(t.get("income_amount", 0) for t in monthly_transactions if t.get("type") == "income")
    expense = sum(t.get("expense_amount", 0) for t in monthly_transactions if t.get("type") == "expense")
    balance = income - expense
    savings_rate = (balance / income * 100) if income > 0 else 0

    # *Use most_common to show frequency
    expense_desc = [t.get("description", "Unknown") for t in monthly_transactions if t.get("type") == "expense"]
    income_desc = [t.get("description", "Unknown") for t in monthly_transactions if t.get("type") == "income"]
    top_expense_categories = Counter(expense_desc).most_common(3)
    top_income_categories = Counter(income_desc).most_common(3)

    print("\nMonthly Summary")
    print("-" * 40)
    print(f"Month:         {month}")
    print(f" Total Income:  {income:>10.2f} xaf")
    print(f" Total Expense: {expense:>10.2f} xaf")
    print(f" Net Balance:   {balance:>10.2f} xaf")
    print(f" Savings Rate:  {savings_rate:>9.2f}%")
    print("-" * 40)

    print("\nTop Expense Categories (by frequency):")
    for category, count in top_expense_categories:
        print(f"• {category:<20} — {count} entries")

    print("\n Top Income Categories (by frequency):")
    for category, count in top_income_categories:
        print(f"• {category:<20} — {count} entries")


def summarize_by_month(transactions):
    """Aggregate income, expenses, and balance by month
    Returns a clean monthly summary table as a list of dictionaries
    """
    monthly_data = defaultdict(lambda: {"income": 0.0, "expenses": 0.0, "balance": 0.0})

    for transaction in transactions:
        try:
            transaction_date = datetime.strptime(transaction.get("date", ""), "%d-%m-%Y")
            month = transaction_date.strftime("%B %Y")

            if transaction.get("type") == "income":
                monthly_data[month]["income"] += transaction.get("income_amount", 0.0)
            elif transaction.get("type") == "expense":
                monthly_data[month]["expenses"] += transaction.get("expense_amount", 0.0)

        except (ValueError, KeyError):
            # Skip transactions with invalid dates or missing required fields
            continue

    for m in monthly_data:
        monthly_data[m]["balance"] = monthly_data[m]["income"] - monthly_data[m]["expenses"]

    # sort months chronologically
    months = sorted(set(monthly_data), key=lambda m: datetime.strptime(m, "%B %Y"))
    return months, monthly_data


def visualize_finances(transactions):
    """Create a bar chart showing income vs expenses by month."""
    if not transactions:
        print("No data available for visualization.")
        return

    months, monthly_data = summarize_by_month(transactions)

    if not months:
        print("No monthly data found after summarization. ")

    income_values = [monthly_data[m]["income"] for m in months]
    expense_values = [monthly_data[m]["expenses"] for m in months]

    x = range(len(months))
    plt.figure(figsize=(10, 6))
    plt.bar([i - 0.2 for i in x], income_values, width=0.4, label="Income", alpha=0.7, color="green")
    plt.bar([i + 0.2 for i in x], expense_values, width=0.4, label="Expenses", alpha=0.7, color="red")

    plt.xticks(x, months, rotation=45, ha="right")

    plt.title("Monthly Income vs Expenses", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Amount (FCFA)")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("finance_chart.png")
    print(f" Chart exported as {os.path.abspath('finance_chart.png')}")
    plt.show()


# exporting reports
def safe_filename(filename):
    # Only allow alphanumeric, dash, underscore, and dot
    filename = re.sub(r'[^A-Za-z0-9._-]', '_', filename)
    # Prevent path traversal
    if '..' in filename or filename.startswith(('/', '\\')):
        raise ValueError("Invalid filename.")
    return filename


def export_to_csv(transactions, filename="finance_report.csv"):
    """
    Export transaction to a csv file

    Args:
        transactions (_type_): _description_
        filename (str, optional): _description_. Defaults to "finance_report.csv".
    """
    if not transactions:
        print("No transactions to export")
        return
    fieldnames = ["date", "type", "income_amount", "expense_amount", "net_amount", "description"]

    # Sanitize filename and restrict to EXPORT_DIR
    filename = safe_filename(filename)
    export_path = os.path.join(EXPORT_DIR, filename)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    try:
        with open(export_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        print(f"Transactions successfully exported to {os.path.abspath(export_path)}")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def export_to_json(transactions, filename="finance_data.json"):
    """
    Export transactions to a JSON file

    Args:
        transactions (_type_): _description_
        filename (str, optional): _description_. Defaults to "finance_data.json".
    """
    if not transactions:
        print("No transactions to export.")
        return

    # Sanitize filename and restrict to EXPORT_DIR
    filename = safe_filename(filename)
    export_path = os.path.join(EXPORT_DIR, filename)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)

    print(f"Transactions successfully exported to {os.path.abspath(export_path)}")


# -----------------------------
#  Main Program Loop
# -----------------------------

def main():
    """Main control loop for the finance tracker."""
    transactions = load_transactions()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            show_summary(transactions)
        elif choice == "4":
            search_transactions(transactions)
        elif choice == "5":
            monthly_summary(transactions)
        elif choice == "6":
            visualize_finances(transactions)
        elif choice == "7":
            export_to_csv(transactions)
        elif choice == "8":
            export_to_json(transactions)
        elif choice == "9":
            save_transactions(transactions)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1–9.")


if __name__ == "__main__":
    main()
