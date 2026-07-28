import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from database.models import (
    get_student_by_id,
    update_student_profile,
    get_all_courses,
    get_enrolled_courses,
    enroll_student_course,
    save_upload_record,
    get_student_uploads,
    get_upload_by_id
)
from cloud.azure_blob import upload_file_to_storage, UPLOAD_FOLDER

student_bp = Blueprint('student', __name__)

def student_required(func):
    """Decorator helper to restrict routes to logged-in students."""
    def wrapper(*args, **kwargs):
        if session.get('role') != 'student':
            flash('Access restricted. Please log in as a student.', 'warning')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ================================
# STUDENT DASHBOARD
# ================================
@student_bp.route('/dashboard')
@student_required
def dashboard():
    """Renders student dashboard with overview metrics, progress tracking, and courses."""
    student_id = session.get('user_id')
    student = get_student_by_id(student_id)
    
    if not student:
        session.clear()
        flash('Student record not found.', 'danger')
        return redirect(url_for('auth.login'))

    enrolled = get_enrolled_courses(student_id)
    all_courses = get_all_courses()
    uploads = get_student_uploads(student_id)

    return render_template(
        'dashboard.html',
        student=student,
        enrolled_courses=enrolled,
        total_courses_count=len(all_courses),
        uploads=uploads
    )


# ================================
# COURSES CATALOG & ENROLLMENT
# ================================
@student_bp.route('/courses')
@student_required
def courses():
    """Displays all available courses and enrollment status."""
    student_id = session.get('user_id')
    all_courses = get_all_courses()
    enrolled_courses = get_enrolled_courses(student_id)
    
    # Get set of enrolled course IDs
    enrolled_ids = {c['id'] for c in enrolled_courses}

    return render_template(
        'courses.html',
        courses=all_courses,
        enrolled_ids=enrolled_ids
    )


@student_bp.route('/enroll/<int:course_id>', methods=['POST'])
@student_required
def enroll(course_id):
    """Enrolls the logged-in student into a specified course."""
    student_id = session.get('user_id')
    success = enroll_student_course(student_id, course_id)
    
    if success:
        flash('Successfully enrolled in the course!', 'success')
    else:
        flash('You are already enrolled in this course.', 'info')
        
    return redirect(url_for('student.courses'))


# ================================
# STUDENT PROFILE MANAGEMENT
# ================================
@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    """Allows viewing and updating student profile."""
    student_id = session.get('user_id')
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', 1, type=int)
        course = request.form.get('course', '').strip()

        if not name:
            flash('Name cannot be empty.', 'danger')
        else:
            update_student_profile(student_id, name, department, year, course)
            session['user_name'] = name
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('student.profile'))

    student = get_student_by_id(student_id)
    return render_template('profile.html', student=student)


# ================================
# ASSIGNMENT FILE UPLOAD & VIEW
# ================================
@student_bp.route('/upload', methods=['GET', 'POST'])
@student_required
def upload():
    """Handles assignment file upload to local storage or Azure Blob Storage."""
    student_id = session.get('user_id')
    
    if request.method == 'POST':
        if 'assignment_file' not in request.files:
            flash('No file selected for upload.', 'danger')
            return redirect(url_for('student.upload'))
            
        file_obj = request.files['assignment_file']
        
        if file_obj.filename == '':
            flash('No file selected. Please choose a file to upload.', 'danger')
            return redirect(url_for('student.upload'))

        try:
            # Upload file via Cloud storage module (local fallback built-in)
            filename, filepath_or_url = upload_file_to_storage(file_obj, student_id)
            save_upload_record(student_id, filename, filepath_or_url)
            flash(f'File "{filename}" uploaded successfully!', 'success')
            return redirect(url_for('student.upload'))
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'danger')

    uploads = get_student_uploads(student_id)
    return render_template('upload.html', uploads=uploads)


@student_bp.route('/download/<int:upload_id>')
@student_required
def download(upload_id):
    """Allows downloading student's uploaded assignment file."""
    upload_rec = get_upload_by_id(upload_id)
    
    if not upload_rec:
        flash('File record not found.', 'danger')
        return redirect(url_for('student.upload'))
        
    # Verify ownership or admin role
    if upload_rec['student_id'] != session.get('user_id') and session.get('role') != 'admin':
        flash('Access denied. You can only download your own files.', 'danger')
        return redirect(url_for('student.dashboard'))

    filepath = upload_rec['filepath']
    
    # If URL (Azure Blob Storage), redirect to Azure URL
    if filepath.startswith('http://') or filepath.startswith('https://'):
        return redirect(filepath)
        
    # Local file download
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        # Fallback check in default uploads folder
        alt_path = os.path.join(UPLOAD_FOLDER, upload_rec['filename'])
        if os.path.exists(alt_path):
            return send_file(alt_path, as_attachment=True)
        else:
            flash('File does not exist on local server disk.', 'danger')
            return redirect(url_for('student.upload'))
