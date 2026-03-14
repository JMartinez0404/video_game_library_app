import pytest
import requests

from application.external_game_service import ExternalGameService
from application.game_use_cases import GameService
from application.errors import ExternalApiError
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

def test_get_library_filters_and_sorts():
    repo = FakeGameRepository()
    service = GameService(repo)

    service.add_video_game(VideoGame(None, "Zelda", 9.0, 8.0, PlayState.STARTED, Platform.SWITCH, "img", "2020"))
    service.add_video_game(VideoGame(None, "Halo", 8.5, 7.0, PlayState.BEATEN, Platform.XBOX, "img", "2019"))
    service.add_video_game(VideoGame(None, "Mario", 9.5, 9.0, PlayState.STARTED, Platform.SWITCH, "img", "2018"))

    filtered = service.get_library(platform=Platform.SWITCH)
    assert len(filtered) == 2

    sorted_games = service.get_library(sort_by="title", sort_order="asc")
    assert [game.title for game in sorted_games] == ["Halo", "Mario", "Zelda"]

def test_get_library_rejects_invalid_sort():
    repo = FakeGameRepository()
    service = GameService(repo)

    with pytest.raises(ValueError):
        service.get_library(sort_by="invalid_field")

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
    service = ExternalGameService(repository=None, rawg_client=fake_client)

    results = service.search_by_name("zelda")

    assert results.count == 1
    assert len(results.results) == 1
    assert results.results[0].title == "Zelda Test"
    assert results.results[0].communal_rating == 4.5
    assert results.results[0].rawg_slug == "zelda-test"

def test_search_external_games_pagination_metadata():
    fake_client = FakeRawgClient()
    service = ExternalGameService(repository=None, rawg_client=fake_client)

    results = service.search_by_name("zelda", page=2, page_size=5)

    assert results.count == 1
    assert results.next is None
    assert results.previous is None

def test_search_external_games_handles_rawg_error():
    class ErrorRawgClient:
        def search_games_by_name(
            self,
            game_name: str,
            page: int = 1,
            page_size: int = 10,
        ):
            raise requests.RequestException("RAWG error")

    service = ExternalGameService(repository=None, rawg_client=ErrorRawgClient())

    with pytest.raises(ExternalApiError) as excinfo:
        service.search_by_name("zelda")

    assert "RAWG search failed" in str(excinfo.value)

def test_get_external_game_by_id():
    fake_client = FakeRawgClient()
    service = ExternalGameService(repository=None, rawg_client=fake_client)

    result = service.get_by_id(1)

    assert result.id == 1
    assert result.communal_rating == 4.5
    assert result.rawg_slug == "zelda-test"

def test_import_external_game_by_id():
    fake_repo = FakeGameRepository()
    fake_client = FakeRawgClient()

    service = ExternalGameService(repository=fake_repo, rawg_client=fake_client)

    result = service.import_game_by_id(1)

    assert result.id == 1
    assert result.title == "Zelda Test"
    assert result.personal_rating == 0.0
    assert result.platform == Platform.PS1
    assert result.rawg_slug == "zelda-test"

def test_import_external_game_maps_platform():
    class SwitchRawgClient:
        def get_game_by_id(self, game_id: str):
            return {
                "id": 2,
                "name": "Switch Test",
                "released": "2021-01-01",
                "platforms": [{"platform": {"name": "Nintendo Switch"}}],
                "rating": 4.2,
                "background_image": "http://image.url"
            }

    fake_repo = FakeGameRepository()
    service = ExternalGameService(repository=fake_repo, rawg_client=SwitchRawgClient())

    result = service.import_game_by_id(2)

    assert result.platform == Platform.SWITCH

def test_backfill_rawg_slugs():
    class BackfillRawgClient:
        def search_games_by_name(
            self,
            game_name: str,
            page: int = 1,
            page_size: int = 10,
        ):
            return {
                "results": [
                    {
                        "id": 10,
                        "name": game_name,
                        "slug": "matched-slug",
                        "released": "2003-11-14",
                    }
                ]
            }

    repo = FakeGameRepository()
    repo.add(
        VideoGame(
            id=None,
            title="Pokemon Colosseum",
            communal_rating=8.0,
            personal_rating=7.5,
            play_state=PlayState.NOT_STARTED,
            platform=Platform.PS2,
            image_url="img",
            release_date="2003-11-14",
        )
    )
    repo.add(
        VideoGame(
            id=None,
            title="Zelda Test",
            communal_rating=9.0,
            personal_rating=9.0,
            play_state=PlayState.BEATEN,
            platform=Platform.SWITCH,
            image_url="img",
            release_date="2020-01-01",
            rawg_slug="zelda-test",
        )
    )

    service = ExternalGameService(repository=repo, rawg_client=BackfillRawgClient())
    result = service.backfill_rawg_slugs()

    assert result["updated"] == 1
    assert result["skipped"] == 1
    assert repo.video_games[0].rawg_slug == "matched-slug"
