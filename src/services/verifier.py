import hashlib
from redis import Redis


class Verifier:
    def __init__(self, redis: Redis, challenge_id: str):
        self.redis = redis
        self.challenge_id = challenge_id

    @staticmethod
    def verify_pow(challenge: str, solution: str, difficulty: int) -> bool:
        guess = f"{challenge}{solution}".encode()
        hashed = hashlib.sha256(guess).hexdigest()
        return hashed.startswith("0" * difficulty)

    def mark_verified(self, time: int = 300):
        return self.redis.set(f"verified:{self.challenge_id}", "1", ex=time)

    def is_verified(self):
        return self.redis.exists(f"verified:{self.challenge_id}")
