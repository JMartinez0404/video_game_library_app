from application.game_use_cases import GameService
from domain.entities import PlayState, Platform, VideoGame
from tests.fakes import FakeGameRepository, FakeRawgClient

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

    saved = service.add_video_game(video_game)

    assert saved.id == 1
    assert saved.communal_rating == 9.5
    assert saved.personal_rating == 9
    assert saved.play_state == PlayState.BEATEN
    assert saved.platform == Platform.PS5
    assert saved.image_url == "img.jpg"
    assert saved.title == "Elden Ring"
    assert len(repo.video_games) == 1

def test_get_library():
    repo = FakeGameRepository()
    service = GameService(repo)

    service.add_video_game(VideoGame(None, "Game1", 8.0, 7.5, PlayState.STARTED, Platform.SWITCH, "img", "2020"))

    video_games = service.get_library()

    assert len(video_games) == 1

def test_delete_all_video_games():
    repo = FakeGameRepository()
    service = GameService(repo)
    
    service.delete_all_video_games()

    assert service.get_library() == []

def test_delete_video_game():
    repo = FakeGameRepository()
    service = GameService(repo)

    game_title = "Elden Ring"

    video_game = VideoGame(
        id=None,
        title=game_title,
        communal_rating=9.5,
        personal_rating=9,
        play_state=PlayState.BEATEN,
        platform=Platform.PS5,
        image_url="img.jpg",
        release_date="2022-02-25"
    )

    service.add_video_game(video_game)
    
    deleted = service.delete_video_game(game_title)

    assert deleted.id == 1
    assert deleted.communal_rating == 9.5
    assert deleted.personal_rating == 9
    assert deleted.play_state == PlayState.BEATEN
    assert deleted.platform == Platform.PS5
    assert deleted.image_url == "img.jpg"
    assert deleted.title == "Elden Ring"
    assert len(repo.video_games) == 0

def test_search_external_games_by_name():
    fake_client = FakeRawgClient()
    service = GameService(repository=None, rawg_client=fake_client)

    results = service.search_external_games_by_name("zelda")

    assert len(results) == 1
    assert results[0]["title"] == "Zelda Test"
    assert results[0]["communal_rating"] == 4.5

def test_get_external_game_by_id():
    fake_client = FakeRawgClient()
    service = GameService(repository=None, rawg_client=fake_client)

    result = service.search_external_game_by_id(1)

    assert result.id == 1
    assert result.communal_rating == 4.5

def test_import_external_game():
    fake_repo = FakeGameRepository()
    fake_client = FakeRawgClient()

    service = GameService(repository=fake_repo, rawg_client=fake_client)

    result = service.import_external_game_by_id(1)

    assert result.id == 1
    assert result.title == "Zelda Test"
    assert result.personal_rating == 0.0
