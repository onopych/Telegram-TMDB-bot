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


def _parse_date(string_date: str | None) -> date | None:
    if not string_date:
        return None
    return date.fromisoformat(string_date)


def _extract_year(string_date: str | None) -> str | None:
    parsed_date = _parse_date(string_date)
    return str(parsed_date.year) if parsed_date is not None else None


def multi_search(name: str) -> list[dict]:
    data = _tmdb_get('/search/multi', params={'query': name})
    results = []
    for item in data['results']:
        parsed_item = {
            'id': item['id'],
            'media_type': item['media_type'],
            'name': item.get('title') or item.get('name'),
        }
        if item['media_type'] == 'tv':
            parsed_item['subtitle'] = _extract_year(item.get('first_air_date'))
        elif item['media_type'] == 'movie':
            parsed_item['subtitle'] = _extract_year(item.get('release_date'))
        elif item['media_type'] == 'person':
            parsed_item['subtitle'] = item.get('known_for_department')
        else:
            continue
        results.append(parsed_item)

    return results


def _parse_episode_info(episode: dict | None) -> dict | None:
    if not episode:
        return None
    parsed_episode = {
        'air_date': _parse_date(episode.get('air_date')),
        'episode_number': episode['episode_number'],
        'season_number': episode['season_number'],
        'name': episode['name'],
    }
    return parsed_episode


def _get_details_about_tv_show(tv_show_id: int) -> dict:
    data = _tmdb_get(f'/tv/{tv_show_id}')
    details = {
        'name': data['name'],
        'status': data['status'],
        'overview': data['overview'],
        'release_date': _parse_date(data.get('first_air_date')),
        'number_of_episodes': data['number_of_episodes'],
        'number_of_seasons': data['number_of_seasons'],
        'last_episode_to_air': _parse_episode_info(data['last_episode_to_air']),
        'next_episode_to_air': _parse_episode_info(data['next_episode_to_air']),
    }
    return details


def _get_details_about_movie(movie_id: int) -> dict:
    data = _tmdb_get(f'/movie/{movie_id}')
    details = {
        'name': data['title'],
        'status': data['status'],
        'runtime': data['runtime'],
        'release_date': _parse_date(data.get('release_date')),
        'overview': data['overview'],
        'budget': data.get('budget'),
    }
    return details


def _calculate_age(birthday: date | None, deathday: date | None) -> int | None:
    if not birthday:
        return None
    end = deathday or date.today()
    birthday_not_yet_this_year = ((end.month, end.day)
                                  < (birthday.month, birthday.day))
    return end.year - birthday.year - birthday_not_yet_this_year


def _get_details_about_person(person_id: int) -> dict:
    data = _tmdb_get(f'/person/{person_id}')
    birthday = _parse_date(data.get('birthday'))
    deathday = _parse_date(data.get('deathday'))
    details = {
        'name': data['name'],
        'age': _calculate_age(birthday, deathday),
        'birthday': birthday,
        'is_dead': deathday is not None,
        'deathday': deathday,
        'known_for_department': data['known_for_department'],
        'biography': data['biography'],
        'place_of_birth': data['place_of_birth'],
    }
    return details


_DETAILS_GETTERS = {
    'tv': _get_details_about_tv_show,
    'movie': _get_details_about_movie,
    'person': _get_details_about_person,
}


def get_details(item: dict) -> dict:
    details_getter = _DETAILS_GETTERS.get(item['media_type'])
    if details_getter is None:
        raise ValueError(f'Invalid media type: {item["media_type"]}')
    return details_getter(item['id'])
