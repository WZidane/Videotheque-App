from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/catalogue', methods=['GET'])
def catalogue():
    return render_template('catalogue.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')