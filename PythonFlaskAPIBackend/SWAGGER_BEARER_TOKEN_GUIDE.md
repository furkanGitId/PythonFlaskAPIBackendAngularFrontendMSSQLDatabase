# Using Bearer Token in Swagger UI

## Quick Start

1. **Start the Flask app:**
```powershell
; .\venv\Scripts\activate
; $env:FLASK_APP='app.py'
; python -m flask run
```

2. **Open Swagger UI:**
```
http://127.0.0.1:5000/apidocs
```

## Getting a Bearer Token

### Option 1: Get token via Swagger UI
1. Click on the **`/api/login` POST** endpoint
2. Click **"Try it out"**
3. Enter credentials:
```json
{
  "username": "admin",
  "password": "admin"
}
```
4. Click **"Execute"**
5. Copy the `token` from the response

### Option 2: Get token via curl
```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

## Using Token in Swagger UI

### Step 1: Authorize
1. Click the **"Authorize"** button (top-right of Swagger UI)
2. In the "Bearer" field, enter your token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
3. Click **"Authorize"** button
4. Click **"Close"**

### Step 2: Test Protected Endpoints
Now all protected endpoints will automatically include the Bearer token:

- **GET /api/users** — List all users
- **POST /api/users** — Create a new user
- **GET /api/users/<id>** — Get user by ID
- **PUT /api/users/<id>** — Update user
- **DELETE /api/users/<id>** — Delete user

Each endpoint will now include the `Authorization: Bearer <token>` header automatically.

## Token Expiration

By default, tokens expire after **1 hour** (3600 seconds). If you get a 401 error saying "Invalid or expired token", get a new token by logging in again.

## Example: Create User in Swagger

1. Get your Bearer token (see above)
2. Click **"Authorize"** and enter the token
3. Find **POST /api/users** endpoint
4. Click **"Try it out"**
5. Enter request body:
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```
6. Click **"Execute"**
7. Response should be 201 with the created user

## Troubleshooting

| Error | Solution |
|-------|----------|
| 401 "Token is missing" | Click "Authorize" and enter your Bearer token |
| 401 "Invalid or expired token" | Login again to get a fresh token |
| 400 "Validation failed" | Check your request body (name, email, etc.) |
| 404 "User not found" | Use a valid user ID when testing GET/PUT/DELETE |

## Security Note

- The default test credentials are `admin`/`admin`
- In production, implement proper user authentication against your database
- Store tokens securely (never expose in client code)
- Use HTTPS in production to protect tokens in transit
