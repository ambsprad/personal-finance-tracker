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
        have_income = input("Do you have income to add? Y for Yes N for No. ").strip().upper()

        if have_income == "Y":
            new_transaction = {
                'type': "income",
                'amount': float(input("Enter income amount: ")),
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



def main():
    transactions = []
    while True:
        display_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nAdd Income Selected")
            add_income(transactions)
        
        elif choice == "2":
            print("\nAdd Expense Selected")

        elif choice == "3":
            print("\nView Transactions Selected")

        elif choice == "4":
            print("\nView Balance Selected")

        elif choice == "5":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid option")


if __name__ == "__main__":
    main()
