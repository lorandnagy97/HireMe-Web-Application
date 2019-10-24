from flask import Blueprint

bp = Blueprint(
    'main_app',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from application.main_app import routes, forms