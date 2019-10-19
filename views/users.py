from flask import Blueprint, render_template, request, session, redirect, url_for
from models.user import User, UserErrors

user_bluprint = Blueprint('users', __name__)


@user_bluprint.route('/')
def index():
    pass


@user_bluprint.route('/register', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_bluprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')


@user_bluprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('.login_user'))
