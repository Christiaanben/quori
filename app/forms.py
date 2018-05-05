from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form, TextField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')


# class SearchForm(Form):
#     autocomp= StringField('autocomp',id='autocomplete')