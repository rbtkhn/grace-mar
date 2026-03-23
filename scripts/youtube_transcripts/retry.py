from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def sleep_backoff(attempt: int, *, base: float = 1.0, max_wait: float = 60.0) -> None:
    """Exponential backoff with jitter (attempt is 0-based)."""
    exp = min(max_wait, base * (2**attempt))
    jitter = random.uniform(0, exp * 0.2)
    time.sleep(exp + jitter)


def retry_call(
    fn: Callable[[], T],
    *,
    max_attempts: int = 4,
    on_retry: Callable[[int, BaseException], None] | None = None,
) -> T:
    last: BaseException | None = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except BaseException as e:
            last = e
            if attempt + 1 >= max_attempts:
                break
            if on_retry:
                on_retry(attempt, e)
            sleep_backoff(attempt)
    assert last is not None
    raise last
