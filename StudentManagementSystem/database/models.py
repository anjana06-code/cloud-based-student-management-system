import sqlite3
import os

# Helper to get the absolute path to database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def get_db_connection():
    """
    Establishes and returns a database connection with row factory configured to dict-like objects.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ================================
# STUDENT DATABASE MODEL FUNCTIONS
# ================================

def get_student_by_email(email):
    """Fetch a single student record by email address."""
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
    conn.close()
    return student

def get_student_by_id(student_id):
    """Fetch a single student record by primary key ID."""
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return student

def create_student(name, email, password, department, year, course):
    """Create a new student record in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO students (name, email, password, department, year, course, progress)
           VALUES (?, ?, ?, ?, ?, ?, 0)""",
        (name, email, password, department, year, course)
    )
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return student_id

def update_student_profile(student_id, name, department, year, course):
    """Update existing student profile information."""
    conn = get_db_connection()
    conn.execute(
        """UPDATE students 
           SET name = ?, department = ?, year = ?, course = ?
           WHERE id = ?""",
        (name, department, year, course, student_id)
    )
    conn.commit()
    conn.close()

def update_student_password(student_id, new_password_hash):
    """Update student password by student ID."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE students SET password = ? WHERE id = ?",
        (new_password_hash, student_id)
    )
    conn.commit()
    conn.close()

def update_student_progress(student_id, progress):
    """Update progress percentage for a student."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE students SET progress = ? WHERE id = ?",
        (progress, student_id)
    )
    conn.commit()
    conn.close()

def get_all_students():
    """Retrieve all student records for admin management."""
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return students

def delete_student_by_id(student_id):
    """Delete a student record and associated records by ID."""
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


# ================================
# ADMIN DATABASE MODEL FUNCTIONS
# ================================

def get_admin_by_username(username):
    """Fetch an admin account by username."""
    conn = get_db_connection()
    admin = conn.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
    conn.close()
    return admin


# ================================
# COURSE DATABASE MODEL FUNCTIONS
# ================================

def get_all_courses():
    """Fetch all available courses."""
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses ORDER BY id ASC").fetchall()
    conn.close()
    return courses

def get_enrolled_courses(student_id):
    """Fetch courses enrolled by a specific student."""
    conn = get_db_connection()
    query = """
        SELECT c.* FROM courses c
        JOIN student_courses sc ON c.id = sc.course_id
        WHERE sc.student_id = ?
    """
    courses = conn.execute(query, (student_id,)).fetchall()
    conn.close()
    return courses

def enroll_student_course(student_id, course_id):
    """Enroll a student in a course if not already enrolled."""
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM student_courses WHERE student_id = ? AND course_id = ?",
        (student_id, course_id)
    ).fetchone()
    
    if not existing:
        conn.execute(
            "INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
            (student_id, course_id)
        )
        
        # Calculate new progress percentage based on enrolled courses
        total_courses = conn.execute("SELECT COUNT(*) as count FROM courses").fetchone()['count']
        enrolled_count = conn.execute(
            "SELECT COUNT(*) as count FROM student_courses WHERE student_id = ?",
            (student_id,)
        ).fetchone()['count']
        
        if total_courses > 0:
            new_progress = min(100, int((enrolled_count / total_courses) * 100))
            conn.execute("UPDATE students SET progress = ? WHERE id = ?", (new_progress, student_id))
            
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False


# ================================
# UPLOADS DATABASE MODEL FUNCTIONS
# ================================

def save_upload_record(student_id, filename, filepath):
    """Save metadata for an uploaded file."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO uploads (student_id, filename, filepath) VALUES (?, ?, ?)",
        (student_id, filename, filepath)
    )
    conn.commit()
    conn.close()

def get_student_uploads(student_id):
    """Retrieve all upload records for a specific student."""
    conn = get_db_connection()
    uploads = conn.execute(
        "SELECT * FROM uploads WHERE student_id = ? ORDER BY upload_date DESC",
        (student_id,)
    ).fetchall()
    conn.close()
    return uploads

def get_all_uploads():
    """Retrieve all upload records across all students for Admin view."""
    conn = get_db_connection()
    query = """
        SELECT u.*, s.name as student_name, s.email as student_email
        FROM uploads u
        JOIN students s ON u.student_id = s.id
        ORDER BY u.upload_date DESC
    """
    uploads = conn.execute(query).fetchall()
    conn.close()
    return uploads

def get_upload_by_id(upload_id):
    """Retrieve a single upload record by ID."""
    conn = get_db_connection()
    upload = conn.execute("SELECT * FROM uploads WHERE id = ?", (upload_id,)).fetchone()
    conn.close()
    return upload

def delete_upload_by_id(upload_id):
    """Delete an upload record from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM uploads WHERE id = ?", (upload_id,))
    conn.commit()
    conn.close()
