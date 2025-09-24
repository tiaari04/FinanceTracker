from datetime import date

def test_create_transaction_with_all_params(client):
    # Tests POST transaction with all parameters

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

def test_create_transaction_without_date(client):
    # Tests POST transaction without the date parameter

    data = {
        "amount" : 5.25,
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == str(date.today())
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

def test_create_transaction_without_description(client):
    # Tests POST transaction without the description parameter

    data = {
        "amount" : 5.25,
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == str(date.today())
    assert response.json()["description"] == None
    assert response.json()["category_id"] == 1

def test_create_transaction_without_amount_fail(client):
    # Tests fail POST transaction without the amount parameter

    data = {
        "description" : "Bought some bread",
        "date" : "2025-08-25",
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"][1] == "amount"
    

def test_create_transaction_without_category_fail(client):
    # Tests fail POST transaction without the category parameter

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"][1] == "category"

def test_update_transaction_without_date(client):
    # Tests POST transaction without the date parameter

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    new_data = {
        "amount" : 5.25,
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

    response = client.put("/transactions/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["transaction_id"] == 1
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == str(date.today())
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

def test_get_transaction_exists(client):
    # Tests GET transaction that is in the database

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

    response = client.get("/transactions/1")
    assert response.status_code == 200
    assert response.json()["transaction_id"] == 1
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

def test_get_transaction_not_exists(client):
    # Tests GET transaction that is not in the database
    response = client.get("/transactions/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction with id 1 not found"


def test_update_transaction_with_date(client):
    # Tests POST transaction with the date parameter

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    new_data = {
        "amount" : 5.25,
        "date" : "2025-08-26",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

    response = client.put("/transactions/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-26"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

def test_update_transaction_with_new_category(client):
    # Tests PUT transaction with new category parameter

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    new_data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Went to an Arcade",
        "category" : "Entertainment",
        }
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Bought some bread"
    assert response.json()["category_id"] == 1

    response = client.put("/transactions/1", json=new_data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["date"] == "2025-08-25"
    assert response.json()["description"] == "Went to an Arcade"
    assert response.json()["category_id"] == 2

def test_update_transaction_that_doesnt_exist(client):
    # Tests PUT transaction that is not in the database

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    response = client.put("/transactions/1", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction with id 1 not found"

def test_delete_transaction(client):
    # Tests DELETE transaction that is in the database

    data = {
        "amount" : 5.25,
        "date" : "2025-08-25",
        "description" : "Bought some bread",
        "category" : "Groceries",
        }
    
    response = client.post("/transactions",json=data)
    assert response.status_code == 200
    assert response.json()["amount"] == 5.25
    assert response.json()["category_id"] == 1

    response = client.delete("/transactions/1")
    assert response.status_code == 200
    assert response.json()["msg"] == "deleted transaction with id 1"

def test_delete_transaction_that_doesnt_exist(client):
    # Tests GET transaction that is not in the database

    response = client.delete("/transactions/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction with id 1 not found"

def create_mock_transactions(client):
    # Create mock transactions to test OData service parameter simulations

    """A helper function to create a consistent set of transactions for testing."""
    client.post("/transactions", json={
        "amount": 25.00, "date": "2025-08-25", "category": "Groceries", "description": "Fridge was empty"
    })
    client.post("/transactions", json={
        "amount": 10.00, "date": "2025-08-26", "category": "Utilities", "description": "Water bill"
    })
    client.post("/transactions", json={
        "amount": 50.00, "date": "2025-08-27", "category": "Groceries", "description": "Was hosting a party"
    })
    client.post("/transactions", json={
        "amount": 10.00, "date": "2025-08-28", "category": "Utilities", "description": "Light bill"
    })
    client.post("/transactions", json={
        "amount": 5.00, "date": "2025-08-29", "category": "Entertainment", "description": "Saw a cheap movie"
    })

def test_get_transactions_with_amount_filters(client):
    create_mock_transactions(client)
    # Filter for amount > 5 and amount < 50

    response = client.get("/transactions?amount__gt=5&amount__lt=50")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 3
    assert transactions[0]["amount"] == 25.00
    assert transactions[1]["amount"] == 10.00
    assert transactions[2]["amount"] == 10.00

def test_get_transactions_by_date_filter(client):
    create_mock_transactions(client)
    # Filter for transactions after 2025-08-27

    response = client.get("/transactions?date__gt=2025-08-27")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2 
    assert transactions[0]["description"] == "Light bill"
    assert transactions[1]["description"] == "Saw a cheap movie"

def test_get_transactions_with_orderby_amount_desc(client):
    create_mock_transactions(client)
    # Sort by amount in descending order

    response = client.get("/transactions?$orderby=amount desc")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 5
    assert transactions[0]["amount"] == 50.00
    assert transactions[1]["amount"] == 25.00
    assert transactions[2]["amount"] == 10.00

def test_get_transactions_with_multiple_orderby(client):
    create_mock_transactions(client)
    # Sort by amount descending, then date ascending for ties
    
    response = client.get("/transactions?$orderby=amount desc,date asc")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 5
    assert transactions[0]["amount"] == 50.00
    assert transactions[1]["amount"] == 25.00
    assert transactions[2]["date"] == "2025-08-26"
    assert transactions[3]["date"] == "2025-08-28"
    assert transactions[4]["amount"] == 5.00

def test_get_transactions_with_top_and_skip(client):
    create_mock_transactions(client)
    # Get the 3rd and 4th transactions (top=2, skip=2)

    response = client.get("/transactions?$top=2&$skip=2")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 50.00
    assert transactions[1]["amount"] == 10.00

def test_get_transactions_with_expand(client):
    client.post("/transactions", json={
        "amount": 10.00, "date": "2025-08-26", "category": "Utilities", "description": "T-2"
    })
    # Expand the category relationship

    response = client.get("/transactions?$expand=category")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 1
    
    # Check that the category field is a dictionary, not just an ID
    assert "name" in transactions[0]["category"]
    assert transactions[0]["category"]["name"] == "Utilities".lower()

def test_get_transactions_with_invalid_orderby_param(client):
    create_mock_transactions(client)
    # Test an invalid sort field

    response = client.get("/transactions?$orderby=invalid_field")
    assert response.status_code == 200
    assert response.json()["msg"] == "Cannot order by given parameters. Check parameter spelling or word order"

def test_get_transactions_with_invalid_expand_param(client):
    create_mock_transactions(client)
    # Test an invalid expand field

    response = client.get("/transactions?$expand=invalid_field")
    assert response.status_code == 200 
    assert response.json()["msg"] == "Cannot expand on given parameter. Check parameter spelling or word order"

def test_get_transactions_with_invalid_top_param(client):
    create_mock_transactions(client)
    # Test top=-1, which should be caught by FastAPI's validation

    response = client.get("/transactions?$top=-1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "greater_than_equal"

def test_get_transactions_with_invalid_skip_param(client):
    create_mock_transactions(client)
    # Test skip=-1, which should be caught by FastAPI's validation

    response = client.get("/transactions?$skip=-1")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "greater_than_equal"

def test_get_transactions_with_no_results(client):
    # This test assumes the database is empty or a unique filter is used
    
    response = client.get("/transactions?$amount__gt=99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "No transactions found under these filters"