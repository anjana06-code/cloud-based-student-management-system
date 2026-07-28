# Cloud-Based Student Management System

A full-stack, cloud-ready **Student Management System** developed with **Python Flask**, **SQLite**, custom **HTML5/CSS3/JavaScript**, and **Azure Cloud Storage / App Service** integration.

This project is designed specifically to serve as a complete, beginner-friendly internship academic project while maintaining clean architectural principles and industry-standard practices.

---

## 📁 Project Folder Structure

```text
StudentManagementSystem/
├── app.py                      # Main Flask application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive project documentation
├── .gitignore                  # Git ignore specifications
├── database.db                 # SQLite database (auto-generated)
├── uploads/                    # Local directory for assignment file uploads
│   └── .gitkeep
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout header/footer & alerts
│   ├── index.html              # Home landing page
│   ├── login.html              # Student login & password reset
│   ├── register.html           # Student registration form
│   ├── dashboard.html          # Student dashboard & progress tracking
│   ├── courses.html            # Course catalog & single-click enrollment
│   ├── upload.html             # Assignment file upload & history
│   ├── profile.html            # Student profile management
│   ├── admin_login.html        # Administrator authentication portal
│   ├── admin_dashboard.html    # Admin analytics & overview
│   ├── students.html           # Admin page: View/delete student accounts
│   └── uploads.html            # Admin page: View/delete uploaded files
├── static/                     # Static web assets
│   ├── css/
│   │   ├── style.css           # Global Navy Blue theme & UI components
│   │   ├── dashboard.css       # Metric cards, progress bars & grids
│   │   └── admin.css           # Admin data tables & status badges
│   ├── js/
│   │   ├── script.js           # Alert dismissal & delete confirmations
│   │   └── validation.js       # Client-side form & file validation
│   └── images/
├── database/                   # Database scripts and queries
│   ├── schema.sql              # SQL table creation DDL
│   ├── create_database.py      # Database setup & sample seed data script
│   └── models.py               # Database helper functions & SQLite queries
├── routes/                     # Modular Flask Blueprints
│   ├── auth.py                 # Authentication routes (login/register/logout)
│   ├── student.py              # Student dashboard, courses, file upload routes
│   └── admin.py                # Admin dashboard and management routes
└── cloud/                      # Azure Integration & Cloud Deployment
    ├── azure_blob.py           # Azure Blob Storage client with local fallback
    └── deployment.md           # Step-by-step Azure App Service & SQL guide
```

---

## 🛠️ Technology Stack

* **Backend**: Python 3.10+, Flask 3.0, Werkzeug (Password Hashing)
* **Frontend**: HTML5, Custom CSS3 (Modern Blue Palette, No Bootstrap), JavaScript (Vanilla ES6)
* **Database**: SQLite3 (Local Development), Azure SQL (Optional Migration)
* **Cloud**: Azure App Service (Hosting), Azure Blob Storage (Assignment Files)
* **Authentication**: Flask Session Management & Role-Based Access Control (Student/Admin)
* **IDE & OS**: VS Code on Windows 10/11

---

## 🔑 Pre-Configured Sample Accounts

For quick evaluation, the database is pre-seeded with sample records:

### 1. Student Account
* **Email**: `student@example.com`
* **Password**: `student123`
* **Role**: Student (Enrolled in Cloud Computing & Python Web Development)

### 2. Administrator Account
* **Username**: `admin`
* **Password**: `admin123`
* **Role**: Admin (Full access to student directory and upload auditing)

---

## 🚀 Quickstart & Installation Guide

### Step 1: Open Terminal / Command Prompt
Navigate to the project root directory in VS Code:
```powershell
cd StudentManagementSystem
```

### Step 2: Create a Virtual Environment
```powershell
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Initialize SQLite Database
Run the automated creation script to build tables and insert seed data:
```powershell
python database/create_database.py
```

### Step 5: Run Local Flask Server
```powershell
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🧪 Testing Procedure & Verification

### Test Case 1: Student Registration & Login
1. Navigate to **Student Register** (`/register`).
2. Fill out the form with a new email (`teststudent@example.com`) and submit.
3. Login using the newly created credentials.
4. **Expected Output**: Redirected to Student Dashboard displaying student name, department, and 0% initial progress.

### Test Case 2: Course Enrollment & Progress Calculation
1. From the student dashboard, click **Browse Course Catalog** (`/courses`).
2. Click **Enroll Now** on any un-enrolled course (e.g. *Database Management Systems*).
3. **Expected Output**: Flash notification "Successfully enrolled in the course!". Dashboard progress bar updates dynamically.

### Test Case 3: Assignment File Upload
1. Navigate to **Upload Assignment** (`/upload`).
2. Select a PDF or text file and click **Upload File**.
3. **Expected Output**: Success alert displayed. The upload appears in the **Submission History** table with a download link.

### Test Case 4: Admin Panel Management
1. Log out and navigate to **Admin Login** (`/admin/login`).
2. Enter username `admin` and password `admin123`.
3. Open **Students List** (`/admin/students`) to view all registered students.
4. Open **Uploaded Files** (`/admin/uploads`) to inspect or delete student file submissions.

---

## ☁️ Azure Cloud Deployment

Full instructions for deploying to **Azure App Service** and configuring **Azure Blob Storage** are available in [cloud/deployment.md](file:///C:/Users/admin/.gemini/antigravity/scratch/StudentManagementSystem/cloud/deployment.md).

### Quick Summary:
1. Set the environment variable `AZURE_STORAGE_CONNECTION_STRING` on Azure App Service.
2. The application will automatically stream all assignment uploads to Azure Blob Storage container `student-uploads`.

---

## 🐙 Git & GitHub Upload Guide

To upload this repository to your GitHub account:

### Step 1: Initialize Git Repository
```powershell
git init
git add .
git commit -m "Initial commit - Complete Cloud-Based Student Management System"
```

### Step 2: Link Remote GitHub Repository
```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/StudentManagementSystem.git
git push -u origin main
```

---

## 📷 UI Screenshots & Layout Placeholders

| Page | Description |
|---|---|
| **Landing Page** | Blue gradient hero banner with quick navigation cards for Student Registration, Login, and Admin Portal. |
| **Student Dashboard** | Metric overview cards, dynamic percentage progress bar, enrolled courses grid, and quick actions panel. |
| **Course Catalog** | Available courses grid with single-click course enrollment buttons. |
| **Assignment Upload** | Interactive file upload zone with file size/format validation and submission history table. |
| **Admin Control Panel** | Dark-themed header, student count metrics, data tables with deletion actions. |
