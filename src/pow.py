import hashlib
import random
import string

def generate_challenge():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def verify_pow(challenge, solution, difficulty):
    guess = f"{challenge}{solution}".encode()
    hashed = hashlib.sha256(guess).hexdigest()
    return hashed.startswith("0" * difficulty)