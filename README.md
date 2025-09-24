# Personal Finance API

This project is a **RESTful API** built with **FastAPI** for managing personal finance transactions. It provides a robust set of endpoints for creating, retrieving, updating, and deleting transactions, with advanced features for filtering, sorting, and pagination.

---

## Features

- **Transactions Management**: Complete CRUD (Create, Read, Update, Delete) functionality for transactions.  
- **Advanced Filtering**: Filter transactions on fields like `amount`, `date`, and `category_id` using a flexible query syntax.  
- **Sorting**: Order the results by `amount` or `date` in ascending or descending order.  
- **Pagination**: Efficiently handle large datasets using `$top` (limit) and `$skip` (offset) query parameters.  
- **Data Expansion**: Retrieve related `Category` data by using the `$expand` query parameter to avoid multiple API calls.  
- **Data Validation**: Enforces strict data validation on all incoming requests using Pydantic models.  
- **API Documentation**: Automatic interactive API documentation is generated with Swagger UI.  
- **OpenAPI Specifications**: FastAPI automatically generates an OpenAPI Specification (OAS) JSON file (`/openapi.json`) which provides a standard, machine-readable description of the API's structure and endpoints.  
- **Simulated OData Services**: This API simulates key functionalities of the OData query syntax (e.g., `$filter`, `$orderby`, `$top`, `$skip`). This allows for powerful and flexible data querying without requiring a full OData service implementation.  

---

## Technologies Used

- **Framework**: FastAPI  
- **Database ORM**: SQLAlchemy  
- **Database**: SQLite (for simplicity, but can be easily swapped)  
- **Data Models**: Pydantic  
- **Advanced Filtering**: fastapi-filter  
- **Testing**: pytest  
- **Server**: Uvicorn  

---

## Setup and Installation

Follow these steps to get the API running on your local machine.  

### Prerequisites
- Python 3.8+  

### Steps

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On macOS/Linux
   source venv/bin/activate
   # On Windows
   venv\Scripts\activate

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the API server:
  ```bash
  uvicorn app.main:app --reload
  ```
The API will now be running at http://127.0.0.1:8000


## API Documentation

The API automatically generates interactive documentation using **Swagger UI**.
You can access it in your browser at:

👉 http://127.0.0.1:8000/docs

This documentation allows you to explore each endpoint, view required parameters, and make test requests directly from your browser.

### Endpoints

### POST /transaction
Creates a new transaction.
**Request Body:**
```json
{
  "amount": 5.25,
  "date": "2025-08-25",
  "description": "Bought some bread",
  "category": "Groceries"
}
```

**Responses:**
- ```200 OK```: Transaction created successfully.
- ```422 Unprocessable Entity```: Invalid or missing fields in the request body.

### GET /transactions/{transaction_id}
Retrieves a single transaction by its ID.
Parameters:
- ```transaction_id (path)```: The unique identifier of the transaction.

**Responses:**
- ```200 OK```: Returns the transaction data.
- ```404 Not Found```: Transaction with the given ID does not exist.

### PUT /transactions/{transaction_id}
Updates an existing transaction.
**Parameters:**
- ```transaction_id (path)```: The ID of the transaction to update.
Request Body: Same as the POST request body.

**Responses:**
- ```200 OK```: Transaction updated successfully.
- ```404 Not Found```: Transaction with the given ID does not exist.

### DELETE /transactions/{transaction_id}
Deletes a transaction.
**Parameters:**
- ```transaction_id (path)```: The ID of the transaction to delete.

**Responses:**
- ```200 OK```: Deletion successful.

- ```404 Not Found```: Transaction with the given ID does not exist.

### GET /transactions
Retrieves a list of transactions with advanced filtering, sorting, and pagination.
**Query Parameters:**

- ```$filter``` (optional): Filter the results. Supports amount, date, and category_id fields.
  **Examples:**
  ``` text
  ?amount__gt=50
  ?date__le=2025-08-27
  ?category_id__neq=1
  ```

- ```$orderby``` (optional): Sort the results.
  **Syntax:**
  ```text
  ?orderby=<field> [asc|desc]
  ```
  with comma-separated fields for multi-level sorting.
  **Examples:**
  ```text
  ?orderby=amount desc
  ?orderby=date asc,amount desc
  ```

- ```$top``` (optional): Limits the number of results.
**Constraints:** Must be an integer between 1 and 100.
**Example:**
```text
?top=10
```

- ```$skip``` (optional): Skips a specified number of results (for pagination).
**Constraints**: Must be a non-negative integer.
**Example**:
```text
?skip=20
```

- ```$expand``` (optional): Expands related data.
**Supported value**: category.
**Example:**
```text
?expand=category
```

## Running Tests
To run the test suite, navigate to the project root and execute the following command:
``` bash
pytest
```
