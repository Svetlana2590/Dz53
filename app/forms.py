from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import SubmitField, StringField, PasswordField, BooleanField


class KupitForm(FlaskForm):
    kolvo=StringField('Kolvo', validators=[DataRequired()])
    submit=SubmitField('Купить')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    pasword = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=4)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class TovarForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    price = StringField('Price', validators=[DataRequired(), Length(min=1, max=6)])
    ostatok = StringField('Ostatok')
    submit = SubmitField('Add tovar')