from flask import Blueprint, render_template
from client import Client
from utils.locale import get_locale
from utils.connected import isConnected

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/')
def home_():
    response = Client.getTrends("week", get_locale())
    connected = isConnected()

    if 'isConnected' in connected and connected['isConnected'] == True:
        return render_template('home.html', data=response.json(), nav=0)
    else:
        return render_template('home.html', data=response.json(), nav=1)