from datetime import date

import requests

from config import TMDB_TOKEN

TMDB_API_URL = 'https://api.themoviedb.org/3'

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {TMDB_TOKEN}'})


def _tmdb_get(path: str, params: dict | None = None) -> dict:
    response = session.get(
        TMDB_API_URL + path,
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_tv_show_by_name(name: str) -> list[dict]:
    data = _tmdb_get('/search/tv', params={'query': name})
    searched_shows = [
        {
            'id': show['id'],
            'name': show['name'],
            'first_air_date': show.get('first_air_date'),
        }
        for show in data['results']
    ]
    return searched_shows


def _parse_date(string_date: str | None) -> date | None:
    if not string_date:
        return None
    return date.fromisoformat(string_date)


def _parse_episode_info(episode: dict | None) -> dict | None:
    if not episode:
        return None
    parsed_episode = {
        'air_date': _parse_date(episode.get('air_date')),
        'episode_number': episode['episode_number'],
        'season_number': episode['season_number'],
    }
    return parsed_episode


def get_details_about_tv_show(tv_show_id: int) -> dict:
    data = _tmdb_get(f'/tv/{tv_show_id}')
    details = {
        'name': data['name'],
        'status': data['status'],
        'last_episode_to_air': _parse_episode_info(data['last_episode_to_air']),
        'next_episode_to_air': _parse_episode_info(data['next_episode_to_air']),
    }
    return details
