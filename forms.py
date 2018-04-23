#encoding: utf-8

import wtforms
from models import UserModel
from wtforms import validators, StringField, BooleanField, SubmitField, PasswordField
from wtforms import ValidationError

class RegistForm(wtforms.Form):
	email = StringField('Email', validators = [validators.InputRequired(),validators.length(1,64),validators.Email()])
	username = StringField('Username', validators = [validators.InputRequired(message=u'请输入用户名')])
	password1 = StringField(validators = [validators.InputRequired()])
	password2 = StringField(validators = [validators.InputRequired(),validators.EqualTo('password1')])
	submit = SubmitField('RegistForm')

class LoginForm(wtforms.Form):
	email = StringField('Email', validators = [validators.InputRequired(),validators.length(1,64),validators.Email()])
	password = PasswordField('Password', validators = [validators.InputRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('log in')
