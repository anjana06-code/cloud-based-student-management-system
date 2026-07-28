# 🎓 Cloud-Based Student Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite3-Database-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-Blob_Storage-0089D6?style=for-the-badge&logo=microsoftazure)](https://azure.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A full-stack, cloud-enabled **Student Management System** developed with **Python Flask**, **SQLite**, custom **HTML5/CSS3/JavaScript** (No heavy UI frameworks), and **Microsoft Azure** cloud storage integration. 

This project was built as a full-stack internship portfolio project showcasing role-based access control, cloud file management, dynamic progress tracking, and cloud deployment architecture.

---

## ✨ Features Overview

### 👨‍🎓 Student Portal
- **User Authentication**: Student registration and secure login using hashed passwords (`werkzeug.security`).
- **Interactive Dashboard**: Displays active degree courses, assignment submission count, and automated academic completion percentage.
- **Course Enrollment**: Catalog of university courses with 1-click enrollment tracking.
- **Cloud Assignment Upload**: Submits assignment files directly to **Azure Blob Storage** (with seamless local disk fallback for offline development).
- **Profile Management**: Update department, year of study, and degree track.
- **Self-Service Password Reset**: Secure password recovery module.

### 🛡️ Administrator Panel
- **System Metrics Dashboard**: Real-time stats on registered students, active courses, and cloud file storage.
- **Student Management Directory**: View all student records and delete inactive accounts.
- **Cloud File Auditor**: Review uploaded student assignments with single-click download and deletion controls.
- **Role-Based Security**: Flask session middleware ensuring strict access control between Student and Admin roles.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.10+, Flask 3.0, Werkzeug WSGI
- **Frontend**: HTML5, Vanilla CSS3 (Custom Navy Blue Palette, Responsive Grid, No Bootstrap), ES6 JavaScript
- **Database**: SQLite3 (Local Development) / Azure SQL Database (Cloud Migration Ready)
- **Cloud Infrastructure**: Azure App Service (Hosting), Azure Blob Storage (Assignment Files)
- **Deployment Server**: Gunicorn WSGI Server

```text
               +-----------------------------------+
               |       Browser / User Interface    |
               +-----------------+-----------------+
                                 |
                                 v
               +-----------------+-----------------+
               |        Flask Web Server           |
               | (Auth, Student & Admin Blueprints)|
               +--------+------------------+------+
                        |                  |
       +----------------+                  +----------------+
       v                                                    v
+--------------+                                  +-------------------+
|  SQLite DB   |                                  | Azure Blob Storage|
| (database.db)|                                  | (student-uploads) |
+--------------+                                  +-------------------+

StudentManagementSystem/
├── app.py                      # Flask Application Entry Point
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
├── .gitignore                  # Git Exclusion Rules
├── database.db                 # Seeded SQLite Database File
├── uploads/                    # Local Directory for File Uploads
├── database/
│   ├── schema.sql              # SQL Table Definitions (DDL)
│   ├── create_database.py      # Database Initialization & Sample Data Seed
│   └── models.py               # Database Helper Functions & SQL Queries
├── cloud/
│   ├── azure_blob.py           # Azure Blob Storage Client & Local Fallback
│   └── deployment.md           # Step-by-Step Azure Deployment Guide
├── routes/
│   ├── auth.py                 # Login, Registration & Logout Routes
│   ├── student.py              # Student Dashboard, Courses & Upload Routes
│   └── admin.py                # Admin Panel Management Routes
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Master Layout (Header, Navigation, Footer)
│   ├── index.html              # Landing Page
│   ├── login.html              # Student Login & Password Reset
│   ├── register.html           # Student Registration Form
│   ├── dashboard.html          # Student Dashboard & Progress Tracker
│   ├── courses.html            # Course Catalog & Enrollment
│   ├── upload.html             # Assignment Upload & History
│   ├── profile.html            # Student Profile Management
│   ├── admin_login.html        # Administrator Login Portal
│   ├── admin_dashboard.html    # Admin Analytics & Control Center
│   ├── students.html           # Student Management Directory
│   └── uploads.html            # File Upload Management Auditor
└── static/
    ├── css/
    │   ├── style.css           # Global Navy Theme, Form & Button Styles
    │   ├── dashboard.css       # Metric Cards & Progress Bars
    │   └── admin.css           # Admin Tables & Badges
    └── js/
        ├── script.js           # Toast Alerts & UI Interactions
        └── validation.js       # Client-Side Form & File Validation
