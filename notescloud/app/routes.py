from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


posts = [
    {
        "author": "Jasmine",
        "title": "Session 1",
        "content": "Class Notes",
        "date_posted": "August 24 2020",
    },
    {
        "author": "Jiaying",
        "title": "Session 26",
        "content": "Review Session",
        "date_posted": "November 18 2020",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "jgong1@babson.edu" and form.password.data == "12345678":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid information. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)