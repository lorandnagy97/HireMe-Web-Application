from flask_wtf import FlaskForm
from wtforms import StringField, \
    PasswordField, BooleanField, \
    TextAreaField, DecimalField, \
    SubmitField
from wtforms.validators import \
    DataRequired, Email, \
    EqualTo, Length


class RegistrationForm(FlaskForm):
    """
    wtform used for user registration
    """
    email = StringField(
        'Contact Email',
        validators=[
            Length(
                min=6,
                message='Too short..'
            ),
            Email(
                message='Not a valid email address.'
            ),
            DataRequired(
                message='Please input email address.'
            )
    ])
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_assword = PasswordField(
        'Confirm Password',
        validators=[
            EqualTo(
                'password',
                message='Passwords do not match.'
            ),
            DataRequired(
                message='Please confirm your password.'
            )
        ]
    )
    invitation_code = StringField(
        'Invitation Code',
        validators=[DataRequired()]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    wtform used for user authentication
    """
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember_me = BooleanField(
        'Remember Me'
    )
    submit = SubmitField('Sign In')

