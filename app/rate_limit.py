"""In-memory rate limits for the public endpoint, which spends money on every call.

Per IP: a sliding one-minute window. Global: a daily cap, as a backstop if many IPs are used.
State lives in the process, so it resets on restart; enough for a single-instance demo.
The alternative, AWS WAF rate rules, is sturdier but adds cost and another moving part.
"""

import time
from collections import defaultdict, deque
from threading import Lock


class RateLimiter:
    def __init__(self, per_minute: int, per_day: int):
        self.per_minute = per_minute
        self.per_day = per_day
        self._recent: dict[str, deque[float]] = defaultdict(deque)
        self._day = -1
        self._today = 0
        self._lock = Lock()  # sync endpoints run in a thread pool

    def allow(self, key: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        with self._lock:
            day = int(now // 86_400)
            if day != self._day:
                self._day, self._today = day, 0
            if self._today >= self.per_day:
                return False

            recent = self._recent[key]
            while recent and recent[0] <= now - 60:
                recent.popleft()
            if len(recent) >= self.per_minute:
                return False

            recent.append(now)
            self._today += 1
            return True
