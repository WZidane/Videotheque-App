from flask import Blueprint, render_template, request, redirect
from client import Client
from utils.locale import get_locale

catalog = Blueprint('catalog', __name__, template_folder='templates')

@catalog.route('/catalog')
def catalog_():
    return render_template('catalog.html')

@catalog.route('/search', methods=['POST'])
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

@catalog.route('/search_results', methods=['GET'])
def search_results():

    query = request.args.get('input')
    filter_type = request.args.get('filter_type')
    
    if not query:
        return redirect(request.referrer)
    
    return render_template('catalog.html', query=query, filter_type=filter_type)