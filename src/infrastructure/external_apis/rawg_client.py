import requests
from typing import Dict, Any


class RawgClient:
    BASE_URL = "https://api.rawg.io/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_games(self, query: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.BASE_URL}/games",
            params={
                "key": self.api_key,
                "search": query,
            },
            timeout=10,
        )

        response.raise_for_status()
        return response.json()
