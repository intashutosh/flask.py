from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# Initialize database and app settings
app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate(app, db)

def create_app():
    app.config['SECRET_KEY'] = "@Adarsh30"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # Register blueprints for routes
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import models and create the database if it doesn't exist
    from .models import Student, Clothdetails, Employee
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created Database!")
        else:
            print("Database already exists.")

    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Determine if the user is a student or employee based on your implementation
        user = Student.query.get(user_id) or Employee.query.get(user_id)
        return user
    return app
    
from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user  # Import from Flask-Login

def student_login_required(func):
    """Decorator to restrict access to students."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:  # Check if user is logged in
            flash("Please log in to access this page.", category="error")
            return redirect(url_for("auth.login"))  # Redirect to login page
        if hasattr(current_user, 'role') and current_user.role != "student":
            flash("Unauthorized access.", category="error")
            return redirect(url_for("views.home"))  # Redirect to the student home
        return func(*args, **kwargs)
    return wrapper

def employee_login_required(func):
    """Decorator to restrict access to employees."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:  # Check if user is logged in
            flash("Please log in to access this page.", category="error")
            return redirect(url_for("auth.laundrylogin"))  # Redirect to employee login
        if hasattr(current_user, 'role') and current_user.role != "employee":
            flash("Unauthorized access.", category="error")
            return redirect(url_for("views.laundry_management"))  # Redirect to some safe page
        return func(*args, **kwargs)
    return wrapper

