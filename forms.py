from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User, Book

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=13)])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Book')

    def validate_isbn(self, isbn):
        book = Book.query.filter_by(isbn=isbn.data).first()
        if book:
            raise ValidationError('ISBN already exists.')

class BorrowForm(FlaskForm):
    submit = SubmitField('Borrow Book')

class ReturnForm(FlaskForm):
    submit = SubmitField('Return Book')