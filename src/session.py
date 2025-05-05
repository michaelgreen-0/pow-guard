import redis
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def save_challenge(ip, challenge):
    r.setex(f"challenge:{ip}", 300, challenge)

def get_challenge(ip):
    return r.get(f"challenge:{ip}")

def mark_verified(ip):
    r.setex(f"verified:{ip}", 300, "1")

def is_verified(ip):
    return r.exists(f"verified:{ip}")