import hashlib
from redis import Redis


class Verifier:
    def __init__(self, redis: Redis, event_key: str):
        self.redis = redis
        self.event_key = event_key

    @staticmethod
    def verify_pow(challenge: str, solution: str, difficulty: int) -> bool:
        guess = f"{challenge}{solution}".encode()
        hashed = hashlib.sha256(guess).hexdigest()
        return hashed.startswith("0" * difficulty)

    def mark_verified(self, time: int = 300):
        return self.redis.set(f"verified:{self.event_key}", "1", ex=time)

    def is_verified(self):
        return self.redis.exists(f"verified:{self.event_key}")
