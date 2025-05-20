import os
from dotenv import load_dotenv
from os import environ

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
BACKEND_URL = os.getenv("BACKEND_URL")
# POW_DIFFICULTY = int(os.getenv("POW_DIFFICULTY"))
POW_DIFFICULTY = int(environ["POW_DIFFICULTY"])
