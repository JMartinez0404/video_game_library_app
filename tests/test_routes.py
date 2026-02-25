from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_external_search_route(monkeypatch):

    def fake_search(self, query: str):
        return {
            "results": [
                {
                    "name": "Mock Zelda",
                    "released": "2021-01-01",
                    "rating": 5.0,
                    "background_image": "http://mock.url"
                }
            ]
        }

    monkeypatch.setattr(
        "infrastructure.external_apis.rawg_client.RawgClient.search_games",
        fake_search
    )

    response = client.get("/external/video_games?query=zelda")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Mock Zelda"
