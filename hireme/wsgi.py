from application import db, create_app

# runs app factory
app = create_app()

# once app is initialized, imports needed modules
from application.database import models
from application import \
    register_blueprints, get_locale


register_blueprints(app)

@app.before_first_request
def on_application_activation():
    """
    When the application boots up, the first
    request triggers the app to send an email
    to the admin specified in the config file,
    with an invitation code to set up an
    administrator account. It also gets the
    locale to be used for language options
    (second part to be implemented)
    :return:
    """
    from application.utils.code_gen import send_initial_admin_code
    send_initial_admin_code()
    get_locale(app)


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