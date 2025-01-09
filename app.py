import secrets, textwrap
from flask import Flask, redirect, url_for
from flask_babel import Babel, _
from client import Client
from utils.locale import get_locale

from blueprints.home import home
from blueprints.catalog import catalog
from blueprints.auth import auth
from blueprints.contact import contact

app = Flask(__name__, template_folder='blueprints/templates')

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = secrets.token_hex(32)

babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

@app.template_filter('shorten')
def shorten_text(text, width=100, placeholder="..."):
    return textwrap.shorten(text, width=width, placeholder=placeholder)

@app.route('/change_language/', methods=['GET'])
def change_language():
    session['lang'] = request.args.get('lang')
    return redirect(request.referrer)

@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('home.home_'))

app.register_blueprint(home)
app.register_blueprint(catalog)
app.register_blueprint(auth)
app.register_blueprint(contact)

@app.route('/test', methods=['GET'])
def test():
    # response = Client.getTrends("week", get_locale())
    response = Client.searchActors("Tom", language=get_locale())
    return response