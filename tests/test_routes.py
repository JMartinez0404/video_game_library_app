from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_external_search_route(monkeypatch):

    def fake_search_games_by_name(self, game_name: str):
        return {
            "results": [
                {
                    "id": 1,
                    "name": "Mock Zelda",
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

    response = client.get("/external/video_games?game_name=zelda")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Mock Zelda"

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
