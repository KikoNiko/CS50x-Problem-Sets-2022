from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Welcome back!", category='success')
                return redirect(url_for("main.home"))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("User does not exist!", category='error')


    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        # Conditions for successfull registration
        if email_exists:
            flash("Email already exists!", category='error')
        elif username_exists:
            flash("Username already exists!", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='errorr')
        elif len(username) < 2:
            flash("Username too short!", category='error')
        elif len(password1) < 6:
            flash("Password is too short!", category='error')
        elif len(email) < 6:
            flash("Not a valid email", category='error')
        elif '@' and '.' not in email:
            flash("Not a valid email", category='error')
        else:
            hashed_password = generate_password_hash(password1)
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User Created! Welcome, Foodster!", category='success')
            return redirect(url_for("main.home"))


    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


