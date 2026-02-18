# tests/test_game_service.py

from application.game_use_cases import GameService
from domain.entities import PlayState, Platform, VideoGame
from tests.fakes import FakeGameRepository


def test_add_video_game():
    repo = FakeGameRepository()
    service = GameService(repo)

    video_game = VideoGame(
        id=None,
        title="Elden Ring",
        communal_rating=9.5,
        personal_rating=9,
        play_state=PlayState.BEATEN,
        platform=Platform.PS5,
        image_url="img.jpg",
        release_date="2022-02-25"
    )

    saved = service.add_game(video_game)

    assert saved.id == 1
    assert saved.title == "Elden Ring"
    assert len(repo.games) == 1


def test_get_library():
    repo = FakeGameRepository()
    service = GameService(repo)

    service.add_game(VideoGame(None, "Game1", 8.0, 7.5, PlayState.STARTED, Platform.SWITCH, "img", "2020"))

    video_games = service.get_library()

    assert len(video_games) == 1
