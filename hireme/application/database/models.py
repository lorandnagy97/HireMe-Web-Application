from datetime import datetime

from application import db
from application import login

from flask_login import UserMixin
from werkzeug.security import \
    generate_password_hash, check_password_hash


class Company(db.Model):
    """
    Defines table in which information about companies
    which have sent the site owner job offers is stored
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    offers = db.relationship('Offer', backref='employer', lazy='dynamic')

    def __repr__(self):
        return '<Company: {}, ID: {}>'.format(self.name, self.id)


class Offer(db.Model):
    """
    Defines table in which information on job offers
    is stored
    """
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120), index=True)
    pay_offer = db.Column(db.Float(asdecimal=True), index=True)
    contact_email = db.Column(db.String(120), index=True)
    job_description = db.Column(db.String(500))
    date = db.Column(db.String(25))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Position: {}, Pay: {}'.format(self.job_title, self.pay_offer)


class User(UserMixin, db.Model):
    """
    Defines users table in which usernames, emails,
    creation times, and password hashes are stored.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    user_role = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        """
        Hashes the user's password and stores it in the database
        :param password: unhashed password string
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the hashed password against the one
        which a user inputs when attempting to sign in.
        :param password: unhashed password string
        :return: boolean, true if correct pw
        """
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        """
        Returns the user's role/permissions group
        :return: self.urole
        """
        return self.urole

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Invite(db.Model):
    """
    A database table to store invite codes, and keep track
    of whether or not they have been used to create an account.
    """
    id = db.Column(db.Integer, primary_key=True)
    code_hash = db.Column(db.String(128), index=True, unique=True)
    code_type = db.Column(db.String(64), index=True, default='employer')
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    code_is_used = db.Column(db.Boolean, index=True, default=False)

    def set_code(self, code):
        """
        Hashes the invite code upon creation and stores it.
        :param code: unhashed invite code
        :return:
        """
        self.code_hash = generate_password_hash(code)

    def check_code(self, code):
        """
        Checks the hashed invite code against the code inputted
        when a user attempts to create an account.
        :param code: unhashed invite code
        :return:
        """
        return check_password_hash(self.code_hash, code)

    def __repr__(self):
        return 'Invite Code #' + self.id


@login.user_loader
def load_user(id):
    """
    Flask login function which simplifies user login
    :param id: ID of user
    :return: returns the user with the given ID from the database
    """
    return User.query.get(int(id))