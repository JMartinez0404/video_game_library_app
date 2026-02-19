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
