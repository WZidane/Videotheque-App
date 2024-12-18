import requests;
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

class Client:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_KEY')}"
    }

    @classmethod
    def searchMovies(cls, query, page=1):
        response = requests.get('https://api.themoviedb.org/3/search/movie', {'query': query, 'language': 'fr', 'page': page}, headers= cls.headers)
        return response
    
    @classmethod
    def getMovie(cls, id):
        url = f"https://api.themoviedb.org/3/movie/{id}"

        response = requests.get(url, {'language': 'fr'}, headers=cls.headers)
        return response