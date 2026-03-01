from typing import List
from domain.entities import VideoGame, PlayState, Platform
from domain.repositories import GameRepository
from infrastructure.external_apis.rawg_client import RawgClient
from infrastructure.external_apis.dtos import ExternalGameDTO


class ExternalGameService:

    def __init__(
        self,
        repository: GameRepository,
        rawg_client: RawgClient
    ):
        self.repository = repository
        self.rawg_client = rawg_client

    # -------- SEARCH BY NAME --------
    def search_by_name(self, game_name: str) -> List[ExternalGameDTO]:
        data = self.rawg_client.search_games_by_name(game_name)
        results = data.get("results", [])

        return [
            ExternalGameDTO(
                id=g["id"],
                title=g["name"],
                communal_rating=g.get("rating"),
                image_url=g.get("background_image"),
                release_date=g.get("released"),
            )
            for g in results
        ]

    # -------- GET BY ID --------
    def get_by_id(self, game_id: int) -> ExternalGameDTO:
        data = self.rawg_client.get_game_by_id(game_id)

        return ExternalGameDTO(
            id=data["id"],
            title=data["name"],
            communal_rating=data.get("rating"),
            image_url=data.get("background_image"),
            release_date=data.get("released"),
        )

    # -------- IMPORT INTO LIBRARY --------
    def import_game_by_id(self, game_id: int) -> VideoGame:
        data = self.rawg_client.get_game_by_id(game_id)

        video_game = VideoGame(
            id=None,
            title=data["name"],
            communal_rating=data.get("rating", 0.0),
            personal_rating=0.0,
            play_state=PlayState.NOT_STARTED,
            platform=Platform.PS1,  # TODO: improve mapping
            image_url=data.get("background_image", ""),
            release_date=data.get("released", ""),
        )

        return self.repository.add(video_game)
