
import requests

def get_movie_details(movie_title, api_key):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    plot = data.get('Plot', 'N/A')
    poster = data.get('Poster', 'N/A')
    return plot, poster
