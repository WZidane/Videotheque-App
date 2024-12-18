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
    
    @classmethod
    def getMoviesByDirector(cls, query, page=1, language="fr"):
        # Resquest to search persons
        personResponse = requests.get('https://api.themoviedb.org/3/search/person', {'query': query}, headers=cls.headers)
        data= personResponse.json()
        directors = []
        if data.get("total_results") > 0 :
            for person in data.get("results", []):
                # Retrieve the ids of only the directors in the list
                if person.get("known_for_department") == "Directing":
                    directors.append(person["id"])
            if(len(directors)> 0):
                # json where all results will be stored
                data = []
                # count of the results
                total_results = 0
                for director in directors:
                    # Request to get the films the director worked on
                    url = f"https://api.themoviedb.org/3/person/{director}/movie_credits"
                    response = requests.get(url, {'language': language, 'page': 1}, headers=cls.headers)
                    dataMovieCredits= response.json()
                    # Only retrieves the movies where the director worked as a director
                    for movie in dataMovieCredits.get("crew", []): 
                        if movie.get("job") == "Director":
                            data.append(movie)
                            total_results += 1
                json_results = {
                    "total_results" : total_results,
                    "results" : data
                }
                return json_results
        return None
