from domain.entities import VideoGame
from domain.repositories import GameRepository
from typing import List

class GameService:

    def __init__(self, repository: GameRepository):
        self.repository = repository

    def add_video_game(self, video_game: VideoGame) -> VideoGame:
        return self.repository.add(video_game)

    def get_library(self) -> List[VideoGame]:
        return self.repository.list()
