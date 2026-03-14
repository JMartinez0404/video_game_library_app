from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import VideoGame, Platform, PlayState

class GameRepository(ABC):

    @abstractmethod
    def add(self, video_game: VideoGame) -> VideoGame:
        pass

    @abstractmethod
    def list(
        self,
        platform: Optional[Platform] = None,
        play_state: Optional[PlayState] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> List[VideoGame]:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass

    @abstractmethod
    def delete(self, game_name: str) -> VideoGame:
        pass
