from flask import request
from application import \
    babel, db, create_app

# runs app factory
app = create_app()

# once app is initialized, import needed modules
from application.database import models
from application import register_blueprints


register_blueprints(app)

@app.before_first_request
def on_application_activation():
    """
    When the application boots up, the first
    request triggers the app to send an email
    to the admin specified in the config file,
    with an invitation code to set up an
    administrator account.
    :return:
    """
    from application.utils.code_gen import send_initial_admin_code
    send_initial_admin_code()


@app.shell_context_processor
def make_shell_context():
    """
    Allows for the flask application and
    database to be manipulated via cli
    without having to specify configs
    :return:
    """
    return {
        'db': db,
        'Company': models.Company,
        'Offer': models.Offer}


@babel.localeselector
def get_locale():
    """
    Gets the user's region and allows
    for proper language translation.
    This is still to be implemented.
    :param app: flask application instance
    :return: the best match out of the app's configured languages
    """
    return request.accept_languages.best_match(
        app.config['LANGUAGES']
    )