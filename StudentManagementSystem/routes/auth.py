from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import (
    get_student_by_email,
    create_student,
    get_admin_by_username,
    update_student_password
)

auth_bp = Blueprint('auth', __name__)

# ================================
# STUDENT REGISTRATION
# ================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new student registration."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        department = request.form.get('department', 'Computer Science')
        year = request.form.get('year', 1, type=int)
        course = request.form.get('course', 'B.Tech CS')

        # Form Validation
        if not name or not email or not password:
            flash('All required fields must be filled out.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')

        # Check if student already exists
        existing_student = get_student_by_email(email)
        if existing_student:
            flash('An account with this email address already exists. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        # Hash password and create student
        password_hash = generate_password_hash(password)
        create_student(name, email, password_hash, department, year, course)

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ================================
# STUDENT LOGIN
# ================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles student authentication."""
    # Redirect if already logged in as student
    if session.get('role') == 'student':
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html')

        student = get_student_by_email(email)

        if student and check_password_hash(student['password'], password):
            # Set session parameters
            session.clear()
            session['user_id'] = student['id']
            session['user_name'] = student['name']
            session['user_email'] = student['email']
            session['role'] = 'student'

            flash(f'Welcome back, {student["name"]}!', 'success')
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email address or password. Please try again.', 'danger')

    return render_template('login.html')


# ================================
# ADMIN LOGIN
# ================================
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Handles administrator authentication."""
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both admin username and password.', 'danger')
            return render_template('admin_login.html')

        admin = get_admin_by_username(username)

        if admin and check_password_hash(admin['password'], password):
            session.clear()
            session['user_id'] = admin['id']
            session['user_name'] = admin['username']
            session['role'] = 'admin'

            flash('Administrator authentication successful.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid administrator credentials.', 'danger')

    return render_template('admin_login.html')


# ================================
# FORGOT PASSWORD
# ================================
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handles password reset for students."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        student = get_student_by_email(email)
        if not student:
            flash('No registered account found with that email address.', 'danger')
            return render_template('login.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('login.html')

        # Update password hash
        new_hash = generate_password_hash(new_password)
        update_student_password(student['id'], new_hash)

        flash('Your password has been reset successfully. Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


# ================================
# LOGOUT
# ================================
@auth_bp.route('/logout')
def logout():
    """Logs out student or admin and clears active session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
