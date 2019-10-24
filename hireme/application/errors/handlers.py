from flask import render_template
from application import db
from application.utils import routing_tools
from application.errors import bp

import traceback


@bp.app_errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    error_info = traceback.format_exc()
    routing_tools.send_error_mail(error_info)
    return render_template('500.html'), 500