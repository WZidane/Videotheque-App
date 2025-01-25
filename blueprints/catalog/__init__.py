from flask import Blueprint, render_template, request, redirect, url_for
from client import Client
from utils.locale import get_locale
from utils.connected import isConnected

catalog = Blueprint('catalog', __name__, template_folder='templates')

@catalog.route('/catalog')
def catalog_():

    connected = isConnected()

    res = Client.getGenres()

    if 'isConnected' in connected and connected['isConnected'] == True:
        return render_template('catalog.html', data=res, nav=0)
    else:
        return render_template('catalog.html', data=res, nav=1)

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

    connected = isConnected()

    query = request.args.get('input')
    filter_type = request.args.get('filter_type')
    res = Client.getGenres(get_locale())
    
    if not query:
        return redirect(request.referrer)
    
    if 'isConnected' in connected and connected['isConnected'] == True:
        return render_template('catalog.html', query=query, filter_type=filter_type, data=res, nav=0)
    else:
        return render_template('catalog.html', query=query, filter_type=filter_type, data=res, nav=1)
    

@catalog.route('/catalog/genre/<id>', methods=['GET'])
def catalog_genre(id):

    result = Client.getMoviesByGenre(id)
    res = Client.getGenres(get_locale())
    genre = result['results']

    connected = isConnected()

    if 'isConnected' in connected and connected['isConnected'] == True:
        return render_template('catalog.html', data=res, data_genre=genre, id_genre=int(id), nav=0)
    else:
        return render_template('catalog.html', data=res, data_genre=genre, id_genre=int(id), nav=1)