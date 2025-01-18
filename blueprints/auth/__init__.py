from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')