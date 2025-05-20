import hashlib
from redis import Redis


class Verifier:
    def __init__(self, redis: Redis, ip: str):
        self.redis = redis
        self.ip = ip

    def verify_pow(self, challenge: str, solution: str, difficulty: int) -> bool:
        guess = f"{challenge}{solution}".encode()
        hashed = hashlib.sha256(guess).hexdigest()
        return hashed.startswith("0" * difficulty)

    def mark_verified(self, time: int = 300):
        return self.redis.setex(f"verified:{self.ip}", time, "1")

    def is_verified(self):
        return self.redis.exists(f"verified:{self.ip}")
