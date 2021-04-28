from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
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

class ReviewsForm(FlaskForm):
    # username = LOGGED_USER
    title = StringField('Restaurant Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    content  = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    food_rating = IntegerField('Food Rating', validators=[
                                               DataRequired(), NumberRange(min=1, max=10, message='Enter a number between 1-10')])
    convenience_rating = IntegerField('Convenience Rating', validators=[
                                               DataRequired(), NumberRange(min=1, max=10, message='Enter a number between 1-10')])
    meal_cost = FloatField('Meal Cost', validators=[
                                               DataRequired(), NumberRange(min=1, max=100, message='Enter a number between 1-100')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[
                                    DataRequired(), Length(min=2, max=20)])
    search = SubmitField('Search')

LOGGED_USER = 'empty'
