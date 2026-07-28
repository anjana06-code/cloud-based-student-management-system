import sqlite3
import os
from werkzeug.security import generate_password_hash

# Path to the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def init_db():
    """
    Initializes the SQLite database using schema.sql and populates sample data.
    """
    print(f"Initializing database at: {DB_PATH}")
    
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read schema SQL script
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
        
    # Execute database creation statements
    cursor.executescript(schema_sql)
    print("Database schema tables created successfully.")
    
    # Insert default admin account (username: admin, password: admin123)
    admin_password_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT INTO admins (username, password) VALUES (?, ?)",
        ('admin', admin_password_hash)
    )
    
    # Insert sample courses
    sample_courses = [
        ('Cloud Computing Essentials', 'Learn fundamentals of AWS, Azure, virtualization, and cloud infrastructure.'),
        ('Python Web Development', 'Master Flask framework, RESTful APIs, and full-stack web applications.'),
        ('Database Management Systems', 'Understand relational databases, SQL queries, indexing, and normalized design.'),
        ('Data Structures & Algorithms', 'Study arrays, linked lists, trees, graphs, sorting, and algorithmic complexity.'),
        ('Cyber Security Basics', 'Introduction to network security, cryptography, and application security best practices.')
    ]
    
    cursor.executemany(
        "INSERT INTO courses (course_name, course_description) VALUES (?, ?)",
        sample_courses
    )
    
    # Insert sample student (email: student@example.com, password: student123)
    student_password_hash = generate_password_hash('student123')
    cursor.execute(
        """INSERT INTO students (name, email, password, department, year, course, progress) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ('Alex Johnson', 'student@example.com', student_password_hash, 'Computer Science', 3, 'B.Tech CS', 65)
    )
    
    # Enroll sample student in initial courses (Course IDs: 1 and 2)
    student_id = cursor.lastrowid
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, 1))
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, 2))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Sample seed data inserted successfully!")
    print("Default Admin: Username = admin | Password = admin123")
    print("Default Student: Email = student@example.com | Password = student123")

if __name__ == '__main__':
    init_db()
