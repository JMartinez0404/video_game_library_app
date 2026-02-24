from typing import List
from domain.entities import VideoGame
from domain.repositories import GameRepository
from infrastructure.external_apis.rawg_client import RawgClient


class GameService:
    
    def __init__(self, repository: GameRepository, rawg_client: RawgClient | None = None):
        self.repository = repository
        self.rawg_client = rawg_client

    def add_video_game(self, video_game: VideoGame) -> VideoGame:
        return self.repository.add(video_game)

    def get_library(self) -> List[VideoGame]:
        return self.repository.list()
    
    def delete_all_video_games(self) -> None:
        return self.repository.delete_all()
    
    def delete_video_game(self, game_name: str) -> VideoGame:
        return self.repository.delete(game_name)
    
    def search_external_games(self, query: str):
        if not self.rawg_client:
            raise ValueError("RAWG client not configured")

        data = self.rawg_client.search_games(query)

        return [
            {
                "title": game["name"],
                "release_date": game.get("released"),
                "communal_rating": game.get("rating"),
                "image_url": game.get("background_image"),
            }
            for game in data.get("results", [])
        ]
