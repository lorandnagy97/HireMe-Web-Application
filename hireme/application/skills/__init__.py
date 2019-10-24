from flask import Blueprint

bp = Blueprint(
    'skills',
    __name__,
    template_folder='templates'
)

from application.skills import routes