import os
from threading import Thread

from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask, request, render_template, session, redirect, url_for
)
# from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Message, Mail

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Flask App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'flask.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'QCQweaC53r4l8Dp8jCyXz&*FL3hzmCAebAByU8SaM@C7CS^1P&'


# Configure Mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <mbaamutendwa@gmail.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


# Bootstrap(app)
class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):

    __users__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Sibmit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/', methods=['GET', 'POST'])
def user():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(
                    app.config['FLASKY_ADMIN'],
                    'New user',
                    'mail/new_user',
                    user=user
                )
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user'))
    return render_template(
        'user.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False)
    )


@app.route('/agent')
def agent():
    user_agent = request.headers.get('User-agent')
    return render_template('agent.html', user_agent=user_agent)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_erro(e):
    return render_template('500.html'), 500


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
        sender=app.config['FLASKY_MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_asyc_email, args=[app, msg])
    thr.start()
    return thr
