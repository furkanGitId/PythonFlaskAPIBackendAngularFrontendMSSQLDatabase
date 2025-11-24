# Python Flask API Backend

This is the backend for our application, built using Python and Flask. It provides an API to interact with the SQL Server database.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python**: [Download Python](https://www.python.org/downloads/) (Version 3.8 or higher is recommended).
2.  **SQL Server**: You need access to a SQL Server instance.
3.  **ODBC Driver**: [Download ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

## ⚙️ Installation & Setup

Follow these steps to set up the backend:

### 1. Navigate to the Backend Directory
Open your terminal or command prompt and move into the backend folder:
```bash
cd PythonFlaskAPIBackend
```

### 2. Create a Virtual Environment
It's good practice to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
```

### 3. Activate the Virtual Environment
```bash
# Windows (PowerShell)
.\venv\Scripts\Activate
```
*Note: You should see `(venv)` at the beginning of your terminal line.*

### 4. Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a file named `.env` in the `PythonFlaskAPIBackend` directory. Add your database connection details:

```env
DB_SERVER=YOUR_SERVER_NAME\INSTANCE_NAME
DB_NAME=your_database_name
ODBC_DRIVER=ODBC Driver 17 for SQL Server
SECRET_KEY=your_secret_key
```
*Replace `YOUR_SERVER_NAME\INSTANCE_NAME` and `your_database_name` with your actual SQL Server details.*

## 🚀 Running the Application

Start the Flask server:

```bash
# Windows (PowerShell)
$env:FLASK_APP='app.py'
python -m flask run
```

The API will be available at `http://127.0.0.1:5000`.

## 📖 API Documentation

Once the server is running, you can view the interactive API documentation (Swagger UI) at:
`http://127.0.0.1:5000/apidocs`

## 🧪 Testing

To run the tests:
```bash
pytest
```
