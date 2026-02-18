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
