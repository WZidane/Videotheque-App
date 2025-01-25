from flask import Blueprint, render_template, redirect, url_for
from client import Client
from utils.locale import get_locale
from utils.connected import isConnected
import requests

movie = Blueprint('movie', __name__, template_folder='templates')


def getMovieDB(id):

    query = f"http://host.docker.internal:5001/api/movie/{id}"

    response = requests.get(query)
    
    return response.json()

def createMovieDB(id):

    request1 = Client.getMovie(id, "fr")
    request2 = Client.getMovie(id, "en")

    title_fr = request1['title']

    title_en = request2['title']

    country = request1['origin_country'][0]

    synopsis_fr = request1['overview']

    synopsis_en = request2['overview']

    release_date = request1['release_date']

    poster = request1['poster_path']

    data = {'id': id, 'title_fr': title_fr, 'title_en': title_en, 'country': country, 'synopsis_fr': synopsis_fr, 'synopsis_en': synopsis_en, 'poster': poster, 'release_date': release_date}

    query = "http://host.docker.internal:5001/api/movie/"

    response = requests.post(query, headers={"Content-Type": "application/json"}, json=data)

    return response

def getGenres(response):
    
    genres = []

    for i in range(len(response['genres'])):
        genres.append(response['genres'][i]['name'])

    genre = ", ".join(genres) + "."

    return genre

@movie.route('/movie/<id>', methods=['GET'])
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
            actors = Client.getCredits(id, get_locale())

            data_actors = []

            for person in actors.get('crew', []):
                if person.get('job') == 'Director':
                    director_id = person.get('id')
                    director_name = person.get('name')
                    director_profile = person.get('profile_path')

            for person in actors.get('cast', []):
                actor_id = person.get('id')
                actor_name = person.get('name')
                actor_profile = person.get('profile_path')
                data_actors.append({'actor_id': actor_id, 'actor_name': actor_name, 'actor_profile': actor_profile})
            
            act = {}

            act['Actors'] = data_actors

            connected = isConnected()

            if 'isConnected' in connected and connected['isConnected'] == True:
                return render_template('movie.html', data=res, genres=genre, director_id=director_id, director_name=director_name, director_profile=director_profile, data_actors=act['Actors'], nav=0)
            else:
                return render_template('movie.html', data=res, genres=genre, director_id=director_id, director_name=director_name, director_profile=director_profile, data_actors=act['Actors'], nav=1)

@movie.route('/person/<id>', methods=['GET'])
def person_(id):

    res = Client.getPerson(id, get_locale())

    if(res.get('success')  == False):
        
        return redirect(url_for('home.home_'))
    
    else:
        connected = isConnected()

        request = Client.getMoviesByActor(id, get_locale())

        if 'isConnected' in connected and connected['isConnected'] == True:
            return render_template('person.html', data=res, data_movies=request['results'], nav=0)
        else:
            return render_template('person.html', data=res, data_movies=request['results'], nav=1)