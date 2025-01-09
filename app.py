import secrets, textwrap, re
from flask import Flask, render_template, request, redirect, session
from flask_babel import Babel, _
from client import Client

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

@app.template_filter('shorten')
def shorten_text(text, width=100, placeholder="..."):
    return textwrap.shorten(text, width=width, placeholder=placeholder)

@app.route('/', methods=['GET'])
def index():
    response = Client.getTrends("week", get_locale())
    return render_template('index.html', data=response.json())

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

@app.route('/search', methods=['POST'])
def search():

    data = request.get_json()
    query = data.get('query')
    filter_type = data.get('filter_type')

    if filter_type == '1':  # Titre
        response = Client.searchMovies(query, language=get_locale())
    elif filter_type == '2':  # Acteurs
        response = Client.searchActors(query, language=get_locale())
    elif filter_type == '3':  # Réalisateur
        response = Client.searchDirectors(query, language=get_locale())

    return response

@app.route('/test', methods=['GET'])
def test():
    # response = Client.getTrends("week", get_locale())
    response = Client.searchActors("Tom", language=get_locale())
    return response