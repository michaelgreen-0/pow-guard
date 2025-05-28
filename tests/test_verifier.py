import hashlib
from unittest.mock import MagicMock
import pytest
from src.services.verifier import Verifier


@pytest.fixture
def redis_mock():
    return MagicMock()


@pytest.fixture
def verifier(redis_mock):
    return Verifier(redis=redis_mock, challenge_id="abc123")


def test_verify_pow_success(verifier):
    challenge = "abc"
    difficulty = 2

    i = 0
    while True:
        solution_try = str(i)
        guess = f"{challenge}{solution_try}".encode()
        hashed = hashlib.sha256(guess).hexdigest()
        if hashed.startswith("0" * difficulty):
            break
        i += 1

    assert verifier.verify_pow(challenge, solution_try, difficulty) is True


def test_verify_pow_failure(verifier):
    assert verifier.verify_pow("abc", "wrong", 4) is False


def test_mark_verified_sets_key(verifier, redis_mock):
    time = 300
    redis_mock.set.return_value = True
    result = verifier.mark_verified(time=time)
    redis_mock.set.assert_called_once_with("verified:abc123", "1", ex=time)
    assert result is True


def test_is_verified_true(verifier, redis_mock):
    redis_mock.exists.return_value = True
    assert verifier.is_verified() is True
    redis_mock.exists.assert_called_once_with("verified:abc123")


def test_is_verified_false(verifier, redis_mock):
    redis_mock.exists.return_value = False
    assert verifier.is_verified() is False
    redis_mock.exists.assert_called_once_with("verified:abc123")
