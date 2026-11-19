import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import httpx

from tmdb import multi_search


router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer('Hi, type anything you want '
                         'to find in the movie world')


def _make_search_answer_for_user(search_results: list[dict]) -> str:
    string_list = []
    for result in search_results:
        media_type_for_user = ('series' if result['media_type'] == 'tv'
                               else result['media_type'])
        subtitle_for_user = ('' if not result['subtitle']
                             else f' ({result["subtitle"]})')
        string_result = (f'{result["name"]}{subtitle_for_user} - '
                         f'{media_type_for_user}')
        string_list.append(string_result)
    return '\n\n'.join(string_list)


@router.message(F.text)
async def on_text(message: Message, tmdb_client: httpx.AsyncClient) -> None:
    try:
        tmdb_results = await multi_search(tmdb_client, message.text)
    except httpx.HTTPError:
        logger.exception('Failed to make TMDB multi search for %s',
                         message.text)
        await message.answer('Something went wrong while searching. '
                             'Please try again later.')
        return
    if not tmdb_results:
        await message.answer('There are no search results for '
                             f'{message.text}')
        return
    await message.answer(f'Search results for {message.text}:')
    await message.answer(_make_search_answer_for_user(tmdb_results))
