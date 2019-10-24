from flask_wtf import FlaskForm
from wtforms import \
    StringField, TextAreaField, \
    DecimalField, SubmitField
from wtforms.validators import \
    DataRequired, Email


class ContactForm(FlaskForm):
    """
    Form allowing potential employers
    to easily contact me with potential
    employment prospects.
    """
    recruiter_email = StringField(
        'Email',
        validators=[Email()]
    )
    recruiter_company = StringField(
        'Company',
        validators=[DataRequired()]
    )
    job_title = StringField(
        'Job Title',
        validators=[DataRequired()]
    )
    pay_offer = DecimalField(
        'Monthly Pay',
        default=None
    )
    job_description = TextAreaField(
        'Job Description',
        validators=[DataRequired()]
    )
    submit = SubmitField('Send Inquiry')