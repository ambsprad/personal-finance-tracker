def display_menu():
    print("\n" + "=" * 40)
    print(" Personal Finance Tracker")
    print("=" * 40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Exit")


def main():
    while True:
        display_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            print("\nAdd Income Selected")
        
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
