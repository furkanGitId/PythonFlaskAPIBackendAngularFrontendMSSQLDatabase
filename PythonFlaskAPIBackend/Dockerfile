# ---- run stage ----
FROM python:3.11-slim

# 1. install ODBC manager + curl/gpg utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl gnupg unixodbc unixodbc-dev g++ && \
    rm -rf /var/lib/apt/lists/*

# 2. add Microsoft SQL Server ODBC repo (Debian 12 example)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] \
          https://packages.microsoft.com/debian/12/prod bookworm main" \
          > /etc/apt/sources.list.d/mssql-release.list

# 3. install Driver 17
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. application
COPY . .
CMD ["python", "app.py"]