from flask import render_template, \
    flash, \
    redirect, \
    url_for, \
    Blueprint
from application.database.models \
    import Company, Offer, User
from application.main_app \
    import bp
from application.main_app.forms \
    import ContactForm
from application.utils.db_utils \
    import DbUtility
from application.utils \
    import routing_tools, db_utils


def process_offer_submission(form):
    """
    When a prospective employer submits
    an offer via the contact form, this
    function adds the offer to the database,
    while notifying the user of the successful
    submission. An email is also sent to the
    site owner address specified in the app's
    configurations.
    :param form: contact form
    :return:
    """
    db_util = db_utils.DbUtility(form)
    db_util.add_offer()
    routing_tools. \
        flash_offer_validation(form)
    routing_tools.send_offer_mail(form)


@bp.route('/')
@bp.route('/index')
def index():
    """
    Renders the html for the home page of
    the application, reading from a text
    file which allows for easy configuration
    of the 'buzzwords'/catchphrases displayed.
    :return: the rendered index.html file
    """
    content = {
        'title': 'HireMe Home',
        'buzzwords': routing_tools.read_buzzword_file(
            'buzzwords.txt'
        )
    }
    content['first_buzzword'] = \
        content['buzzwords'][0]
    return render_template('index.html',
                           title=content['title'],
                           content=content
                           )


@bp.route('/contact',
           methods=['GET', 'POST'])
def contact():
    """
    A contact form page which allows for
    a prospective employer to easily send me
    an email with information about a job
    offer. This function executes the tasks
    required to render the page, processing
    the form if needed.
    :return: the rendered html for the form.
    """
    form = ContactForm()
    if form.validate_on_submit():
        process_offer_submission(form)
        return redirect(url_for('main_app.index'))
    return render_template(
        'contact.html',
        title = 'Contact Me',
        form=form
    )


@bp.route('/offers')
def offers():
    """
    A page restricted to administrator view only
    which displays a list of offers, sorted by
    time submitted and detailing the company
    and job title specified.
    :return: the rendered html (complete with listings)
    """
    listings = routing_tools.get_offer_listings()
    return render_template(
        'offers.html',
        title='Recent Offers',
        listings=listings)