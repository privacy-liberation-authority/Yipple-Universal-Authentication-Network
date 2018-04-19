from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Implement me
        return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Implement me
        return "register request received", 400

    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    # Implement me

    return render_template("users.html")
