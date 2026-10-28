from datetime import date

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


def parse_date(string_date: str | None) -> date | None:
    if not string_date:
        return None
    return date.fromisoformat(string_date)


def parse_episode_info(episode: dict | None) -> dict | None:
    if not episode:
        return None
    parsed_episode = {
        'air_date': parse_date(episode.get('air_date')),
        'episode_number': episode['episode_number'],
        'season_number': episode['season_number'],
    }
    return parsed_episode


def get_details_about_tv_show(tv_show_id: int) -> dict:
    response = session.get(
        TMDB_API_URL + f'/tv/{tv_show_id}',
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    details = {
        'name': data['name'],
        'status': data['status'],
        'last_episode_to_air': parse_episode_info(data['last_episode_to_air']),
        'next_episode_to_air': parse_episode_info(data['next_episode_to_air']),
    }
    return details
