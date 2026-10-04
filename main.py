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
            income_amount = get_valid_amount()
            income_date = get_valid_date()
            income_description = get_description()

            new_transaction = {
                'type': "income",
                'amount': income_amount,
                'date': income_date,
                'description': income_description,
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
            expense_amount = get_valid_amount()
            expense_date = get_valid_date()
            expense_description = get_description()

            new_transaction = {
                'type': "expense",
                'amount': expense_amount,
                'date': expense_date,
                'description': expense_description
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


def view_transactions(transactions, transaction_type="all"):
    income_transactions = []
    expense_transactions = []

    if transactions:
        for transaction in transactions:
            if transaction["type"] == "income":
                income_transactions.append(transaction)
            elif transaction["type"] == "expense":
                expense_transactions.append(transaction)

        if transaction_type == "all" or transaction_type == "income":
            if income_transactions:
                print("\nIncome\n" + "-"*10)
            
                for income_trans in income_transactions:
                    print(
                        f"\nIncome Amount: ${income_trans['amount']:.2f}"
                        f"\nDate Received: {income_trans['date']}" 
                        f"\nDescription: {income_trans['description']}"
                    )
            else:
                print("\nThere are no income transactions to view at this time.\n")

        if transaction_type == "all" or transaction_type == "expense":   
            if expense_transactions:
                print("\nExpenses")
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

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter the amount: $"))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
    return amount

def get_valid_date():
    while True:
        date_text = input("Enter the date of the transaction (MM-DD-YYYY): ")
        valid_date = validate_date(date_text)

        if valid_date is None:
            print("Please enter a valid date.")
            continue
        break
    return date_text


def get_description():
    while True:
        description = input("Enter a description for the transaction: ").strip()

        if description == "":
            blank_desc = input("Your description is blank.  Do you want to leave it blank? Y for yes N for no.  ").strip().upper()
            if blank_desc == "Y":
                break
            elif blank_desc == "N":
                continue
            else:
                print("Invalid response.")
                continue

        break

    return description


def transaction_menu(transactions):
    while True:
        print("\n" + "=" * 40)
        print(" View Transactions ")
        print("=" * 40)
        print("1. View All Transactions ")
        print("2. View Income Only ")
        print("3. View Expense Only ")
        print("4. Return to Main Menu ")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_transactions(transactions)
        elif choice == "2":
            view_transactions(transactions, "income")
        elif choice == "3":
            view_transactions(transactions, "expense")
        elif choice == "4":
            print("\nReturning to main menu.")
            break
        else:
            print("\nInvalid option.  Please choose again.")



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
            transaction_menu(transactions)

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
