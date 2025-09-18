from datetime import date

def test_create_transaction_with_all_params(client):
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
    response = client.get("/transactions/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction with id 1 not found"


def test_update_transaction_with_date(client):
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
    response = client.delete("/transactions/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction with id 1 not found"