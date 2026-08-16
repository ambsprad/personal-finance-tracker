Personal Finance Tracker

A command-line personal finance tracker built with Python. This project is part of my software development portfolio as I transition from retail management into software development.

Features
Add income transactions
Add expense transactions
Store transaction data using JSON
Load saved transactions when the application starts
View income and expense transactions
Calculate total income
Calculate total expenses
Calculate current balance
Handle missing transaction files
Handle invalid or corrupted JSON data
Validate menu responses
Technologies
Python 3
JSON
Git
GitHub
How It Works

The application uses a list of dictionaries to store financial transactions while the program is running. Each transaction contains:

Transaction type
Amount
Date
Description

Transactions are automatically saved to transactions.json when income or expenses are added. Previously saved transactions are loaded when the application starts.

Project Status

🚧 In Progress

This project is being developed as part of my software development portfolio while I transition from retail management into software development.

Planned Features
Automated testing with pytest
Improved input validation
Refactor duplicated code
Monthly financial reports
Additional transaction management features
How to Run

Clone the repository and run:
python3 main.py