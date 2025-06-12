import pytest
import fakeredis
from freezegun import freeze_time
from datetime import timedelta
from src.services.verifier import Verifier


class TestVerifier:

    @pytest.fixture
    def fake_redis(self):
        redis_client = fakeredis.FakeRedis()
        redis_client.flushdb()
        return redis_client

    @pytest.fixture
    def verifier_instance(self, mocker, fake_redis):
        mocker.patch("src.services.verifier.get_redis", return_value=fake_redis)
        return Verifier(event_key="123_sesion_cookie")

    @pytest.mark.parametrize(
        "challenge, solution, difficulty, expected_verification",
        [
            ["GrjHugQwnssyI57c", "114437", 4, True],
            ["GrjHugQwnssyI57c", "014437", 4, False],
        ],
    )
    def test_verify_pow(
        self,
        challenge,
        solution,
        difficulty,
        expected_verification,
        verifier_instance: Verifier,
    ):
        verification = verifier_instance.verify_pow(challenge, solution, difficulty)
        assert expected_verification == verification

    def test_mark_and_get_verification(self, verifier_instance: Verifier):
        """
        Checks that False is returned before an event is marked as verified
        Then checks that True is returned only once the event is marked as verified
        """
        assert verifier_instance.is_verified() == False
        verifier_instance.mark_verified()
        assert verifier_instance.is_verified()

    def test_cookie_expires(self, verifier_instance: Verifier):
        """
        Checks that as a cookie expires the user will no longer be verified
        """
        with freeze_time("1991-12-26 00:00:00") as freezer:
            verifier_instance.mark_verified(time=300)
            assert verifier_instance.is_verified()

            freezer.tick(delta=timedelta(seconds=299))
            assert verifier_instance.is_verified()

            freezer.tick(delta=timedelta(seconds=5))
            assert verifier_instance.is_verified() == False
