from flask import render_template, \
    flash, \
    redirect, \
    url_for, \
    Blueprint
from application.main_app import bp
from application.database.models import Company, Offer, User
from application.main_app.forms import ContactForm
from application.utils.db_utils import DbUtility
from application.utils import routing_tools
from sqlalchemy import desc
from wsgi import app


@bp.route('/')
@bp.route('/index')
def index():
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
    form = ContactForm()
    if form.validate_on_submit():
        db_util = DbUtility(form)
        db_util.add_offer()
        routing_tools.\
            flash_offer_validation(form)
        routing_tools.send_offer_mail(form)
        return redirect(url_for('index'))
    return render_template(
        'contact.html',
        title = 'Contact Me',
        form=form
    )


@bp.route('/offers')
def offers():
    listings = routing_tools.get_offer_listings()
    return render_template(
        'offers.html',
        title='Recent Offers',
        listings=listings)