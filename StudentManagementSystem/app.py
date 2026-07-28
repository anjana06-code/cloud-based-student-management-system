import os
from flask import Flask, render_template
from database.create_database import init_db

def create_app():
    """
    Application factory for Cloud-Based Student Management System.
    """
    app = Flask(__name__)
    
    # Secret Key configuration for Flask Session security
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'internship-student-management-secret-key-2026')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file upload limit
    
    # Check and initialize SQLite database if missing
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    if not os.path.exists(db_file):
        print("Database file database.db not found. Initializing new database...")
        init_db()

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    # Home Landing Page Route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Run local development server
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Student Management System server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
