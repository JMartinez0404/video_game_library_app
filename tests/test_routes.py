from fastapi.testclient import TestClient
from main import app
from application.errors import ExternalApiError
from domain.entities import PlayState, Platform, VideoGame


client = TestClient(app)


def test_external_search_route(monkeypatch):

    def fake_search_games_by_name(
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

    response = client.post("/external/video_games/1/import")

    assert response.status_code == 200
    assert response.json()["title"] == "Imported Game"
