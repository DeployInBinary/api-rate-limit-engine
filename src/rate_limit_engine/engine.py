import time
from .config import WINDOW_SECONDS, DEFAULT_LIMIT, PREMIUM_CLIENTS
from .storage import JSONStorage


class RateLimitEngine:
    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self.data = self.storage.load()

    def _get_limit(self, client_id: str) -> int:
        return PREMIUM_CLIENTS.get(client_id, DEFAULT_LIMIT)

    def _clean_window(self, client_id: str, current_time: float):
        if client_id not in self.data:
            return []

        valid = [
            t for t in self.data[client_id]
            if t > (current_time - WINDOW_SECONDS)
        ]

        self.data[client_id] = valid
        return valid

    def handle_request(self, client_id: str):
        current_time = time.time()
        limit = self._get_limit(client_id)

        history = self._clean_window(client_id, current_time)
        usage = len(history)

        if usage < limit:
            history.append(current_time)
            self.data[client_id] = history
            self.storage.save(self.data)
            return 200, f"OK ({usage + 1}/{limit})"

        return 429, f"Rate limit exceeded ({usage}/{limit})"

    def get_status(self, client_id: str):
        current_time = time.time()
        limit = self._get_limit(client_id)

        history = self._clean_window(client_id, current_time)
        self.storage.save(self.data)

        usage = len(history)
        is_limited = usage >= limit

        time_left = 0.0
        if is_limited:
            expiry = history[0] + WINDOW_SECONDS
            time_left = max(0.0, expiry - current_time)

        return {
            "limit": limit,
            "usage": usage,
            "is_limited": is_limited,
            "time_left": round(time_left, 2),
        }
