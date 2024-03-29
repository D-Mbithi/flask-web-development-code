from flask import render_template, redirect, request, flash, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_required, logout_user, login_user
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            print('User valid')
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(url_for('main.index'))
        flash('Invalid user or password')
        print('Invalid user or password.')
    print('Form not validated.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You can now login')

        return redirect(url_for('auth.login'))
    print('Forma not valid')
    return render_template('auth/register.html', form=form)
