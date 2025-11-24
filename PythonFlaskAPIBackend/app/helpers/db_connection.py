# app/helpers/db_connection.py
import pyodbc
from app.config import Config


def get_db_connection() -> pyodbc.Connection:
    """
    Create and return a live SQL Server connection using the
    connection string assembled inside Config.SQLALCHEMY_DATABASE_URI.
    Any exception will bubble up and the caller will handle it.
    """
    try:
        return pyodbc.connect(
            Config.SQLALCHEMY_DATABASE_URI,
            timeout=5  # optional, avoids long hanging attempts
        )
    except Exception as ex:
        print("Database connection failed:")
        print(ex)
        raise  # let the caller see the real error


def row_to_dict(cursor, row) -> dict | None:
    """
    Convert a pyodbc Row to a dictionary using column names.
    Example: {"id": 1, "name": "Sam"}
    """
    if not row:
        return None

    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
