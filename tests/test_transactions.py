from main import calculate_balance, save_transactions, load_transactions

def test_calculate_balance():
    transactions = [
        {
            "type": "income",
            "amount": 2000.00,
            "date": "08-01-2026",
            "description": "Paycheck"
        },
        {
            "type": "expense",
            "amount": 750.00,
            "date": "08-02-2026",
            "description": "Rent"
        }
    ]

    income_total, expense_total, balance = calculate_balance(transactions)

    assert income_total == 2000.00
    assert expense_total == 750.00
    assert balance == 1250.00


def test_calculate_balance_income_only():
    transactions = [
        {
            "type": "income",
            "amount": 500.00,
            "date": "08-09-2026",
            "description": "pay"

        },
        {
            "type": "income",
            "amount": 500.00,
            "date": "08-10-2026",
            "description": "check"
        }
    ]

    income_total, expense_total, balance = calculate_balance(transactions)

    assert income_total == 1000.00
    assert expense_total == 0.0
    assert balance == 1000.00

def test_calculate_balance_expense_only():
    transactions = [
        {
            "type": "expense",
            "amount": 150.00,
            "date": "08-01-2026",
            "description": "wifi"
        },
        {
            "type": "expense",
            "amount": 50.00,
            "date": "08-05-2026",
            "description": "gas"
        }
    ]

    income_total, expense_total, balance = calculate_balance(transactions)

    assert income_total == 0
    assert expense_total == 200
    assert balance == -200

def test_calculate_balance_empty():
    transactions = []

    income_total, expense_total, balance = calculate_balance(transactions)

    assert income_total == 0
    assert expense_total == 0
    assert balance == 0

def test_save_and_load_transactions(tmp_path):
    test_file = tmp_path / "test_transactions.json"
    transactions = [
        {
            "type": "income",
            "amount": 1789.65,
            "date": "08-01-2026",
            "description": "pay"
        },
        {
            "type": "income",
            "amount": 600.79,
            "date": "08-15-2026",
            "description": "reimbursement"
        },
        {
            "type": "expense",
            "amount": 980.00,
            "date": "08-03-2026",
            "description": "rent"
        }
    ]

    save_transactions(transactions, test_file)
    loaded_transactions = load_transactions(test_file)

    assert loaded_transactions == transactions

def test_load_transactions_file_not_found(tmp_path):
    missing_file = tmp_path / "missing_transactions.json"
    transactions = load_transactions(missing_file)

    assert transactions == []

def test_load_transactions_invalid_json(tmp_path):
    test_file = tmp_path / "test_file.json"

    with open(test_file, "w") as file:
        file.write("this is not valid JSON")
    
    transactions = load_transactions(test_file)

    assert transactions == []