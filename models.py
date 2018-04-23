#encoding: utf-8

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
import datetime
from flask_login import UserMixin, LoginManager
from flask import Flask, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(64),index=True)
    _password = db.Column(db.String(100),nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    aboutme = db.Column(db.Text)

    def __init__(self,*args,**kwargs):
        password = kwargs.pop('password')
        username = kwargs.pop('username')
        email = kwargs.pop('email')
        confirmed = kwargs.pop('confirmed')
        aboutme = kwargs.pop('aboutme')
        self.confirmed = confirmed
        self.password = password
        self.username = username
        self.email = email
        self.aboutme = aboutme

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(app.congfig['SECRET_KEY'])

        try:
           data = s.loads(token)
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def send_async_email(app,msg):
        with app.app_context():
            mail.send(msg)


class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.String(100),db.ForeignKey('users.id'))

    author = db.relationship('UserModel',backref='questions')

class AnswerModel(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('users.id'))
    question = db.relationship('QuestionModel',backref=db.backref('answers',order_by=create_time.desc()))
    author = db.relationship('UserModel',backref='answers')

class ReplyModel(db.Model):
    __tablename__ = 'replys'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    answer_id = db.Column(db.Integer,db.ForeignKey('answers.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('users.id'))
    answer = db.relationship('AnswerModel',backref=db.backref('replys',order_by=create_time.desc()))
    author = db.relationship('UserModel',backref='replys')
