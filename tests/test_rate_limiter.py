from infrastructure.external_apis.rate_limiter import RateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        return self.now

    def sleep(self, duration: float) -> None:
        self.sleeps.append(duration)
        self.now += duration


def test_rate_limiter_sleeps_when_called_too_fast() -> None:
    clock = FakeClock()
    limiter = RateLimiter(1.0, time_fn=clock.time, sleep_fn=clock.sleep)

    limiter.wait()
    limiter.wait()

    assert clock.sleeps == [1.0]
    assert clock.now == 1.0


def test_rate_limiter_skips_sleep_when_enough_time_passed() -> None:
    clock = FakeClock()
    limiter = RateLimiter(1.0, time_fn=clock.time, sleep_fn=clock.sleep)

    limiter.wait()
    clock.now = 2.0
    limiter.wait()

    assert clock.sleeps == []
