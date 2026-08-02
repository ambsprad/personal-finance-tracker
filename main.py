def display_menu():
    print("\n" + "=" * 40)
    print(" Personal Finance Tracker")
    print("=" * 40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Exit")


def add_income(transactions):

    while True:
        have_income = input("Do you have income to add? Y for Yes, N for No. ").strip().upper()

        if have_income == "Y":
            new_transaction = {
                'type': "income",
                'amount': float(input("Enter income amount: $")),
                'date': input("Enter date of income (MM-DD-YYYY): "),
                'description': input("Enter description of income: ")
                }
            transactions.append(new_transaction)

        elif have_income == "N":
            if transactions:
                print("You added the following income transactions: ")
                for transaction in transactions:
                    print(
                        f"\nIncome Amount: ${transaction["amount"]:.2f}"
                        f"\nDate Recevied: {transaction["date"]}" 
                        f"\nDescription: {transaction["description"]}"
                    )         

            else:
                print("You did not add any income transactions.")
                print("Returning to main menu.")

            break

        else:
            print("You entered an invalid response. Please enter Y or N for your response.")


def add_expense(transactions):
    while True:
        have_expense = input("Do yo have expenses to add? Y for yes, N for No.  ").strip().upper()

        if have_expense == "Y":
            new_transaction = {
                'type': "expense",
                'amount': float(input("Enter the amount of the expense. $")),
                'date': input("Enter the date of the expense (MM-DD-YY).  "),
                'description': input("Enter a description for the expense.  ")
            }
            transactions.append(new_transaction)
        elif have_expense == "N":
            if transactions: 
                print("You added the following expense transactions: ")
                for transaction in transactions:
                    if transaction["type"] == "expense":
                        print(
                            f"\nExpense Amount: ${transaction['amount']:.2f}"
                            f"\nDate Recevied: {transaction['date']}" 
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
                    f"\nDate Recevied: {income_trans['date']}" 
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
    income_total = 0
    expense_total = 0

    for trans in transactions:
        if trans["type"] == "income":
            income_total += trans["amount"]
        elif trans["type"] == "expense":
            expense_total += trans["amount"]
    
    balance = income_total - expense_total

    print("\nBalance Summary" + "\n" + "-"*10)
    print(f"\nTotal Income: ${income_total:.2f}")
    print(f"\nTotal Expenses: ${expense_total:.2f}")
    print("\n" + "-"*10)
    print(f"\nBalance: ${balance:.2f}")


def main():
    transactions = []
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
