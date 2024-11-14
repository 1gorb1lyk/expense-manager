
## Project Overview
This project is a simple Django REST API for managing user expenses. It allows users to create, list, update, and delete expenses, as well as filter expenses by date range and generate category summaries.

## Features
- **Expense CRUD**: Create, retrieve, update, and delete expenses.
- **Filter by Date Range**: List expenses for a user within a specified date range.
- **Category Summary**: Calculate total expenses per category for a given month.

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django 5.x
- Django REST Framework

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/1gorb1lyk/expense-manager.git
    cd expense-manager
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://localhost:8000/api/`.

---

## API Endpoints

### 1. List All Expenses
- **Method**: `GET`
- **Endpoint**: `/api/expenses/`
- **Description**: Retrieves a list of all expenses.
- **Response**: `200 OK`
    ```json
    [
      {
        "id": 1,
        "user": 1,
        "title": "Groceries",
        "amount": "75.50",
        "date": "2024-11-15",
        "category": "Food"
      }
    ]
    ```

---

### 2. Create an Expense
- **Method**: `POST`
- **Endpoint**: `/api/expenses/`
- **Description**: Creates a new expense.
- **Body**:
    ```json
    {
      "user": 1,
      "title": "Groceries",
      "amount": 75.50,
      "date": "2024-11-15",
      "category": "Food"
    }
    ```
- **Response**: `201 Created`
    ```json
    {
      "id": 1,
      "user": 1,
      "title": "Groceries",
      "amount": "75.50",
      "date": "2024-11-15",
      "category": "Food"
    }
    ```

---

### 3. Retrieve a Single Expense
- **Method**: `GET`
- **Endpoint**: `/api/expenses/<int:pk>/`
- **Description**: Retrieves details of a single expense by its ID.
- **Response**: `200 OK`
    ```json
    {
      "id": 1,
      "user": 1,
      "title": "Groceries",
      "amount": "75.50",
      "date": "2024-11-15",
      "category": "Food"
    }
    ```

---

### 4. Delete an Expense
- **Method**: `DELETE`
- **Endpoint**: `/api/expenses/<int:pk>/`
- **Description**: Deletes an expense by its ID.
- **Response**: `204 No Content`

---

### 5. List Expenses by Date Range
- **Method**: `GET`
- **Endpoint**: `/api/expenses/date-range/<int:user_id>/?start=YYYY-MM-DD&end=YYYY-MM-DD`
- **Description**: Lists expenses for a user within the specified date range.
- **Example**:
    ```
    /api/expenses/date-range/1/?start=2024-11-01&end=2024-11-30
    ```
- **Response**: `200 OK`
    ```json
    [
      {
        "id": 2,
        "user": 1,
        "title": "Taxi",
        "amount": "30.00",
        "date": "2024-11-12",
        "category": "Travel"
      }
    ]
    ```

---

### 6. Get Expense Category Summary
- **Method**: `GET`
- **Endpoint**: `/api/expenses/summary/<int:user_id>/<int:month>/`
- **Description**: Calculates and returns the total expenses per category for a given user and month.
- **Example**:
    ```
    /api/expenses/summary/1/11/
    ```
- **Response**: `200 OK`
    ```json
    [
      {
        "category": "Food",
        "total": "75.50"
      },
      {
        "category": "Travel",
        "total": "30.00"
      }
    ]
    ```

---