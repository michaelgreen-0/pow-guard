import pytest
from unittest.mock import MagicMock
from src.services.challenger import Challenger


@pytest.fixture
def redis_mock():
    return MagicMock()


@pytest.fixture
def challenger(redis_mock):
    return Challenger(redis=redis_mock, ip="127.0.0.1")


def test_generate_challenge_length_and_charset():
    challenge = Challenger.generate_challenge()
    assert len(challenge) == 16
    assert all(c.isalnum() for c in challenge)


def test_save_challenge_sets_value(challenger, redis_mock):
    challenge = "abc123XYZ"
    challenger.save_challenge(challenge, time=300)
    redis_mock.setex.assert_called_once_with("challenge:127.0.0.1", 300, challenge)


def test_get_challenge_returns_value(challenger, redis_mock):
    redis_mock.get.return_value = b"abc123XYZ"
    result = challenger.get_challenge()
    redis_mock.get.assert_called_once_with("challenge:127.0.0.1")
    assert result == b"abc123XYZ"
