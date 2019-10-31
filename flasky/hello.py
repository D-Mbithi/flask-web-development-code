from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Flask</h2>'


@app.route('/user/<username>')
def user(username):
    return '<h2> Hello, {}. Welcome to flasky'.format(username)


@app.route('/agent')
def agent():
    user_agent = request.headers.get('User-agent')
    return '<p> Your browser is {}</p>'.format(user_agent)


@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = load_user(user_id)

    if not user:
        abort(404)
    return '<h2>Hello, {}</h2>'.format(user)
