import requests;

class Client:

    def searchMovies(query, page=1):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Yzk3M2M3NTNjMmNlNTFiNjJkN2JiMWY3MTczY2Y4OSIsIm5iZiI6MTczNDEwMDQ1NC4zNjA5OTk4LCJzdWIiOiI2NzVjNDVlNjZhODAwM2I2M2JiN2EyZjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.W8NKYICiTLrmn7Hf_IL2wmTkWfAAL6r2FZJcZntrAE4"
        }
        response = requests.get('https://api.themoviedb.org/3/search/movie', {'query': query, 'language': 'fr', 'page': page}, headers= headers)
        return response
    
    def getMovie(id):
        url = f"https://api.themoviedb.org/3/movie/{id}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Yzk3M2M3NTNjMmNlNTFiNjJkN2JiMWY3MTczY2Y4OSIsIm5iZiI6MTczNDEwMDQ1NC4zNjA5OTk4LCJzdWIiOiI2NzVjNDVlNjZhODAwM2I2M2JiN2EyZjkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.W8NKYICiTLrmn7Hf_IL2wmTkWfAAL6r2FZJcZntrAE4"
        }

        response = requests.get(url, {'language': 'fr'}, headers=headers)
        return response