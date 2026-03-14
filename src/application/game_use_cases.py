from typing import List, Optional
from domain.entities import VideoGame, Platform, PlayState
from domain.repositories import GameRepository


class GameService:
    
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def add_video_game(self, video_game: VideoGame) -> VideoGame:
        return self.repository.add(video_game)

    def get_library(
        self,
        platform: Optional[Platform] = None,
        play_state: Optional[PlayState] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> List[VideoGame]:
        if sort_by is not None and sort_by not in {
            "title",
            "communal_rating",
            "personal_rating",
            "release_date",
        }:
            raise ValueError("Invalid sort_by value")
        if sort_order not in {"asc", "desc"}:
            raise ValueError("Invalid sort_order value")

        return self.repository.list(
            platform=platform,
            play_state=play_state,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    
    def delete_all_video_games(self) -> None:
        return self.repository.delete_all()
    
    def delete_video_game(self, game_name: str) -> VideoGame:
        return self.repository.delete(game_name)
