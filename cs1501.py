#encoding: utf-8

from flask import Flask,flash,render_template
from exts import db
import flask
import config
from forms import RegistForm, LoginForm
from models import UserModel,QuestionModel,AnswerModel,ReplyModel
from decorators import login_required
from sqlalchemy import or_
from flask_login import LoginManager,current_user
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# 邮箱验证
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '458861529@qq.com'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
mail = Mail(app)

app.config.from_object(config)
db.init_app(app)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/')
def index():
    context = {
        'questions': QuestionModel.query.all()
    }
    return flask.render_template('index.html',**context)

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if flask.request.method == 'GET':
        return flask.render_template('question.html')
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        question_model = QuestionModel(title=title,content=content)
        question_model.author = flask.g.user
        db.session.add(question_model)
        db.session.commit()
        return flask.redirect(flask.url_for('index'))

@app.route('/d/<id>/')
def detail(id):
    question_model = QuestionModel.query.get(id)
    return flask.render_template('detail.html',question=question_model)

@app.route('/comment/',methods=['POST'])
@login_required
def comment():
    question_id = flask.request.form.get('question_id')
    content = flask.request.form.get('content')
    answer_model = AnswerModel(content=content)
    answer_model.author = flask.g.user
    answer_model.question = QuestionModel.query.get(question_id)
    db.session.add(answer_model)
    db.session.commit()
    return flask.redirect(flask.url_for('detail',id=question_id))

@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q)))
    context = {
        'questions': questions
    }
    return flask.render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        form = LoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and user.check_password(password):
                flask.session['id'] = user.id
                flask.g.user = user
                return flask.redirect(flask.url_for('index'))
            else:
                return '用户名或密码错误，请重新输入！'

@app.route('/logout/',methods=['GET'])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template('regist.html')
    else:
        form = RegistForm(flask.request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            confirmed = False
            aboutme = "这个人很懒。。。"
            user = UserModel(email=email,username=username,password=password,confirmed=confirmed,aboutme=aboutme)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, 'confirm your account','confirm', user=user, token=token)
            flash('A confimed email has been sent via email')
            return flask.redirect(flask.url_for('login'))

@app.route('/reply/',methods=['POST'])
@login_required
def reply():
    answer_id = flask.request.form.get('answer_id')
    content = flask.request.form.get('answer_content')
    reply_model = ReplyModel(content=content)
    reply_model.author = flask.g.user
    reply_model.answer = AnswerModel.query.get(answer_id)
    reply_model.answer.question = QuestionModel.query.get(reply_model.answer.question_id)
    db.session.add(reply_model)
    db.session.commit()
    return flask.redirect(flask.url_for('detail',id=reply_model.answer.question_id))

@app.route('/self_info/<id>/',methods=['GET','POST'])
def self_info(id):
    user_model = UserModel.query.get(id)
    if flask.request.method == 'GET':
        return flask.render_template('self_info.html', user=user_model)
    else:
        print(flask.request.form.get('username'))
        user_model.username = flask.request.form.get('username')
        user_model.aboutme = flask.request.form.get('aboutme')
        db.session.add(user_model)
        db.session.commit()
        # return flask.redirect(flask.url_for('index'))
        return flask.render_template('self_info.html', user=user_model)

@app.before_request
def before_request():
    id = flask.session.get('id')
    if id:
        user = UserModel.query.get(id)
        flask.g.user = user

@app.context_processor
def context_processor():
    if hasattr(flask.g,'user'):
        return {"user":flask.g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run()
