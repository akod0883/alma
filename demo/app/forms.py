from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import app, db
#from flask_login import userMIxin

# part 6 24 / part 4 5:00
# need a user class for the login manager extension...
# class User():
#    def __init__(self, user_id):
#        self.user_id = user_id
#    conn = db.connect()
#    query_results = conn.execute(
#        "Select * from newRestaurants where id = {};").format(user_id).fetchall()
#    conn.close()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        conn = db.connect()
        query_results = conn.execute("Select username from users;").fetchall()
        conn.close()
        exists = False
        for each in query_results:
            if username.data == each[0]:
                exists = True
        if exists:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        conn = db.connect()
        query_results = conn.execute("Select email from users;").fetchall()
        conn.close()
        exists = False
        for each in query_results:
            if email.data == each[0]:
                exists = True
        if exists:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
