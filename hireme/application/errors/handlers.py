import traceback
from flask import render_template
from application import db
from application.utils import routing_tools
from application.errors import bp


@bp.app_errorhandler(404)
def not_found_error(e):
    """
    Shows a custom 404 page if a user
    attempts to access a non-existent page.
    :param e: error, not used here but
    the app_errorhandler requires it
    :return: rendered 404 page
    """
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(e):
    """
    Shows a custom 500 page is an error
    in the application is encountered.
    Sends an email to administrator with
    error traceback.
    :param e: error
    :return: rendered 500 page
    """
    db.session.rollback()
    error_info = traceback.format_exc()
    routing_tools.send_error_mail(error_info)
    return render_template('500.html'), 500