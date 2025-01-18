from flask import Blueprint, render_template
from client import Client
from utils.locale import get_locale

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/')
def home_():
    response = Client.getTrends("week", get_locale())
    return render_template('home.html', data=response.json())