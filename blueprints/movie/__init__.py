from flask import Blueprint, render_template, redirect, url_for
from client import Client
from utils.locale import get_locale
import requests

movie = Blueprint('movie', __name__, template_folder='templates')


def getMovieDB(id):

    query = f"http://host.docker.internal:5001/api/movie/{id}"

    response = requests.get(query)
    
    res = response.json()

    return res

def createMovieDB(id):

    request = Client.getMovie(id)

    response = request

    title = response['title']

    country = response['origin_country'][0]

    synopsis = response['overview']

    release_date = response['release_date']

    poster = response['poster_path']

    data = {'id': id, 'title': title, 'country': country, 'synopsis': synopsis, 'poster': poster, 'release_date': release_date}

    query = "http://host.docker.internal:5001/api/movie/"

    response = requests.post(query, headers={"Content-Type": "application/json"}, json=data)

    return response

def getGenres(response):
    
    genres = []

    for i in range(len(response['genres'])):
        genres.append(response['genres'][i]['name'])

    genre = ", ".join(genres) + "."

    return genre

@movie.route('/movie/<id>')
def movie_(id):

    res = Client.getMovie(id, get_locale())

    if(res.get('success')  == False):
        
        return redirect(url_for('home.home_'))
    
    else:

        res = getMovieDB(id)

        if(res.get('error')):

            createMovieDB(id)
            
            return redirect(url_for('movie.movie_', id=id))

        else:

            genre = getGenres(Client.getMovie(id, get_locale()))

            return render_template('movie.html', data=res, genres=genre)

@movie.route('/person/<id>')
def person_(id):

    res = Client.getPerson(id, get_locale())

    if(res.get('success')  == False):
        
        return redirect(url_for('home.home_'))
    
    else:

        return render_template('person.html', data=res)