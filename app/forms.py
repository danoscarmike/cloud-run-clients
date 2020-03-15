from app.models import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField,\
    TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, \
    ValidationError


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please choose a different username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="*")])
    password = PasswordField('Password',
                             validators=[DataRequired(message="*")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(message="*")])
    last_name = StringField('Last Name',
                            validators=[DataRequired(message="*")])
    email = StringField('Email', validators=[DataRequired(message="*"),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(message="*")])
    password = PasswordField('Password',
                             validators=[DataRequired(message="*")])
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
            raise ValidationError('An account with this email address'
                                  'already exists.')
