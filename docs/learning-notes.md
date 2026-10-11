# Module 5 Learning Notes: Python Application Development

## 1. What is a backend?
The backend is the part of an application that receives requests, applies logic, works with data, and sends responses. Users usually interact with it through a frontend or an API client.

## 2. What is Flask?
Flask is a lightweight Python web framework. It provides tools to map URLs to Python functions and return responses.

## 3. What is a REST API?
A REST API lets applications communicate using HTTP. Resources are addressed through URLs and manipulated using HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

## 4. Important terms
- Route: URL rule connected to a function.
- Endpoint: A resource/action accessible through a URL and HTTP method.
- Request: Data sent by a client.
- Response: Data returned by a server.
- JSON: A common text format for exchanging structured data.
- Status code: Number describing the result of a request.
- CRUD: Create, Read, Update, Delete.

## 5. HTTP methods and common status codes
- GET: Read data.
- POST: Create a resource.
- PUT: Replace a resource.
- PATCH: Update selected fields.
- DELETE: Remove a resource.
- 200: Request succeeded.
- 201: Resource created.
- 400: Invalid request.
- 401: Authentication missing or invalid.
- 404: Resource or route not found.
- 409: Conflict, such as duplicate email.
- 500: Unexpected server error.

## 6. SQLite and SQL
SQLite is a small database stored in a file. SQL is used to work with database tables. This project uses CREATE TABLE, INSERT, SELECT, UPDATE, and DELETE statements.

The code uses parameterized SQL queries (question-mark placeholders) rather than inserting user text directly into SQL. This helps prevent SQL injection.

## 7. API-key authentication
A client sends a key in the `X-API-Key` header. The server compares it with a configured value before allowing access. This demonstrates a simple authentication pattern; it is not a complete user identity or authorization system.

## 8. Input validation
Validation checks whether required values exist and have acceptable formats. This project checks required student fields, non-empty strings, and a basic email format. A real application should use a robust validation library and stronger rules.

## 9. Testing
Automated tests check the API's expected behavior without needing to test each request manually. The included tests cover health, authentication, CRUD, invalid input, and duplicate email.

## 10. How to run
1. Create and activate a virtual environment.
2. Install packages with `python -m pip install -r requirements.txt`.
3. Set the `API_KEY` environment variable.
4. Run `python app.py`.
5. Use Postman or another HTTP client to test the endpoints.
6. Run tests with `python -m pytest -v`.

## 11. What I learned
I learned how to build a Python backend, define REST endpoints, connect SQLite, perform CRUD operations, validate incoming JSON, protect endpoints with an API key, test requests, and document a project for GitHub.

## 12. Viva questions
1. What is Flask?
2. What is a REST API?
3. What is the difference between GET and POST?
4. What does CRUD stand for?
5. Why do we use SQLite?
6. What is JSON?
7. What is input validation?
8. What is API-key authentication?
9. What is SQL injection and how do parameterized queries help?
10. Why do we write automated tests?
