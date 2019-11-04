from flask import (
        Flask, request, abort, render_template, session, redirect, url_for, flash
        )
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'QCQweaC53r4l8Bd5NZ3#HM2WDp8jCyXz&*FL3hzmCAebAByU8SaM@C7CS^1P&'


Bootstrap(app)


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
        old_name = session.get('name')
        if old_name is not None or old_name != form.name.data:
            flash('It seems you have changed your name.')
        session['name'] = form.name.data
        return redirect(url_for('user'))
    return render_template('user.html', form=form, name=session.get('name'))


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
