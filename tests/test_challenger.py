import pytest
import fakeredis
from src.services.challenger import Challenger


class TestChallenger:

    @pytest.fixture
    def fake_redis(self):
        redis_client = fakeredis.FakeRedis()
        redis_client.flushdb()
        return redis_client

    @pytest.fixture
    def challenger_instance(self, mocker, fake_redis):
        mocker.patch("src.services.challenger.get_redis", return_value=fake_redis)
        return Challenger(challenge_id="123_challenge_id")

    def test_generate_challenge(self):
        """
        Checks challenge:
        - is alphanumeric
        - is a str
        - length is 16
        """
        challenge = Challenger.generate_challenge()
        assert len(challenge) == 16
        assert isinstance(challenge, str)
        assert all(c.isalnum() for c in challenge)

    def test_save_and_get_challenge(self, challenger_instance: Challenger):
        """
        Sets and retrieves challenge in Redis.
        Checks that what is sent is the same as what is retrieved.
        """
        challenge_str = "abc1234"
        challenger_instance.save_challenge(challenge_str)
        retrieved_challenge = challenger_instance.get_challenge()
        assert retrieved_challenge == challenge_str
