from __future__ import annotations

import threading
import time
from typing import Callable


class RateLimiter:
    def __init__(
        self,
        min_interval_seconds: float,
        time_fn: Callable[[], float] = time.monotonic,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self._min_interval_seconds = min_interval_seconds
        self._time_fn = time_fn
        self._sleep_fn = sleep_fn
        self._lock = threading.Lock()
        self._last_request_at: float | None = None

    def wait(self) -> None:
        with self._lock:
            now = self._time_fn()
            if self._last_request_at is None:
                self._last_request_at = now
                return

            elapsed = now - self._last_request_at
            remaining = self._min_interval_seconds - elapsed
            if remaining > 0:
                self._sleep_fn(remaining)
                now = self._time_fn()

            self._last_request_at = now
