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

## 🛠️ Manual Deployment (Without Docker Compose)

If you cannot use `docker-compose.yml` (e.g., you excluded it or want to run containers manually), follow these steps to deploy the application using standard Docker commands.

### 1. Create a Network
Create a shared network so containers can talk to each other.
```powershell
docker network create app-network
```

### 2. Run the Database
Start the SQL Server container. We name it `db` so the backend can find it.
```powershell
docker run -d `
  --name db `
  --network app-network `
  -e "ACCEPT_EULA=Y" `
  -e "MSSQL_SA_PASSWORD=SqlPass@123" `
  -p 1433:1433 `
  mcr.microsoft.com/mssql/server:2022-latest
```

### 3. Build and Run the Backend
Build the image and start the container. We name it `flask-api` so the frontend can find it.

**Build:**
```powershell
docker build -t flask-backend ./PythonFlaskAPIBackend
```

**Run:**
```powershell
docker run -d `
  --name flask-api `
  --network app-network `
  -p 5000:5000 `
  -e "DB_SERVER=db" `
  -e "DB_NAME=flask_demo" `
  -e "DB_USER=sa" `
  -e "DB_PASSWORD=SqlPass@123" `
  -e "ODBC_DRIVER=ODBC Driver 17 for SQL Server" `
  -e "SECRET_KEY=dev_secret_key" `
  flask-backend
```

### 4. Build and Run the Frontend
Build the image and start the container.

**Build:**
```powershell
docker build -t angular-frontend ./AngularFrontend
```

**Run:**
```powershell
docker run -d `
  --name frontend `
  --network app-network `
  -p 4200:4200 `
  angular-frontend
```

### 5. Check Logs (Manual Mode)
Since we are not using Docker Compose, we check logs for each container individually.

```powershell
# Backend Logs
docker logs -f flask-api

# Frontend Logs
docker logs -f frontend

# Database Logs
docker logs -f db
```

### 6. Access Shell (Manual Mode)
To enter the containers manually:

```powershell
# Backend Shell
docker exec -it flask-api bash

# Database Shell
docker exec -it db bash
```

### 7. Cleanup (Stop & Remove)
To stop and remove these manually created containers:
```powershell
docker stop frontend flask-api db
docker rm frontend flask-api db
docker network rm app-network
```

