import requests
from typing import Dict, Any

from infrastructure.external_apis.rate_limiter import RateLimiter


class RawgClient:
    BASE_URL = "https://api.rawg.io/api"

    def __init__(self, api_key: str, rate_limiter: RateLimiter | None = None):
        self.api_key = api_key
        self.rate_limiter = rate_limiter or RateLimiter(min_interval_seconds=1.0)

    def search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        self.rate_limiter.wait()
        response = requests.get(
            f"{self.BASE_URL}/games",
            params={
                "key": self.api_key,
                "search": game_name,
                "page": page,
                "page_size": page_size,
            },
            timeout=10,
        )

        response.raise_for_status()
        return response.json()
    
    def get_game_by_id(self, game_id: str) -> Dict[str, Any]:
        self.rate_limiter.wait()
        response = requests.get(
            f"{self.BASE_URL}/games/{game_id}",
            params={"key": self.api_key},
            timeout=10,
        )

        response.raise_for_status()
        return response.json()
