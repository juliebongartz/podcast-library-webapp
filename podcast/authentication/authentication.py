from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
import podcast.adapters.repository as repo
import podcast.authentication.services as services

authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - please supply another'

    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register')
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_name' in session and session['user_name'] is not None:
        flash('You are already logged in. Redirecting to home page.', 'info')
        return redirect(url_for('home_bp.home'))

    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            session.clear()
            session['user_name'] = user['user_name']
            flash('Login successful!', 'success')
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            user_name_not_recognised = (
                'Username not recognised - '
                f'<a class="underline-link" href="{url_for("authentication_bp.register")}">register here</a>.'
            )

        except services.AuthenticationException:
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home_bp.home'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session or session['user_name'] is None:
            flash('Session expired or invalid. Please register or log in again.', 'warning')
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register', render_kw={"class": "form-submit"})


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login', render_kw={"class": "form-submit"})