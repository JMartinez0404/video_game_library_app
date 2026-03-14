from typing import Optional

from domain.repositories import GameRepository
from domain.entities import VideoGame, Platform, PlayState

class FakeGameRepository(GameRepository):
    def __init__(self):
        self.video_games = []
        self._id = 1

    def add(self, video_game: VideoGame) -> VideoGame:
        video_game.id = self._id
        self._id += 1
        self.video_games.append(video_game)
        return video_game

    def list(
        self,
        platform: Optional[Platform] = None,
        play_state: Optional[PlayState] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ):
        games = list(self.video_games)
        if platform is not None:
            games = [game for game in games if game.platform == platform]
        if play_state is not None:
            games = [game for game in games if game.play_state == play_state]
        if sort_by is not None:
            games.sort(
                key=lambda game: getattr(game, sort_by),
                reverse=sort_order == "desc",
            )
        return games
    
    def delete_all(self) -> None:
        self.video_games.clear()
    
    def delete(self, game_name: str) -> VideoGame:
        for index, video_game in enumerate(self.video_games):
            if game_name == video_game.title:
                return self.video_games.pop(index)

class FakeRawgClient:
    def search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ):
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": "1",
                    "name": "Zelda Test",
                    "slug": "zelda-test",
                    "released": "2020-01-01",
                    "platforms": "PS1",
                    "rating": 4.5,
                    "background_image": "http://image.url"
                }
            ]
        }
    
    def get_game_by_id(self, game_id: str):
        return {
            "id": 1,
            "name": "Zelda Test",
            "slug": "zelda-test",
            "released": "2020-01-01",
            "platforms": "PS1",
            "rating": 4.5,
            "background_image": "http://image.url"
        }
