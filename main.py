import json
from datetime import datetime

def display_menu():
    print("\n" + "=" * 40)
    print(" Personal Finance Tracker")
    print("=" * 40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Exit")


def add_income(transactions, filename="transactions.json"):

    while True:
        have_income = input("Do you have income to add? Y for Yes, N for No. ").strip().upper()

        if have_income == "Y":
            while True:
                try:
                    amount = float(input("Enter income amount: $"))

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue

                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
            while True:
                date_text = input("Enter date of income (MM-DD-YYYY): ")
                valid_date = validate_date(date_text)

                if valid_date is None:
                    print("Please enter a valid date.")
                    continue
                break

            new_transaction = {
                'type': "income",
                'amount': amount,
                'date': date_text,
                'description': input("Enter description of income: ")
                }
            transactions.append(new_transaction)
            save_transactions(transactions, filename)

        elif have_income == "N":
            if transactions:
                print("You added the following income transactions: ")
                for transaction in transactions:
                    if transaction["type"] == "income":
                        print(
                            f"\nIncome Amount: ${transaction['amount']:.2f}"
                            f"\nDate Received: {transaction['date']}" 
                            f"\nDescription: {transaction['description']}"
                        )         
            else:
                print("You did not add any income transactions.")
                print("Returning to main menu.")

            break

        else:
            print("You entered an invalid response. Please enter Y or N for your response.")


def add_expense(transactions, filename="transactions.json"):
    while True:
        have_expense = input("Do you have expenses to add? Y for yes, N for No.  ").strip().upper()

        if have_expense == "Y":
            while True:
                try:
                    amount = float(input("Enter the amount of the expense: $"))
                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue
                    break

                except ValueError:
                    print("Invalid amount. Please enter a valid number.")

            while True:
                date_text = input("Enter date of expense (MM-DD-YYYY): ")
                valid_date = validate_date(date_text)

                if valid_date is None:
                    print("Please enter a valid date.")
                    continue
                break

            new_transaction = {
                'type': "expense",
                'amount': amount,
                'date': date_text,
                'description': input("Enter a description for the expense.  ")
            }
            transactions.append(new_transaction)
            save_transactions(transactions, filename)
        elif have_expense == "N":
            if transactions: 
                print("You added the following expense transactions: ")
                for transaction in transactions:
                    if transaction["type"] == "expense":
                        print(
                            f"\nExpense Amount: ${transaction['amount']:.2f}"
                            f"\nDate Paid: {transaction['date']}" 
                            f"\nDescription: {transaction['description']}"
                        )         
            else:
                print("You did not add any expense transactions.")
                print("Returning to main menu.")

            break

        else:
            print("You entered an invalid response. Please enter Y or N for your response.")


def view_transactions(transactions):
    income_transactions = []
    expense_transactions = []

    if transactions:
        for transaction in transactions:
            if transaction["type"] == "income":
                income_transactions.append(transaction)
            elif transaction["type"] == "expense":
                expense_transactions.append(transaction)

        if income_transactions:
            print("Income\n" + "-"*10)
            
            for income_trans in income_transactions:
                print(
                    f"\nIncome Amount: ${income_trans['amount']:.2f}"
                    f"\nDate Received: {income_trans['date']}" 
                    f"\nDescription: {income_trans['description']}"
                )
        else:
            print("\nThere are no income transactions to view at this time.\n")
        
        if expense_transactions:
            print("Expenses")
            print("-"*10)

            for expense_trans in expense_transactions:
                print(
                    f"\nExpense Amount: ${expense_trans['amount']:.2f}"
                    f"\nDate Paid: {expense_trans['date']}" 
                    f"\nDescription: {expense_trans['description']}"
                )
        else: 
            print("There are no expenses at this time.")

    else:
        print("\nYou do not have any transactions to view.")


def view_balance(transactions):

    income_total, expense_total, balance = calculate_balance(transactions)

    print("\nBalance Summary" + "\n" + "-"*10)
    print(f"\nTotal Income: ${income_total:.2f}")
    print(f"\nTotal Expenses: ${expense_total:.2f}")
    print("\n" + "-"*10)
    print(f"\nBalance: ${balance:.2f}")

def calculate_balance(transactions):
    income_total = 0
    expense_total = 0

    for trans in transactions:
        if trans["type"] == "income":
            income_total += trans["amount"]
        elif trans["type"] == "expense":
            expense_total += trans["amount"]
    
    balance = income_total - expense_total

    return income_total, expense_total, balance

def save_transactions(transactions, filename="transactions.json"):
    with open(filename, "w") as file:
        json.dump(transactions, file, indent=4)

def load_transactions(filename="transactions.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("There was an error reading the current file.")
        return []

def validate_date(date_text):
    try:
        valid_date = datetime.strptime(date_text, "%m-%d-%Y")
        return valid_date
    except ValueError:
        return None

def main():
    transactions = load_transactions()
    while True:
        display_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            print("\nAdd Income Selected")
            add_income(transactions)
        
        elif choice == "2":
            print("\nAdd Expense Selected")
            add_expense(transactions)

        elif choice == "3":
            print("\nView Transactions Selected")
            view_transactions(transactions)

        elif choice == "4":
            print("\nView Balance Selected")
            view_balance(transactions)

        elif choice == "5":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid option")


if __name__ == "__main__":
    main()
