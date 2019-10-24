from flask import flash
from application.database.models import User
from application.utils.db_utils import DbUtility


def process_user_registration(form):
    """
    Adds a user to the database upon
    successful registration form
    submission
    :param form: registration form
    :return:
    """
    db_util = DbUtility(form)
    db_util.add_user()


def flash_failed_login():
    """
    Flashes a message notifying the user
    of a failed login attempt
    :return:
    """
    flash(
        'Invalid username or password',
        category='warning'
    )


def flash_successful_login(form):
    """
    Flashes a message notifying the user
    of a successful login
    :param form:
    :return:
    """
    flash(
        'Welcome, {}!'.format(form.username.data),
        category='success'
    )


def is_successful_login(form):
    """
    Checks the database to see if the
    user has entered credentials that
    will successfully authenticate
    :param form: login form
    :return: bool, true if successful auth
    """
    user = User.query.filter_by(
        name=form.username.data
    ).first()
    if user is None or not user.check_password(
        form.password.data
    ):
        flash_failed_login()
        return False
    return True