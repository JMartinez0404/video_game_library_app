from abc import ABC, abstractmethod
from typing import List
from .entities import VideoGame

class GameRepository(ABC):

    @abstractmethod
    def add(self, video_game: VideoGame) -> VideoGame:
        pass

    @abstractmethod
    def list(self) -> List[VideoGame]:
        pass

    @abstractmethod
    def delete_all(self, video_game: VideoGame) -> None:
        pass

    @abstractmethod
    def delete(self, game_name: str) -> VideoGame:
        pass
