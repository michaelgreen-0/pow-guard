import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
POW_DIFFICULTY = int(os.getenv("POW_DIFFICULTY"))
COOKIE_LIFETIME = os.getenv("COOKIE_LIFETIME")
CHALLENGE_LIFETIME = os.getenv("CHALLENGE_LIFETIME")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
