import sqlite3

from flask import Blueprint, Response, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from komradebank.models import User, Acct, Xact, do_transfer, db
from komradebank.forms import LoginForm, RegisterForm, EditForm, XferForm

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def index():

    acct = None
    xacts = None

    u = User.by_id(current_user.get_id())
    if u is not None:

        acct = Acct.by_user_id(u.id)[0]
        xacts = Xact.by_acct_id(acct.id)

        # calculate running balance
        balance = acct.balance
        for i, x in enumerate(xacts):
            x.balance = balance
            balance -= x.amount

    return render_template("index.html", acct=acct, xacts=xacts)


@main.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        User.new(form.username.data, form.password.data)
        flash('Registration successful!', 'success')
        return redirect(url_for(".login"))

    return render_template("register.html", form=form)


@main.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        u = User.by_name(form.username.data)
        if u:
            login_user(u)
            flash("Logged in successfully.", "success")
            return redirect(request.args.get('next') or url_for(".index"))

    return render_template("login.html", form=form)


@main.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))


@main.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@main.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit(username):

    # fetch user model to edit
    u = User.by_name(username)
    if u is not None:
        user = u
    else:
        user = current_user

    # only admin's can edit other user account details
    if user.id != current_user.id and not current_user.is_admin():
        flash("Access Denied - This infractions has been reported to the cyber police.", "failure")
        return redirect(url_for(".index"))

    form = EditForm(
        role=user.role,
        username=user.name,
        fullname=user.fullname,
        phone=user.phone,
        email=user.email
    )

    if request.method == 'POST' and form.validate_on_submit():

        if form.password.data != "":
            u.set_password(form.password.data)
        u.role = form.role.data
        u.fullname = form.fullname.data
        u.phone = form.phone.data
        u.email = form.email.data

        # commit updates
        u.update()

        flash("Successfully updated details.", "success")
        return redirect(request.args.get('next') or url_for(".index"))

    return render_template("edit.html", user=user, form=form)


@main.route('/xfer', methods=['GET', 'POST'])
@login_required
def xfer():

    acct = Acct.by_user_id(current_user.id)[0]
    form = XferForm(
        dst='',
        amount=0.00,
        memo='Enter description...',
    )
    form.src.data = acct.id

    if request.method == 'POST' and form.validate_on_submit():
        msg = do_transfer(acct.id, form.dst.data, form.amount.data, form.memo.data)
        flash(msg)
        return redirect(url_for(".index"))

    return render_template("xfer.html", form=form, avail=acct.balance)


@main.route('/admin')
@login_required
def admin():

    if not current_user.is_admin():
        flash("Access Denied - This infraction has been reported to the cyber police.", "failure")
        return redirect(url_for(".index"))

    users = User.by_filter('')
    accts = Acct.by_filter('')
    for a in accts:
        u = User.by_id(a.user)
        a.user_name = u.name
        xacts = Xact.by_acct_id(a.id)
        a.count = len(xacts)

    return render_template("admin.html", user=current_user, users=users, accts=accts)


@main.route('/acct/', defaults={'acct_id': ''})
@main.route('/acct/<acct_id>')
@login_required
def acct(acct_id):

    if acct_id == '':
        acct = Acct.by_user_id(current_user.id)[0]
    else:
        try:
            q = "SELECT * from accts WHERE acct_id = '%s'" % acct_id
            row = db.get(q)
            if row is None:
                return 'sql: no rows in result set'
            acct = Acct._from_row(row)
        except Exception as e:
            err = {
                'query': q,
                'error': repr(e),
            }
            return jsonify(err)

    xacts = Xact.by_acct_id(acct.id)
    data = [u.__dict__ for u in xacts]
    return jsonify(data)


@main.route('/users', defaults={'filter':''})
@main.route('/users/<filter>')
@login_required
def users(filter):

    if not current_user.is_admin():
        flash("Access Denied - This infraction has been reported to the cyber police.", "failure")
        return redirect(url_for(".index"))

    users = User.by_filter(filter)
    data = [u.__dict__ for u in users]
    return jsonify(data)
