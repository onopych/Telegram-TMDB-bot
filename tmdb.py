import requests

from config import TMDB_TOKEN

TMDB_API_URL = 'https://api.themoviedb.org/3'

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {TMDB_TOKEN}'})


def search_tv_show_by_name(name: str) -> list[dict]:
    response = session.get(
        TMDB_API_URL + '/search/tv',
        params={'query': name},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    searched_shows = [
        {
            'id': show['id'],
            'name': show['name'],
            'first_air_date': show.get('first_air_date'),
        }
        for show in data['results']
    ]
    return searched_shows
