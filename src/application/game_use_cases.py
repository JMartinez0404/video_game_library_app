from typing import List
from domain.entities import PlayState, Platform, VideoGame
from domain.repositories import GameRepository
from infrastructure.external_apis.dtos import ExternalGameDTO
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
    
    def search_external_games_by_name(self, game_name: str) -> None:
        if not self.rawg_client:
            raise ValueError("RAWG client not configured")

        data = self.rawg_client.search_games_by_name(game_name)

        data_results = data.get("results", [])

        if data_results:
            return [
                {
                    "id": g["id"],
                    "title": g["name"],
                    "communal_rating": g["rating"],
                    "platform": g["platforms"],
                    "image_url": g["background_image"],
                    "release_date": g["released"]
                }
                for g in data_results
            ]
        else:
            return {"message": f"No games found with the name: {game_name}"}

    def search_external_game_by_id(self, game_id: int) -> ExternalGameDTO:
        if not self.rawg_client:
            raise ValueError("RAWG client not configured")

        data = self.rawg_client.get_game_by_id(game_id)

        return ExternalGameDTO(
            id=data["id"],
            title=data["name"],
            communal_rating=data["rating"],
            image_url=data["background_image"],
            release_date=data["released"],
        )

    def import_external_game_by_id(self, game_id: int) -> VideoGame:
        if not self.rawg_client:
            raise ValueError("RAWG client not configured")

        data = self.rawg_client.get_game_by_id(game_id)

        video_game = VideoGame(
            id=None,
            title=data["name"],
            communal_rating=data.get("rating", 0.0),
            personal_rating=0.0,
            play_state=PlayState.NOT_STARTED,
            platform=Platform.PS1,
            image_url=data.get("background_image", ""),
            release_date=data.get("released", ""),
        )

        return self.repository.add(video_game)
