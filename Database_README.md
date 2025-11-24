# Database Setup

This project uses Microsoft SQL Server (MSSQL). Follow these instructions to set up the database.

## 📋 Prerequisites

1.  **SQL Server**: Install SQL Server Express or Developer edition.
2.  **SQL Server Management Studio (SSMS)**: [Download SSMS](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms) to manage your database.

## ⚙️ Setup Instructions

### 1. Open the SQL Script
Locate the file `usersandloginstabledatabase.sql` in the root directory of this project.

### 2. Connect to Your Server
Open SQL Server Management Studio (SSMS) and connect to your SQL Server instance.

### 3. Create the Database
Open a new query window and run the following command to create a new database (if you haven't already):

```sql
CREATE DATABASE your_database_name;
GO
USE your_database_name;
GO
```
*Replace `your_database_name` with the name you want to use (e.g., `ProjectDB`).*

### 4. Run the Script
1.  Open the `usersandloginstabledatabase.sql` file in SSMS.
2.  Ensure you are connected to the correct database (select it from the dropdown in the toolbar).
3.  Click the **Execute** button (or press F5) to run the script.

This will create the necessary tables (`users`, `logins`) and stored procedures.

## 🔍 Verifying the Setup

To verify that everything is set up correctly, run the following query:

```sql
SELECT * FROM logins;
```

You should see an initial admin user:
- **Username**: `admin`
- **Password**: `admin`

## ⚠️ Important Note
Make sure the database name you created matches the `DB_NAME` in your backend `.env` file.
