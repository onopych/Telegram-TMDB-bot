import os
from dotenv import load_dotenv

load_dotenv()
TMDB_TOKEN = os.getenv('TMDB_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TMDB_TOKEN:
    raise RuntimeError('There is no TMDB_TOKEN in .env')
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError('There is no TELEGRAM_BOT_TOKEN in .env')