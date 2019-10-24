from flask_wtf import FlaskForm
from wtforms import StringField, \
    PasswordField, BooleanField, \
    TextAreaField, DecimalField, \
    SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ContactForm(FlaskForm):
    recruiter_email = StringField(
        'Email',
        validators=[DataRequired()]
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
        default=0
    )
    job_description = TextAreaField(
        'Job Description',
        validators=[DataRequired()]
    )
    submit = SubmitField('Send Inquiry')