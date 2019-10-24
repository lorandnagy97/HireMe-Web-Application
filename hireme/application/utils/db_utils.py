from datetime import datetime
from flask import flash
from sqlalchemy.exc import IntegrityError
from werkzeug.security import \
    generate_password_hash, check_password_hash
from application import db
from application.database.models import \
    Company, Offer, User, Invite
from application.utils.code_gen import gen_code
from wsgi import app


class DbUtility:
    """
    This class contains useful methods for manipulating
    data in this application's database.
    """
    def __init__(self, form):
        self.form = form
        self.company = None

    @staticmethod
    def do_company_validation(company_name):
        """
        Check if company already exists in
        the database
        :param company_name: name of company to check for
        :return: bool, true if exists
        """
        company_listing = Company.query.filter_by(
            name=company_name
        ).first()
        if company_listing is not None:
            return True
        return False

    def add_company_row(self):
        """
        If the company doesn't already exist
        in the database, this method adds the
        new company information to the
        company table.
        :return:
        """
        company_name = \
            self.form.recruiter_company.data
        company_listing_exists = \
            self.do_company_validation(company_name)
        if company_listing_exists:
            self.company = \
                Company.query.filter_by(name=company_name).first()
            return
        self.company = Company(name=company_name)
        db.session.add(self.company)
        db.session.commit()

    def add_offer(self):
        """
        Adds information about a job offer to the
        respective table in the database. This row
        is then associated with the company that made
        the offer.
        :return:
        """
        self.add_company_row()
        job_title = self.form.job_title.data
        pay_offer = self.form.pay_offer.data
        contact_email = self.form.recruiter_email.data
        job_description = self.form.job_description.data
        timestamp = datetime.now()
        offer = Offer(
            job_title=job_title,
            pay_offer=pay_offer,
            contact_email=contact_email,
            job_description=job_description,
            date=timestamp.strftime("%a %b %y"),
            timestamp=timestamp,
            employer=self.company
        )
        db.session.add(offer)
        db.session.commit()

    def validate_invite_code(self):
        """
        Checks if a user who is attempting registration
        inputs a valid invite code, which has not been
        used. Returns the invitation's user role and
        whether the code exists
        :return: bool, true if valid code, and type of invite
        """
        code = self.form.invitation_code.data
        invite_codes = Invite.query.all()
        for invite_code in invite_codes:
            if invite_code.check_code(code)\
                    and not invite.code_is_used:
                return True, invite_code.code_type
        return False, None

    def add_user(self):
        """
        Reads the data from user registration form
        and translates that information into the relevant
        User table upon successful registration
        :return:
        """
        username = self.form.username.data
        user_email = self.form.email.data
        password = self.form.password.data
        has_valid_code, code_type = \
            self.validate_invite_code()
        if has_valid_code:
            timestamp = datetime.today()
            user = User(
                name=username,
                email=user_email,
                created_time=timestamp,
                urole=code_type
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered!', category='success')
            return
        flash('Invalid Invite Code', category='warning')
        return

    @staticmethod
    def add_invite_code(code_type):
        """
        Adds an invitation entry to the
        relevant database table (Invite)
        :param code_type: type of code, determines user's role
        :return:
        """
        code = gen_code()
        timestamp = datetime.today()
        invite = Invite(
            created_time=timestamp,
            code_type=code_type
        )
        invite.set_code(code)
        db.session.add(invite)
        db.session.commit()

