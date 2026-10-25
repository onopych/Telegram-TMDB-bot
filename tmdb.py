from config import TMDB_TOKEN
import requests

TMDB_API_URL = 'https://api.themoviedb.org/3'

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {TMDB_TOKEN}'})
