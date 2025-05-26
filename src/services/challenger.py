import random
import string
from redis import Redis


class Challenger:
    def __init__(self, redis: Redis, ip: str):
        self.redis = redis
        self.ip = ip

    @staticmethod
    def generate_challenge():
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

    def save_challenge(self, challenge: str, time: int = 300):
        self.redis.set(f"challenge:{self.ip}", challenge, ex=time)

    def get_challenge(self):
        return self.redis.get(f"challenge:{self.ip}")
