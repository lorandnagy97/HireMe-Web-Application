from flask import Blueprint

bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)

from application.admin import routes
from application.database.models import Invite