import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import tmdb
from config import TELEGRAM_BOT_TOKEN

router = Router()


@router.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer('Hi')


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    async with tmdb.get_new_client() as client:
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())