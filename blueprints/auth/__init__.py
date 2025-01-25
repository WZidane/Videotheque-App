from flask import Blueprint, render_template, url_for, redirect, request, jsonify, make_response
from utils.locale import get_locale
from utils.connected import isConnected
import requests

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/signup', methods=['GET'])
def signup_():

        res = isConnected()

        if 'isConnected' in res and res['isConnected'] == True:
            return redirect(url_for('home.home_'))
        else:
            return render_template('signup.html')

@auth.route('/login', methods=['GET'])
def login_():

    error = request.args.get("error")

    res = isConnected()

    if(error):
        return render_template('login.html', err=error)
    else:
        if 'isConnected' in res and res['isConnected'] == True:
            return redirect(url_for('home.home_'))
        else:
            return render_template('login.html')

@auth.route('/register', methods=['POST'])
def register():

    query = f"http://host.docker.internal:5001/api/user/"

    username = request.form.get('username')

    password = request.form.get('password')

    email = request.form.get('email')

    data = {'username': username, 'password': password, 'email': email}

    response = requests.post(query, json=data, headers={"Content-Type": "application/json"})

    return render_template('register.html', username=username)

@auth.route('/check_login', methods=['POST'])
def check_login():

    query = f"http://host.docker.internal:5001/api/login/"

    error = "Adresse e-mail ou mot de passe incorrect !"

    if(get_locale() == "en"):
        error = "Wrong e-mail or password!"

    password = request.form.get('password')

    email = request.form.get('email')

    data = {'password': password, 'email': email}

    response = requests.post(query, json=data, headers={"Content-Type": "application/json"})

    res = response.json()

    cookie = make_response(redirect(url_for("auth.profile")))

    if 'access_token' in res:
        cookie.set_cookie("filmotek_tk", res['access_token'], max_age=60*60*24, secure=False)
        return cookie
    else:
        return redirect(url_for('auth.login_', error=error))


@auth.route('/profile', methods=['GET'])
def profile():

    res = isConnected()

    error = "Vous n'êtes pas connecté !"

    if(get_locale() == "en"):
        error = "You must login!"

    if 'isConnected' in res and res['isConnected'] == True:

        query = f"http://host.docker.internal:5001/api/collection"

        token = request.cookies.get("filmotek_tk")

        response = requests.get(query, json={'language': get_locale()}, headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})

        return render_template('profile.html', data=response.json())
    else:
        return redirect(url_for('auth.login_', error=error))

@auth.route('/logout', methods=['GET'])
def logout():

    res = isConnected()

    if 'isConnected' in res and res['isConnected'] == True:
        cookie = make_response(redirect(url_for('home.home_')))
        cookie.delete_cookie("filmotek_tk")
        return cookie
    else:
        return redirect(url_for('home.home_'))