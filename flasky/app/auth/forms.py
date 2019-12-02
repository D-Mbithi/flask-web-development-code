from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email', validators=[Email(), DataRequired(), Length(1, 64)]
    )
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(1, 64),
            Regexp('^[a-zA-Z][A-Za-z0-9_.]*$'),
            0,
            # 'Username must have only letters, number, underscores or dots.'
        ]
    )
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            EqualTo('Password2', message='Passwords must match.')
        ]
    )
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def valid_email(self, field):
        if User.query.filter_by(email=field.data).firts():
            raise ValidationError('Email already exist.')

    def valid_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist.')
