import requests
from typing import Dict, Any


class RawgClient:
    BASE_URL = "https://api.rawg.io/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
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
        response = requests.get(
            f"{self.BASE_URL}/games/{game_id}",
            params={"key": self.api_key},
            timeout=10,
        )

        response.raise_for_status()
        return response.json()
