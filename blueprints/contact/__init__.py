from flask import Blueprint, render_template
from utils.connected import isConnected

contact = Blueprint('contact', __name__, template_folder='templates')

@contact.route('/contact')
def contact_():

    connected = isConnected()

    if 'isConnected' in connected and connected['isConnected'] == True:
        return render_template('contact.html', nav=0)
    else:
        return render_template('contact.html', nav=1)