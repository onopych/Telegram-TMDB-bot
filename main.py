import asyncio
import logging

from aiogram import Bot, Dispatcher

from tmdb import get_new_client
from config import TELEGRAM_BOT_TOKEN
from handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    async with get_new_client() as client:
        await dp.start_polling(bot, tmdb_client=client)


if __name__ == '__main__':
    asyncio.run(main())
