# 💰 Personal Finance Tracker

A simple, Python-based personal finance tracker that helps users record and monitor their income and expenses locally.
Built as part of my Python Developer journey — Phase II (freeCodeCamp x Microsoft x IBM learning journey).

## 📋 Features

- **Add Transactions**: Easily add income or expense entries with descriptions, amounts, and dates.
- **View Transactions**: Display all transactions in a formatted table, sorted by date, with running totals.
- **Financial Summary**: Get an overview of total income, expenses, net balance, and average expenses.
- **Search & Filter**: Search by keyword, filter by date range or type (income/expense).
- **Monthly Summary**: Analyze income, expenses, savings rate, and top categories for a specific month.
- **Data Visualization**: Generate bar charts comparing monthly income vs. expenses using Matplotlib.
- **Export Options**: Export data to CSV or JSON for external analysis.
- **Persistent Storage**: Saves data to a JSON file for continuity across sessions.
- **Error Handling**: Gracefully handles invalid inputs, file errors, and corrupted data.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KINGAKWO/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. **Ensure Python is Installed**:
   - Requires Python 3.7 or higher. Download from [python.org](https://www.python.org/downloads/).

3. **Set Up Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

## 🚀 Usage

Run the application:
```bash
python tracker.py
```

### Example Interaction

```
Personal Finance Tracker
------------------------------
1. Add transaction
2. View transactions
3. Show summary
4. Search transactions
5. Monthly Summary
6. Visualize finances
7. Export to CSV
8. Export to JSON
9. Exit
------------------------------

Enter your choice: 1
Add transaction!
1. income
2. expense
Enter your choice: income
Add income!
Description: Freelance project
Enter Amount: 1500
Date (DD-MM-YYYY) [press enter for today]: 06-10-2025
Transaction added successfully!
Transaction added: Freelance project (income) — 1500.00xaf on 06-10-2025
```

### Viewing Transactions
Select option 2 to see a table like:
```
 Transaction History
__________________________________________________
Date         | Type     | Description         | Amount
--------------------------------------------------
06-10-2025   | income   | Freelance project   | 1500.00xaf
...
--------------------------------------------------
Total Income:                      1500.00xaf
Total Expense:                        0.00xaf
Net Balance:                      1500.00xaf
```

### Visualization
Option 6 generates a bar chart (saved as `finance_chart.png`) showing monthly income vs. expenses.

## 🧠 Tech & Concepts Used

- **Python Fundamentals**: Loops, conditionals, functions, and data structures (lists, dicts).
- **File Handling**: JSON I/O for data persistence.
- **Error Handling**: `try/except` for validation and robustness.
- **Libraries**: `matplotlib` for visualization, `csv` and `json` for exports.
- **Date Management**: `datetime` for parsing and validation.
- **Modular Design**: Clean, readable code with functions for each feature.

## 🔮 Future Enhancements

- Build a Flask web dashboard for financial insights and interactive charts.
- Add user authentication for secure, multi-user data access.
- Implement advanced data visualization (e.g., pie charts for expense categories).
- Integrate with APIs for automatic transaction imports (e.g., bank statements).
- Add budgeting features and alerts for overspending.

## 📸 Screenshots

- **Visualization Chart**: A bar chart comparing monthly income (green) and expenses (red), saved as `finance_chart.png` after running the visualize option.

## 🧑‍💻 Author

Akwo Makembe King  
Python Developer | AI & Data Enthusiast  
📍 GitHub: [KINGAKWO](https://github.com/KINGAKWO)  
💼 LinkedIn: [akwo-makembe-king](www.linkedin.com/in/akwo-makembe-king-108a28252)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you'd like to change.
