import random
import string
from ..utils.redis import get_redis


class Challenger:
    def __init__(self, challenge_id: str):
        self.redis = get_redis()
        self.challenge_id = challenge_id

    @staticmethod
    def generate_challenge():
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

    def save_challenge(self, challenge: str, time: int = 300):
        self.redis.set(f"challenge:{self.challenge_id}", challenge, ex=time)

    def get_challenge(self):
        return self.redis.get(f"challenge:{self.challenge_id}")
