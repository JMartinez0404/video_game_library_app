from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import VideoGame, Platform, PlayState, ActivityEntry

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

    @abstractmethod
    def update_rawg_metadata(
        self,
        game_id: int,
        rawg_slug: str | None,
        rawg_platforms: list[str],
    ) -> VideoGame:
        pass

    @abstractmethod
    def update(
        self,
        game_id: int,
        personal_rating: float | None = None,
        platform: Platform | None = None,
        notes: str | None = None,
        tags: list[str] | None = None,
        progress: float | None = None,
        favorite: bool | None = None,
    ) -> VideoGame:
        pass


class ActivityRepository(ABC):

    @abstractmethod
    def add(self, entry: ActivityEntry) -> ActivityEntry:
        pass

    @abstractmethod
    def list(self, limit: int = 10) -> list[ActivityEntry]:
        pass

    @abstractmethod
    def list_imports(self, limit: int = 10) -> list[ActivityEntry]:
        pass
