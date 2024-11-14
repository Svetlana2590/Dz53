from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import SubmitField, StringField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    pasword = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=4)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')