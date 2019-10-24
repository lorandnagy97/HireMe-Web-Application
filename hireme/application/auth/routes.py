from flask import \
    render_template, redirect, url_for, Blueprint
from flask_login import \
    current_user, login_user, logout_user
from application.auth.forms import \
    RegistrationForm, LoginForm
from application.auth import bp
from application.utils import auth_tools


@bp.route('/register',
           methods=['GET', 'POST'])
def register():
    """
    Function to handle the rendering of the
    user registration page, as well as processing
    the submission of the registration form
    :return: rendered page
    """
    # Redirect request if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main_app.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        auth_tools.process_user_registration(form)
        return redirect(url_for('main_app.index'))
    return render_template(
        'register.html',
        title='Register',
        form=form
    )


@bp.route('/login',
           methods=['GET', 'POST'])
def login():
    """
    Function to handle the rendering of the
    login form page, activating the authentication
    procedure upon form submission.
    :return: rendered page, upon successful login
    home page, upon failed login same page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_app.index'))
    form = LoginForm()
    will_remember = form.remember_me.data
    if form.validate_on_submit():
        if not auth_tools.is_successful_login(form):
            auth_tools.flash_failed_login()
            return redirect(url_for('auth.login'))
        login_user(user, remember=will_remember)
        auth_tools.flash_successful_login(form)
        return redirect(url_for('main_app.index'))
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    """
    Simple function utilizing flask's logout method,
    redirects user to homepage and deauthenticates
    :return: home page rendered template
    """
    logout_user()
    return redirect(url_for('main_app.index'))