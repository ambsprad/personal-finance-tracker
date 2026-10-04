from main import (
    calculate_balance, 
    save_transactions, 
    load_transactions,
    add_income,
    add_expense,
    validate_date,
    get_valid_amount,
    get_valid_date,
    get_description,
    transaction_menu,
)

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

def test_add_income(monkeypatch, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "1000.00",
        "08-01-2026",
        "Paycheck",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    add_income(transactions, test_file)

    assert len(transactions) == 1
    assert transactions[0]["type"] == "income"
    assert transactions[0]["amount"] == 1000.00
    assert transactions[0]["date"] == "08-01-2026"
    assert transactions[0]["description"] == "Paycheck"

def test_add_expense(monkeypatch, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "250.50",
        "08-05-2026",
        "Electric Bill",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    add_expense(transactions, test_file)

    assert len(transactions) == 1
    assert transactions[0]["type"] == "expense"
    assert transactions[0]["amount"] == 250.50
    assert transactions [0]["date"] == "08-05-2026"
    assert transactions[0]["description"] == "Electric Bill"

def test_add_income_invalid_response(monkeypatch, capsys):
    transactions = []
    user_inputs = iter([
        "X",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_income(transactions)
    
    captured = capsys.readouterr()

    assert transactions == []
    assert "You entered an invalid response" in captured.out

def test_add_expense_invalid_response(monkeypatch, capsys):
    transactions = []
    user_inputs = iter([
        "X",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_expense(transactions)

    captured = capsys.readouterr()

    assert transactions == []
    assert "You entered an invalid response" in captured.out

def test_add_income_invalid_amount(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "abc",
        "1000.00",
        "08-01-2026",
        "Paycheck",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_income(transactions, test_file)

    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "income"
    assert transactions[0]["amount"] == 1000.00
    assert transactions[0]["date"] == "08-01-2026"
    assert transactions[0]["description"] == "Paycheck"
    assert "Invalid amount" in captured.out

def test_add_expense_invalid_amount(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "abc",
        "250.50",
        "08-05-2026",
        "Electric Bill",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_expense(transactions, test_file)

    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "expense"
    assert transactions[0]["amount"] == 250.50
    assert transactions[0]["date"] == "08-05-2026"
    assert transactions[0]["description"] == "Electric Bill"
    assert "Invalid amount" in captured.out

def test_add_income_non_positive_amount(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "-50",
        "0",
        "500",
        "09-13-2026",
        "Paycheck",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_income(transactions, test_file)
    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "income"
    assert transactions[0]["amount"] == 500
    assert "Amount must be greater than 0." in captured.out

def test_add_expense_non_positive_amount(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "abc",
        "-25",
        "0",
        "250.50",
        "09-13-2026",
        "Electric Bill",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_expense(transactions, test_file)
    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "expense"
    assert transactions[0]["amount"] == 250.50
    assert "Amount must be greater than 0." in captured.out

def test_validate_date_valid():
    result = validate_date("09-13-2026")

    assert result is not None
    assert result.year == 2026
    assert result.month == 9
    assert result.day == 13

def test_validate_date_invalid_date():
    result = validate_date("02-30-2026")

    assert result is None

def test_validate_date_invalid_format():
    result = validate_date("abc")

    assert result is None

def test_add_income_invalid_date(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "500",
        "02-30-2026",
        "abc",
        "09-13-2026",
        "Paycheck",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_income(transactions, test_file)
    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "income"
    assert transactions[0]["amount"] == 500
    assert transactions[0]["date"] == "09-13-2026"
    assert transactions[0]["description"] == "Paycheck"
    assert "Please enter a valid date" in captured.out

def test_add_expense_invalid_date(monkeypatch, capsys, tmp_path):
    transactions = []
    test_file = tmp_path / "test_transactions.json"

    user_inputs = iter([
        "Y",
        "250.50",
        "02-30-2026",
        "abc",
        "09-13-2026",
        "Electric Bill",
        "N"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    add_expense(transactions, test_file)
    captured = capsys.readouterr()

    assert len(transactions) == 1
    assert transactions[0]["type"] == "expense"
    assert transactions[0]["amount"] == 250.50
    assert transactions[0]["date"] == "09-13-2026"
    assert transactions[0]["description"] == "Electric Bill"

def test_valid_amount(monkeypatch):
    user_inputs = iter(["250.50"])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    amount = get_valid_amount()

    assert amount == 250.50

def test_invalid_text_valid_amout(monkeypatch, capsys):
    user_inputs = iter([
        "abc",
        "250.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    amount = get_valid_amount()
    captured = capsys.readouterr()

    assert amount == 250.50
    assert "Invalid amount. Please enter a valid number" in captured.out

def test_non_positive_valid_amount(monkeypatch, capsys):
    user_inputs = iter([
        "-50",
        "0",
        "250.50"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    amount = get_valid_amount()
    captured = capsys.readouterr()

    assert amount == 250.50
    assert "Amount must be greater than 0" in captured.out

def test_get_valid_date(monkeypatch):
    user_inputs = iter(["09-20-2026"])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    date_text = get_valid_date()

    assert date_text == "09-20-2026"

def test_invalid_date_valid_date(monkeypatch, capsys):
    user_inputs = iter([
        "02-30-2026",
        "09-20-2026"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    date_text = get_valid_date()
    captured = capsys.readouterr()

    assert date_text == "09-20-2026"
    assert "Please enter a valid date" in captured.out

def test_invalid_format_valid_date(monkeypatch, capsys):
    user_inputs = iter([
        "abc",
        "09-20-2026"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    date_text = get_valid_date()
    captured = capsys.readouterr()

    assert date_text == "09-20-2026"
    assert "Please enter a valid date" in captured.out


def test_description(monkeypatch):
    user_inputs = iter([
        "paycheck"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    description = get_description()

    assert description == "paycheck"

def test_blank_description(monkeypatch):
    user_inputs = iter([
        "",
        "Y"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    description = get_description()

    assert description == ""

def test_add_description_after_blank(monkeypatch):
    user_inputs = iter([
        "",
        "N",
        "paycheck"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    description = get_description()

    assert description == "paycheck"

def test_invalid_response_description(monkeypatch, capsys):
    user_inputs = iter([
        "",
        "X",
        "",
        "Y"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    description = get_description()
    captured = capsys.readouterr()

    assert description == ""
    assert "Invalid response" in captured.out

def test_description_whitespace_only(monkeypatch):
    user_inputs = iter([
        "   ",
        "Y"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    description = get_description()

    assert description == ""

def test_transaction_menu_all_transactions(monkeypatch, capsys):
    transactions = [
        {
            "type": "income",
            "amount": 1000.00,
            "date": "09-20-2026",
            "description": "Paycheck"
        },
        {
            "type": "expense",
            "amount": 50.00,
            "date": "09-21-2026",
            "description": "Gas"
        }
    ]

    user_inputs = iter([
        "1",
        "4"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    transaction_menu(transactions)
    captured = capsys.readouterr()

    assert "Paycheck" in captured.out
    assert "Gas" in captured.out

def test_transaction_menu_income_only(monkeypatch, capsys):
    transactions = [
        {
            "type": "income",
            "amount": 1000.00,
            "date": "09-20-2026",
            "description": "Paycheck"
        },
        {
            "type": "expense",
            "amount": 50.00,
            "date": "09-21-2026",
            "description": "Gas"
        }
    ]

    user_inputs = iter([
        "2",
        "4"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    transaction_menu(transactions)
    captured = capsys.readouterr()

    assert "Paycheck" in captured.out
    assert "Gas" not in captured.out

def test_transaction_menu_expense_only(monkeypatch, capsys):
    transactions = [
        {
            "type": "income",
            "amount": 1000.00,
            "date": "09-20-2026",
            "description": "Paycheck"
        },
        {
            "type": "expense",
            "amount": 50.00,
            "date": "09-21-2026",
            "description": "Gas"
        }
    ]

    user_inputs = iter([
        "3",
        "4"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    transaction_menu(transactions)
    captured = capsys.readouterr()

    assert "Paycheck" not in captured.out
    assert "Gas"  in captured.out

def test_transaction_menu_return(monkeypatch, capsys):

    transactions = []
    user_inputs = iter([
        "4"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    transaction_menu(transactions)
    captured = capsys.readouterr()

    assert "Returning to main menu." in captured.out

def test_transaction_menu_invalid_option(monkeypatch, capsys):
    transactions = []
    user_inputs = iter([
        "5",
        "4"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    transaction_menu(transactions)
    captured = capsys.readouterr()

    assert "Invalid option" in captured.out
    assert "Returning to main menu." in captured.out
    