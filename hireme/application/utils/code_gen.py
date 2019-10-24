import random
import string
from application import db
from application.utils import db_utils
from application.database.models import Invite
from application.utils.mailer_service import Mailer


def gen_code(code_length=16):
    """
    Generates an invite code with a default
    length of 16 characters, comprised of
    uppercase ascii characters.
    :param code_length: length of generated code
    :return: the generated invite code
    """
    characters = string.ascii_uppercase
    return ''.join(
        random.choice(characters) for i in range(
            code_length
        ))


def create_invite(type):
    """
    Creates an entry in the database detailing
    the invite code and whether or not it has
    been used.
    :param type: the type of user invited,
    e.g. admin or employer
    :return: the invite database object and the code
    """
    invite_code = gen_code()
    invite  = Invite(code_type=type)
    invite.set_code(invite_code)
    return invite, invite_code


def assign_admin_code():
    """
    Adds an admin user invitation to
    the database, returning the code
    :return: invite code
    """
    invite, invite_code = \
        create_invite('admin_code')
    db.session.add(invite)
    db.session.commit()
    return invite_code


def assign_employer_code():
    """
    Adds an employer invitation to
    the database, returning the code
    :return: invite code
    """
    invite, invite_code = \
        create_invite('employer_code')
    db.session.add(invite)
    db.session.commit()
    return invite_code


def has_initial_admin_code():
    """
    Checks if the initial administrator
    invitation has already been sent,
    so we don't duplicate the invite
    (due to the way gunicorn handles workers)
    :return: bool whether or not the code's
    been created
    """
    invite = Invite.query.filter_by(
        code_type='admin_code'
    ).first()
    if invite is not None:
        return True
    return False


def send_initial_admin_code():
    """
    Emails the invitation code for the
    administrator user to the address
    specified in the application configurations
    :return:
    """
    if not has_initial_admin_code():
        code = assign_admin_code()
        mailer = Mailer()
        mailer.send_email(
            type='admin_code',
            content=code
        )


def send_employer_code(email):
    """
    Sends an invitation code to an employer
    who has requested an account, to address
    specified on function call
    :param email: address to send to
    :return:
    """
    assign_employer_code()
    mailer.send_employer_email(
        type='employer_code',
        content=invite_code
    )


