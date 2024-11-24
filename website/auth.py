from flask import Blueprint, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student, Employee
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Student.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":  # Ensure we are checking the request method
        email = request.form.get("email")
        name = request.form.get("name")
        Len = request.form.get("Len")  # Renamed from 'Len' to 'length'
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = Student.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif email is not None and len(email) <= 5:
            flash("Email must be greater than 10 characters", category="error")
        elif name is not None and len(name) <= 4:
            flash("Name must be greater than 4 characters", category="error")
        elif password1 is not None and len(password1) <= 6:
            flash("Password must be greater than 6 characters", category="error")
        elif password1 != password2:
            flash("You entered wrong password", category="error")
        else:
            new_user = Student(email=email, name=name, Len=Len, password=generate_password_hash(password1, method="pbkdf2:sha256"))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Log in the newly created user
            flash("You are registered.", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

# @auth.route("/laundrylogin", methods=["GET", "POST"])
# def laundrylogin():
#     email = request.form.get("email")
#     password = request.form.get("email")
#     employee = Employee.query.filter_by(email=email).first()
#     if employee:
#         if check_password_hash(employee.password, password):
#             login_user(employee, remember=True)
#             return redirect(url_for("views.laundry_management"))
#     return render_template("laundrylogin.html", user=current_user)

# @auth.route("/laundrylogout", methods=["GET", "POST"])
# @login_required
# def laundrylogout():
#     logout_user()
#     return redirect(url_for("auth.laundrylogin"))


# @auth.route("/laundrysignup", methods=["GET", "POST"])
# def laundrysignup():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")
#         employee = Employee.query.filter_by(email=email).first()
#         if employee:
#             flash("Email already exists", category="error")
#         elif password1 != password2:
#             flash("You entered wrong password", category="error")
#         elif email[:12] == "dhobiclinicw":
#             new_employee = Employee(email=email, password=generate_password_hash(password1, method="pbkdf2:sha256"))
#             db.session.add(new_employee)
#             db.session.commit()
#             login_user(new_employee, remember=True)
#             flash("You are registered", category="success")
#             return redirect(url_for("views.laundry_management"))

#         else:
#             flash("Entered wrong email", category="error")
#     return render_template("laundrysign_up.html", user=current_user)

@auth.route("/laundrylogin", methods=["GET", "POST"])
def laundrylogin():
    if request.method == "POST":
        email = request.form.get("email")  # Corrected to "email"
        password = request.form.get("password")  # Corrected to "password"
        employee = Employee.query.filter_by(email=email).first()
        if employee:
            if check_password_hash(employee.password, password):
                flash("Logged in successfully")
                login_user(employee, remember=True)
                return redirect(url_for("views.laundry_management"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
            
    return render_template("laundrylogin.html", user=current_user)


@auth.route("/laundrylogout")
@login_required
def laundrylogout():
    logout_user()
    return redirect(url_for("auth.laundrylogin"))

# @auth.route("/laundrysignup", methods=["GET", "POST"])
# def laundrysignup():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")

#         employee = Employee.query.filter_by(email=email).first()
#         if employee:
#             flash("Email already exists", category="error")
#         elif password1 != password2:
#             flash("Passwords do not match", category="error")
#         elif email[:12] != "dhobiclinicw":
#             flash("wrong email entered")
#         else:
#             new_employee = Employee(
#                 email=email,
#                 password=generate_password_hash(password1, method="pbkdf2:sha256", salt_length=16)
#             )
#             db.session.add(new_employee)
#             db.session.commit()
#             login_user(new_employee, remember=True)
#             flash("Registration successful", category="success")
#             return redirect(url_for("views.laundry_management"))

#     return render_template("laundrysign_up.html", user=current_user)

@auth.route("/laundrysignup", methods=["GET", "POST"])
def laundrysignup():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Debug prints
        print(f"Received email: {email}, Passwords: {password1}, {password2}")

        employee = Employee.query.filter_by(email=email).first()
        if employee:
            flash("Email already exists", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif email[:12] != "dhobiclinicw":
            flash("Wrong email entered", category="error")
        else:
            try:
                new_employee = Employee(
                    email=email,
                    password=generate_password_hash(password1, method="pbkdf2:sha256", salt_length=16)
                )
                db.session.add(new_employee)
                db.session.commit()
                login_user(new_employee, remember=True)
                flash("Registration successful", category="success")
                return redirect(url_for("views.laundry_management"))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", category="error")

    return render_template("laundrysign_up.html", user=current_user)
