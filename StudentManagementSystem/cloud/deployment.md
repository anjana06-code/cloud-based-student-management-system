# Azure Cloud Deployment & Storage Guide

This document provides step-by-step instructions for deploying the **Cloud-Based Student Management System** to **Microsoft Azure App Service**, setting up **Azure Blob Storage** for assignment uploads, and optionally migrating the SQLite database to **Azure SQL Database**.

---

## 1. Prerequisites

Before deploying, ensure you have:
1. An active **Microsoft Azure Account** (Student Subscription or Free Trial).
2. **Azure CLI** installed on your local Windows machine (`az --version`).
3. **VS Code** with the **Azure App Service** and **Azure Storage** extensions.
4. Python 3.10 or Python 3.11 installed locally.

---

## 2. Setting Up Azure Blob Storage

### Step 2.1: Create Storage Account via Azure CLI
Run the following commands in PowerShell or Command Prompt:

```powershell
# 1. Login to Azure
az login

# 2. Create a Resource Group
az group create --name StudentSystem-RG --location eastus

# 3. Create Storage Account (Name must be unique worldwide, lowercase numbers/letters)
az storage account create `
  --name studentmgmtstorage2026 `
  --resource-group StudentSystem-RG `
  --location eastus `
  --sku Standard_LRS

# 4. Create Blob Storage Container
az storage container create `
  --name student-uploads `
  --account-name studentmgmtstorage2026 `
  --public-access blob

# 5. Get Connection String
az storage account show-connection-string `
  --name studentmgmtstorage2026 `
  --resource-group StudentSystem-RG `
  --query connectionString --output tsv
```

> **Note**: Copy the connection string printed by the command above. You will set it as an Environment Variable in Azure App Service.

---

## 3. Deploying to Azure App Service

### Step 3.1: Prepare Application Files
Ensure `requirements.txt` includes:
- `Flask`
- `gunicorn` (WSGI web server for Linux App Service)
- `azure-storage-blob`
- `werkzeug`

Create a file named `startup.txt` in the root directory if deploying via Azure App Service Linux:
```text
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

### Step 3.2: Create and Deploy Web App via Azure CLI

```powershell
# 1. Create App Service Plan (B1 basic tier or F1 free tier)
az appservice plan create `
  --name StudentMgmtPlan `
  --resource-group StudentSystem-RG `
  --sku B1 `
  --is-linux

# 2. Create Web App (Replace student-mgmt-app-2026 with a unique app name)
az webapp create `
  --resource-group StudentSystem-RG `
  --plan StudentMgmtPlan `
  --name student-mgmt-app-2026 `
  --runtime "PYTHON|3.10"

# 3. Configure Environment Variables / App Settings
az webapp config appsettings set `
  --resource-group StudentSystem-RG `
  --name student-mgmt-app-2026 `
  --settings `
    SECRET_KEY="azure-production-secret-key-change-this" `
    AZURE_STORAGE_CONNECTION_STRING="YOUR_COPIED_CONNECTION_STRING_HERE" `
    AZURE_BLOB_CONTAINER_NAME="student-uploads"

# 4. Deploy via ZIP Deploy
az webapp deploy `
  --resource-group StudentSystem-RG `
  --name student-mgmt-app-2026 `
  --src-path ./project.zip `
  --type zip
```

---

## 4. Azure SQL Database Migration (Optional Upgrade)

If upgrading from SQLite to Azure SQL for enterprise scalability:

### Step 4.1: Create Azure SQL Server & Database
```powershell
# 1. Create SQL Server
az sql server create `
  --name student-sql-server-2026 `
  --resource-group StudentSystem-RG `
  --location eastus `
  --admin-user sqladmin `
  --admin-password "P@ssw0rd123456!"

# 2. Allow Azure Services to Access SQL Server
az sql server firewall-rule create `
  --resource-group StudentSystem-RG `
  --server student-sql-server-2026 `
  --name AllowAzureServices `
  --start-ip-address 0.0.0.0 `
  --end-ip-address 0.0.0.0

# 3. Create Database
az sql db create `
  --resource-group StudentSystem-RG `
  --server student-sql-server-2026 `
  --name StudentDB `
  --service-objective S0
```

### Step 4.2: Update Python Connection
Install `pyodbc` or `SQLAlchemy` in `requirements.txt`:
```python
# ODBC Connection String format for Azure SQL
import pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=student-sql-server-2026.database.windows.net;'
    'DATABASE=StudentDB;'
    'UID=sqladmin;'
    'PWD=P@ssw0rd123456!'
)
```

---

## 5. Storage Connection Code Overview

The file `cloud/azure_blob.py` handles storage logic seamlessly:

```python
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client("student-uploads")

# Upload file blob
blob_client = container_client.get_blob_client(filename)
blob_client.upload_blob(file_stream, overwrite=True)
```

* **Local Development**: If `AZURE_STORAGE_CONNECTION_STRING` is not set, files save locally in `uploads/`.
* **Production**: If set, files automatically stream to Azure Blob Storage and generate secure public/container URLs.

---

## 6. Expected Azure Portal Screenshots

When inspecting your deployment in the [Azure Portal](https://portal.azure.com):

1. **Resource Group Overview**:
   - `StudentSystem-RG` containing App Service (`student-mgmt-app-2026`), App Service Plan, and Storage Account.
2. **App Service Configuration**:
   - Application Settings displaying `AZURE_STORAGE_CONNECTION_STRING` and `SECRET_KEY`.
3. **Storage Account - Containers**:
   - Container `student-uploads` showing uploaded assignment files (`student_1_assignment1.pdf`).
4. **App Service Log Stream**:
   - Clean startup logs showing `gunicorn` binding to port 80/443.

---

## 7. Testing Procedure on Azure

1. **URL Verification**: Open `https://student-mgmt-app-2026.azurewebsites.net/`.
2. **Registration Test**: Register a new student account (`newstudent@example.com`).
3. **Login Test**: Login as Student and Admin (`admin` / `admin123`).
4. **File Upload Test**: Navigate to **Upload Assignment**, upload a PDF/Image file.
5. **Azure Blob Check**: Go to Azure Portal -> Storage Account -> `student-uploads` container to confirm the file exists in the cloud.
6. **Admin Panel Verification**: Log in as Admin, view student records and cloud uploads table.
