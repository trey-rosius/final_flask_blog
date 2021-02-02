import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from models.post import PostModel
from models.user import UserModel

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        full_names = request.form['full_names']
        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'Email is required.'
        elif not full_names:
            error = "Full names are required"
        elif not password:
            error = 'Password is required.'
        elif UserModel.find_user_by_email(email) is not None:
            error = 'User  with email- {} is already registered.'.format(email)

        if error is None:
            #   userModel = UserModel(full_names=full_names,email=email,password=enc_password)
            userModel = UserModel()
            userModel.password = UserModel.encrypt_password(password)
            userModel.full_names = full_names
            userModel.email = email
            userModel.save_to_db()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None
        user = UserModel.find_user_by_email(email)

        if user is None:
            error = 'Incorrect Email.'
        elif not user.authenticated(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.find_user_by_id(user_id)


def get_post(id, check_author=True):
    post = PostModel.find_by_id(id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.user_id != g.user.id:
        abort(403)

    return post


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
