# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / '.env'
load_dotenv(dotenv_path=DOTENV_PATH)

# Flask basic settings
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

# SQL Server settings from .env
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "flask_demo")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

# Encryption options
DB_ENCRYPT = os.getenv("DB_ENCRYPT", "yes")
DB_TRUSTSERVERCERTIFICATE = os.getenv("DB_TRUSTSERVERCERTIFICATE", "yes")


def build_pyodbc_conn_str() -> str:
    # Build the connection string with encryption support
    return (
        f"DRIVER={{{ODBC_DRIVER}}};"
        f"SERVER={DB_SERVER},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};PWD={DB_PASSWORD};"
        f"Encrypt={DB_ENCRYPT};"
        f"TrustServerCertificate={DB_TRUSTSERVERCERTIFICATE};"
    )


# Export for Flask
class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = build_pyodbc_conn_str()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
