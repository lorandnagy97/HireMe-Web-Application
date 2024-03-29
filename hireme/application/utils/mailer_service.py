import boto3
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from wsgi import app


def load_mail_credentials(param_path):
    """
    Uses AWS's boto3 API to securely load
    parameters from the SSM parameter store.
    :param param_path: The path (name) of the parameter
    :return: the decrypted value of the parameter
    """
    client = boto3.client('ssm', region_name='eu-central-1')
    pw_param = client.get_parameter(
        Name=param_path,
        WithDecryption=True
    )
    return pw_param["Parameter"]["Value"]


class Mailer:
    """
    Class which uses google's smtp in order to send
    various emails according to the application's needs.
    """
    def __init__(self):
        """
        Initializes with mailing info specified in config
        (mail from, reply to etc). It checks the environment
        variable ENV, and if it's not a local run it
        utilizes AWS's SSM service in order to securely
        access the parameter containing the mail account's
        application password.
        """
        self.recipient_addr = app.config['VARS']['mail_to_name']
        self.mailer_addr = app.config['VARS']['mail_from_name']
        if 'local' not in app.config['VARS']['deploy_env']:
            self.mailer_pw = \
                self.load_mail_credentials(
                    app.config['VARS']['mail_param_path']
                )
        else:
            self.mailer_pw = app.config['VARS']['mail_password']

    def create_smtp_server(self):
        """
        Uses python smtp library to create a gmail smtp client
        :return: smtp client object
        """
        smtphost = "smtp.gmail.com:587"
        server = smtplib.SMTP(smtphost)
        server.ehlo()
        server.starttls()
        username = self.mailer_addr
        password = self.mailer_pw
        server.login(username, password)
        return server

    def create_message_template(self, subject):
        """
        Basic template describing the from/to/date/subject of email
        :param subject: string, subject of the email
        :return: MIMEMultipart message object
        """
        message = MIMEMultipart()
        message["From"] = "HireMe Notification"
        message["To"] = self.recipient_addr
        message["Date"] = formatdate(localtime=True)
        message["Subject"] = subject
        return message

    def compose_admin_invite_notification(self, code):
        """
        Puts together the error email.
        :return: MIMEMultipart message object
        """
        subject = "HireMe Admin Code"
        message = self.create_message_template(subject)
        message.attach(MIMEText("""Greetings!\n\n
Your HireMe web application has 
successfully launched. Please use
the following invitation code to
create your administrator account:\n\n{}
\n\n\n""".format(code))
                       )
        return message

    def compose_offer_notification(self, offer_details):
        """
        Puts together the offer email.
        :return: MIMEMultipart message object
        """
        subject = "New Offer From {}".format(
            offer_details['company_name']
        )
        message = self.create_message_template(subject)
        message.attach(MIMEText("""Congrats!\n\n
You've received an offer to work as a {} for
the following company: {}\n
Payment Offer Provided: {}\n
Contact Email: {}\n\n
Job Description: \n{}\n\n\n
""".format(
            offer_details['job_title'],
            offer_details['company_name'],
            offer_details['payment_offer'],
            offer_details['contact_email'],
            offer_details['job_description']
        )))
        return message

    def compose_error_notification(self, error):
        """
        Puts together the error email.
        :return: MIMEMultipart message object
        """
        subject = "HireMe Error Notification"
        message = self.create_message_template(subject)
        message.attach(MIMEText("""Greetings!\n\n
Your HireMe web application has 
encountered the following error:\n\n{}
\n\n\n""".format(error))
        )
        return message

    def prepare_message(self, type, content):
        """
        Calls the proper message composition based on
        user specification
        :param type: type of message to send (i.e. error or offer mail)
        :param content: variable representing the data to be inserted
        into the email templates
        :return: MIMEText object or None
        """
        if type is 'offer':
            message = self.compose_offer_notification(content)
            return message
        if type is 'error':
            message = self.compose_error_notification(content)
            return message
        if type is 'admin_code':
            message = self.compose_admin_invite_notification(content)
            return message
        return

    def send_email(self, type, content):
        """
        This method sends an email to the administrator;
        the email template used is decided upon by the
        type argument passed.
        :param type: which kind of email to send
        :param content: data to inject into the mail template
        :return:
        """
        message = self.prepare_message(type, content)
        server = self.create_smtp_server()
        server.sendmail(
            message['From'],
            message['To'],
            message.as_string()
        )
        server.close()

    def send_employer_email(self):
        """
        This method will be implemented later
        and will be used to send emails to employer's
        contact addresses.
        :return:
        """
        pass