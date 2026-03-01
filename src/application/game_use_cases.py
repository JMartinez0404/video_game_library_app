from typing import List
from domain.entities import VideoGame
from domain.repositories import GameRepository


class GameService:
    
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def add_video_game(self, video_game: VideoGame) -> VideoGame:
        return self.repository.add(video_game)

    def get_library(self) -> List[VideoGame]:
        return self.repository.list()
    
    def delete_all_video_games(self) -> None:
        return self.repository.delete_all()
    
    def delete_video_game(self, game_name: str) -> VideoGame:
        return self.repository.delete(game_name)
