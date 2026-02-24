from domain.repositories import GameRepository
from domain.entities import VideoGame

class FakeGameRepository(GameRepository):
    def __init__(self):
        self.video_games = []
        self._id = 1

    def add(self, video_game: VideoGame) -> VideoGame:
        video_game.id = self._id
        self._id += 1
        self.video_games.append(video_game)
        return video_game

    def list(self):
        return self.video_games
    
    def delete_all(self) -> None:
        self.video_games.clear()
    
    def delete(self, game_name: str) -> VideoGame:
        for index, video_game in enumerate(self.video_games):
            if game_name == video_game.title:
                return self.video_games.pop(index)

class FakeRawgClient:
    def search_games(self, query: str):
        return {
            "results": [
                {
                    "name": "Zelda Test",
                    "released": "2020-01-01",
                    "rating": 4.5,
                    "background_image": "http://image.url"
                }
            ]
        }
