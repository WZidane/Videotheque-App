import secrets
from flask import Flask, render_template, request, redirect, session
from flask_babel import Babel, _

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = secrets.token_hex(32)

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'fr')

babel = Babel(app, locale_selector=get_locale)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/catalog', methods=['GET'])
def catalog():
    return render_template('catalog.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/change_language/', methods=['GET'])
def change_language():
    session['lang'] = request.args.get('lang')
    return redirect(request.referrer)