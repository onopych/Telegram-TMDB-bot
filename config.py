import os
from dotenv import load_dotenv

load_dotenv()
TMDB_TOKEN = os.getenv('TMDB_TOKEN')

if not TMDB_TOKEN:
    raise RuntimeError('There is no TMDB_TOKEN in .env')