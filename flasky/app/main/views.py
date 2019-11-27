from datetime import datetime
from flask import render_template, redirect, url_for, session
from flask_login import login_required

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        current=datetime.utcnow()
    )


@main.route('/secret')
def secret():
    return 'Only authenticated users can view'
