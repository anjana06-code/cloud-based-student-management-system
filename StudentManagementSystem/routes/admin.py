from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.models import (
    get_all_students,
    delete_student_by_id,
    get_all_uploads,
    get_upload_by_id,
    delete_upload_by_id,
    get_all_courses
)
from cloud.azure_blob import delete_file_from_storage

admin_bp = Blueprint('admin', __name__)

def admin_required(func):
    """Decorator helper to enforce admin authentication."""
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Administrator authentication required.', 'warning')
            return redirect(url_for('auth.admin_login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ================================
# ADMIN DASHBOARD
# ================================
@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    """Renders administrator overview dashboard with system metrics."""
    students = get_all_students()
    uploads = get_all_uploads()
    courses = get_all_courses()

    return render_template(
        'admin_dashboard.html',
        total_students=len(students),
        total_uploads=len(uploads),
        total_courses=len(courses),
        recent_students=students[:5],
        recent_uploads=uploads[:5]
    )


# ================================
# MANAGE STUDENTS
# ================================
@admin_bp.route('/admin/students')
@admin_required
def students():
    """Displays a list of all registered students."""
    all_students = get_all_students()
    return render_template('students.html', students=all_students)


@admin_bp.route('/admin/students/delete/<int:student_id>', methods=['POST'])
@admin_required
def delete_student(student_id):
    """Deletes a student account and associated data by ID."""
    delete_student_by_id(student_id)
    flash(f'Student record ID #{student_id} deleted successfully.', 'success')
    return redirect(url_for('admin.students'))


# ================================
# MANAGE UPLOADED FILES
# ================================
@admin_bp.route('/admin/uploads')
@admin_required
def uploads():
    """Displays all uploaded student files."""
    all_uploads = get_all_uploads()
    return render_template('uploads.html', uploads=all_uploads)


@admin_bp.route('/admin/uploads/delete/<int:upload_id>', methods=['POST'])
@admin_required
def delete_upload(upload_id):
    """Deletes an uploaded file from disk/cloud and database."""
    upload_rec = get_upload_by_id(upload_id)
    if upload_rec:
        # Delete file from Azure Blob or Local disk
        delete_file_from_storage(upload_rec['filepath'])
        delete_upload_by_id(upload_id)
        flash('Uploaded file record deleted successfully.', 'success')
    else:
        flash('Upload record not found.', 'danger')
        
    return redirect(url_for('admin.uploads'))
