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
    def searchMovies(cls, query, page=1, language="fr"):
        response = requests.get('https://api.themoviedb.org/3/search/movie', {'query': query, 'language': language, 'page': page}, headers= cls.headers)
        return response
    
    @classmethod
    def getMovie(cls, id, language="fr"):
        url = f"https://api.themoviedb.org/3/movie/{id}"

        response = requests.get(url, {'language': language}, headers=cls.headers)
        return response