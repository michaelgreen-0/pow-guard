import pytest
from unittest.mock import MagicMock
from src.services.challenger import Challenger


@pytest.fixture
def redis_mock():
    return MagicMock()


@pytest.fixture
def challenger(redis_mock):
    return Challenger(redis=redis_mock, challenge_id="abc123")


def test_generate_challenge_length_and_charset():
    challenge = Challenger.generate_challenge()
    assert len(challenge) == 16
    assert all(c.isalnum() for c in challenge)


def test_save_challenge_sets_value(redis_mock, challenger):
    challenge = "abc123XYZ"
    time = 300
    challenger.save_challenge(challenge, time=time)
    redis_mock.set.assert_called_once_with("challenge:abc123", challenge, ex=time)


def test_get_challenge_returns_value(redis_mock, challenger):
    redis_mock.get.return_value = b"abc123XYZ"
    result = challenger.get_challenge()
    redis_mock.get.assert_called_once_with("challenge:abc123")
    assert result == b"abc123XYZ"
