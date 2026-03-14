from fastapi.testclient import TestClient
from main import app
from application.errors import ExternalApiError
from domain.entities import PlayState, Platform, VideoGame


client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer dev-key"}


def test_external_search_route(monkeypatch):
    captured = {}

    def fake_search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ):
        captured["game_name"] = game_name
        captured["page"] = page
        captured["page_size"] = page_size
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Mock Zelda",
                    "slug": "mock-zelda",
                    "platforms": "PS1",
                    "released": "2021-01-01",
                    "rating": 5.0,
                    "background_image": "http://mock.url"
                }
            ]
        }

    monkeypatch.setattr(
        "infrastructure.external_apis.rawg_client.RawgClient.search_games_by_name",
        fake_search_games_by_name
    )

    response = client.get("/external/video_games/search?game_name=zelda")

    assert response.status_code == 200
    assert response.json()["results"][0]["title"] == "Mock Zelda"
    assert response.json()["count"] == 1
    assert response.json()["results"][0]["rawg_platforms"] == ["PS1"]
    assert captured["page"] == 1
    assert captured["page_size"] == 10

def test_external_search_route_pagination_params(monkeypatch):
    captured = {}

    def fake_search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ):
        captured["page"] = page
        captured["page_size"] = page_size
        return {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        }

    monkeypatch.setattr(
        "infrastructure.external_apis.rawg_client.RawgClient.search_games_by_name",
        fake_search_games_by_name
    )

    response = client.get("/external/video_games/search?game_name=zelda&page=2&page_size=5")

    assert response.status_code == 200
    assert captured["page"] == 2
    assert captured["page_size"] == 5

def test_external_search_route_handles_rawg_error(monkeypatch):
    def fake_search_games_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ):
        raise ExternalApiError("RAWG search failed")

    monkeypatch.setattr(
        "application.external_game_service.ExternalGameService.search_by_name",
        fake_search_games_by_name
    )

    response = client.get("/external/video_games/search?game_name=zelda")

    assert response.status_code == 502
    assert response.json()["detail"] == "RAWG search failed"

def test_external_get_by_id_route(monkeypatch):

    def fake_get_by_id(self, game_id: str):
        return {
            "id": 1,
            "name": "Zelda Test",
            "released": "2020-01-01",
            "rating": 4.5,
            "background_image": "http://image.url"
        }

    monkeypatch.setattr(
        "infrastructure.external_apis.rawg_client.RawgClient.get_game_by_id",
        fake_get_by_id
    )

    response = client.get("/external/video_games/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["rawg_slug"] is None
    assert response.json()["rawg_platforms"] == []

def test_external_import_route(monkeypatch):
    def fake_import_game_by_id(self, game_id: int):
        return VideoGame(
            id=1,
            title="Imported Game",
            communal_rating=4.0,
            personal_rating=0.0,
            play_state=PlayState.NOT_STARTED,
            platform=Platform.PS1,
            image_url="http://image.url",
            release_date="2022-01-01",
        )

    monkeypatch.setattr(
        "application.external_game_service.ExternalGameService.import_game_by_id",
        fake_import_game_by_id
    )

    response = client.post("/external/video_games/1/import", headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["title"] == "Imported Game"

def test_external_backfill_route(monkeypatch):
    def fake_backfill(self):
        return {"updated": 2, "skipped": 1, "failed": 0, "total": 3}

    monkeypatch.setattr(
        "application.external_game_service.ExternalGameService.backfill_rawg_slugs",
        fake_backfill
    )

    response = client.post("/external/video_games/backfill_slugs", headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["updated"] == 2

def test_update_game_route(monkeypatch):
    def fake_update(self, game_id: int, personal_rating=None, platform=None):
        return VideoGame(
            id=game_id,
            title="Updated Game",
            communal_rating=7.5,
            personal_rating=personal_rating,
            play_state=PlayState.NOT_STARTED,
            platform=platform,
            image_url="http://image.url",
            release_date="2022-01-01",
        )

    monkeypatch.setattr(
        "application.game_use_cases.GameService.update_video_game",
        fake_update,
    )

    response = client.patch(
        "/video_games/1",
        headers=AUTH_HEADERS,
        json={"personal_rating": 8.5, "platform": "PS5"},
    )

    assert response.status_code == 200
    assert response.json()["personal_rating"] == 8.5
    assert response.json()["platform"] == "PS5"
