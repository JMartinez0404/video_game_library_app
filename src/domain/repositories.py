from abc import ABC, abstractmethod
from typing import List
from .entities import VideoGame

class GameRepository(ABC):

    @abstractmethod
    def add(self, video_game: VideoGame) -> VideoGame:
        pass

    @abstractmethod
    def remove(self, video_game: VideoGame) -> VideoGame:
        # Could make this so that only one attribute is needed to remove a game
        # Might want to add a filter method that returns game that match that attribute
        # and then you can choose to remove one
        pass

    @abstractmethod
    def list(self) -> List[VideoGame]:
        pass
