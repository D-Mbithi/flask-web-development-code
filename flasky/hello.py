from flask import Flask, request, abort, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<username>')
def user(username):

    name = username
    return render_template('user.html', name=name)


@app.route('/agent')
def agent():
    user_agent = request.headers.get('User-agent')
    return '<p> Your browser is {}</p>'.format(user_agent)


@app.route('/user/<int:user_id>')
def get_user(user_id):
#    user = load_user(user_id)

    if not user:
        abort(404)
    return '<h2>Hello, {}</h2>'.format(user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404 


@app.errorhandler(500)
def internal_server_erro(e):
    return render_template('500.html'), 500
