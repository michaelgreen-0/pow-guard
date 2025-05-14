from redis import Redis
from ..env import REDIS_HOST, REDIS_PORT


def get_redis():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
