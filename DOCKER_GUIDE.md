# Docker Deployment Guide

This guide explains how to deploy the application using Docker Desktop. This is the easiest way to run the Backend, Frontend, and Database together.

## 📋 Prerequisites

1.  **Docker Desktop**: [Download and Install Docker Desktop](https://www.docker.com/products/docker-desktop/).
2.  **Git**: Ensure you have the project files.

## 🚀 Starting the Application

1.  Open your terminal (PowerShell or Command Prompt).
2.  Navigate to the project root directory (where `docker-compose.yml` is located).
3.  Run the following command to build and start all services:

    ```powershell
    docker-compose up --build
    ```

    *The first time you run this, it may take a few minutes to download images and build the containers.*

4.  Once started, you can access the application:
    -   **Frontend**: http://localhost:4200
    -   **Backend API**: http://localhost:5000
    -   **Swagger UI**: http://localhost:5000/apidocs/

    ### Application Preview

    **Frontend (User Management):**
    ![Frontend UI](C:/Users/Furkan/.gemini/antigravity/brain/fa5542ce-041f-4397-9b9d-90389e3639b3/uploaded_image_0_1763989347100.png)

    **Backend API Docs (Swagger UI):**
    ![Swagger UI](C:/Users/Furkan/.gemini/antigravity/brain/fa5542ce-041f-4397-9b9d-90389e3639b3/uploaded_image_1_1763989347100.png)

## 📜 Checking Logs

To see what's happening inside your containers (errors, access logs, etc.), use the following commands:

### View Logs for All Services
```powershell
docker-compose logs -f
```
*(Press `Ctrl+C` to stop watching logs)*

### View Logs for a Specific Service
-   **Backend**: `docker-compose logs -f flask-api`
-   **Frontend**: `docker-compose logs -f frontend`
-   **Database**: `docker-compose logs -f db`

## 💻 Accessing the Container Shell

Sometimes you need to go "inside" a container to run commands manually.

### 1. Backend Shell
To enter the Backend container:
```powershell
docker-compose exec flask-api bash
```
Now you are inside the Linux container! You can run commands like `ls` or `python`.
Type `exit` to leave.

### 2. Database Shell
To enter the Database container (e.g., to run SQL commands):
```powershell
docker-compose exec db bash
```

## 🗄️ Database Setup (First Time Only)

The database container starts empty. You need to create the tables.

### Option A: Using the Container Shell (Recommended)
1.  Enter the database container:
    ```powershell
    docker-compose exec db bash
    ```
2.  Run the SQL script using `sqlcmd` (you might need to copy the script content or mount it first, but here is how to connect):
    ```bash
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'SqlPass@123'
    ```
    *Then paste your SQL commands or run a script if mounted.*

### Option B: Using SQL Server Management Studio (SSMS)
1.  **Connect to the Database**:
    -   **Server**: `localhost,1433`
    -   **Authentication**: SQL Server Authentication
    -   **Login**: `sa`
    -   **Password**: `SqlPass@123` (as defined in `docker-compose.yml`)

2.  **Run the SQL Script**:
    Open the `usersandloginstabledatabase.sql` file and execute it against the connected server.

## 🛑 Stopping the Application

To stop the containers:
```powershell
docker-compose down
```
To stop and **remove data** (start fresh):
```powershell
docker-compose down -v
```

## 🔒 Security Best Practices

Since `docker-compose.yml` contains sensitive information (like database passwords), you might want to exclude it from your public GitHub repository while keeping it on your local machine.

Run these commands in PowerShell to untrack the file:

```powershell
# 1. Remove docker-compose.yml from Git tracking (keeps the file on your disk)
git rm --cached docker-compose.yml

# 2. Add it to .gitignore so it doesn't get added again
Add-Content .gitignore "`ndocker-compose.yml"

# 3. Commit the removal
git commit -m "Remove docker-compose.yml from repo to protect secrets"

# 4. Push the changes to GitHub
git push origin main
```
