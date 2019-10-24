from application import app_directory
from application.database.models import Company, Offer
from application.utils.db_utils import DbUtility
from application.utils.mailer_service import Mailer
from flask import flash, url_for
from sqlalchemy import desc


def sort_offer_listings(listings_by_time):
    """
    When given a dict of job offers with timestamps,
    this function sorts them in descending order.
    :param listings_by_time: dictionary of offers + timestamps
    :return:
    """
    sorted_listings = []
    for key in sorted(listings_by_time, reverse=True):
        sorted_listings.append(listings_by_time[key])
    return sorted_listings


def create_offer_listing(offer_date, company_name, job_title):
    """
    This function creates a string describing
    a job offer.
    :return: string, formatted job offer
    """
    listing = \
        "{}<br><b>{}</b> has submitted an offer " \
        "for the position: <b>{}</b><br><hr>".format(
            offer_date,
            company_name,
            job_title
        )
    return listing


def get_raw_company_details():
    """
    Gets a list of all companies in database
    :return: list of companies
    """
    companies = Company.query.all()
    return companies

def get_company_offers(company):
    """
    Queries for all offers submitted by a specified company
    and returns them
    :param company: the company to query for offers
    :return: listing of offers associated with company
    """
    offers = company.offers.order_by(
        desc(Offer.timestamp)
    ).all()
    return offers


def assign_offer_listing_timestamps():
    """
    This function assigns timestamps to the formatted
    offer listings, returning them as a key/pair dictionary
    to be used for sorting by time.
    :return: listings with timestamps
    """
    companies = get_raw_company_details()
    listings_by_time = {}
    for company in companies:
        offers = get_company_offers(company)
        for offer in offers:
            listing = create_offer_listing(
                offer_date=offer.date,
                company_name=company.name,
                job_title=offer.job_title
            )
            listings_by_time[offer.timestamp] = listing
    return listings_by_time


def flash_offer_validation(form):
    """
    Displays a confirmation message when a company
    has successfully used the contact form
    :param form: contact form object (flask wtforms)
    :return:
    """
    flash(
        'Recruitment details for the position '
        'of {} at {} sent!'.format(
            form.job_title.data,
            form.recruiter_company.data,
            form.recruiter_email.data
        ), category='success')


def read_buzzword_file(buzzwords_file):
    """
    Reads from the application's static/files directory,
    splits file into list of lines
    :param buzzwords_file: name of the file to read&split
    :return: list of strings (lines from file)
    """
    buzzword_list = open(
            app_directory +
            url_for(
                'main_app.static',
                filename='files/{}'.format(
                    buzzwords_file
                )
            )
    ).read().splitlines()
    return buzzword_list


def get_offer_submission(form):
    """
    Reads the user input from the contact form and
    returns a dictionary of key/value pairs describing
    the input values
    :param form: contact form
    :return: dict of user input key/value pairs
    """
    offer_details = {}
    offer_details['company_name'] = form.recruiter_company.data
    offer_details['job_title'] = form.job_title.data
    offer_details['payment_offer'] = form.pay_offer.data
    offer_details['contact_email'] = form.recruiter_email.data
    offer_details['job_description'] = form.job_description.data
    return offer_details

def send_offer_mail(form):
    """
    Sends an email to site owner
    when a job offer has been posted
    :param form: contact form
    :return:
    """
    offer_details = get_offer_submission(form)
    mailer = Mailer()
    mailer.send_email('offer', offer_details)

def send_error_mail(error):
    """
    Sends an email to administrator
    when a 500 error is encountered
    :param error: error traceback
    :return:
    """
    mailer = Mailer()
    mailer.send_email('error', error)


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
    db_util = DbUtility(form)
    db_util.add_offer()
    flash_offer_validation(form)
    send_offer_mail(form)