from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for("basic.users", account="me"))

    if request.method == "POST":
        if not all(x in request.form for x in ["username", "password"]):
            return "Bad request", 400

        if not models.validateUser(request.form['username'], request.form['password']):
            return "Incorrect username and/or password, try again.", 403

        session['username'] = request.form['username']

        return redirect(url_for("basic.users", account="me"))

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect(url_for("basic.users", account="me"))

    if request.method == "POST":
        if not all(x in request.form for x in ["username", "password"]):
            return "Bad request", 400

        try:
            models.registerUser(request.form['username'], request.form['password'])
        except NameError as e:
            return "User already exists, try again.", 400
        except Exception as e:
            print(e)
            return "We encountered a problem handling your request, try again later.", 500

        return redirect(url_for("basic.login"))
    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    if 'username' not in session:
        return redirect(url_for("basic.login"))
    
    return render_template("users.html", account=session['username'])
