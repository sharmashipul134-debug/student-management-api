# Student Management REST API

A beginner-friendly Python REST API built with Flask and SQLite. It demonstrates routing, HTTP methods, CRUD operations, input validation, API-key authentication, parameterized SQL queries, testing, and documentation.

## Features

- Create, read, update, and delete student records
- SQLite database storage
- API-key protection for student endpoints
- Basic JSON and email validation
- Clear error responses and HTTP status codes
- Automated tests using pytest
- Health endpoint and root endpoint documentation

## Requirements

- Python 3.10 or newer recommended
- pip
- VS Code (optional)
- Postman (optional)

## Setup on Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt and run `venv\Scripts\activate.bat`.

Set a development API key before starting the application:

```powershell
$env:API_KEY="my-local-test-key"
python app.py
```

The API runs at `http://127.0.0.1:5000`.

The example default key is for local learning only. Change it before use, never commit real secrets, and do not deploy Flask's development server or debug mode to production.

## Authentication

Include this header for `/students` endpoints:

```text
X-API-Key: my-local-test-key
```

Use the same key value that you set in the `API_KEY` environment variable.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API overview |
| GET | `/health` | Health check |
| GET | `/students` | List all students |
| GET | `/students/<id>` | Get one student |
| POST | `/students` | Create a student |
| PUT | `/students/<id>` | Replace all student fields |
| PATCH | `/students/<id>` | Update selected student fields |
| DELETE | `/students/<id>` | Delete a student |

## Example request

POST `http://127.0.0.1:5000/students`

Headers:
```text
Content-Type: application/json
X-API-Key: my-local-test-key
```

JSON body:
```json
{
  "name": "Asha Sharma",
  "course": "BTech CSE",
  "email": "asha@example.com"
}
```

A successful creation returns HTTP `201 Created` and the new student record.

## Test with Postman

1. Start the server.
2. Create a request for an endpoint.
3. Add the `X-API-Key` header with your configured key.
4. For POST/PUT/PATCH, select Body → raw → JSON and enter the request body.
5. Send the request and check the status code and response.

## Run automated tests

```powershell
python -m pytest -v
```

## Project structure

```text
student-management-api/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── tests/
│   └── test_api.py
└── docs/
    └── learning-notes.md
```

## Limitations and future improvements

This is an educational project, not a production-ready student information system. Future improvements could include proper user login, role-based permissions, stronger schema validation, pagination, logging, database migrations, deployment, and integration tests. Never store real sensitive student information in a public demo.

## Learning outcomes

After completing the project, you should be able to explain Flask routes, REST APIs, HTTP methods, CRUD, SQLite, SQL parameterization, API-key authentication, validation, testing, and GitHub documentation.
