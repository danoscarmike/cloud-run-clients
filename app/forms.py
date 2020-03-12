from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="*")])
    password = PasswordField('Password', validators=[DataRequired(message="*")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="*")])
    last_name = StringField('Last Name', validators=[DataRequired(message="*")])
    email = StringField('Email', validators=[DataRequired(message="*"), Email()])
    username = StringField('Username', validators=[DataRequired(message="*")])
    password = PasswordField('Password', validators=[DataRequired(message="*")])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[DataRequired(message="*"), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with this email address already exists.')