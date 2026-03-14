from typing import List
import requests
from domain.entities import VideoGame, PlayState, Platform
from domain.repositories import GameRepository
from infrastructure.external_apis.rawg_client import RawgClient
from application.dtos import ExternalGameDTO, ExternalGameSearchResult
from application.errors import ExternalApiError


class ExternalGameService:

    def __init__(
        self,
        repository: GameRepository,
        rawg_client: RawgClient
    ):
        self.repository = repository
        self.rawg_client = rawg_client

    # -------- SEARCH BY NAME --------
    def search_by_name(
        self,
        game_name: str,
        page: int = 1,
        page_size: int = 10,
    ) -> ExternalGameSearchResult:
        try:
            data = self.rawg_client.search_games_by_name(
                game_name,
                page=page,
                page_size=page_size,
            )
        except requests.RequestException as exc:
            raise ExternalApiError(
                "RAWG search failed",
                status_code=getattr(getattr(exc, "response", None), "status_code", None),
            ) from exc
        results = data.get("results", [])

        return ExternalGameSearchResult(
            count=data.get("count", 0),
            next=data.get("next"),
            previous=data.get("previous"),
            results=[
                ExternalGameDTO(
                    id=g["id"],
                    title=g["name"],
                    communal_rating=g.get("rating"),
                    image_url=g.get("background_image"),
                    release_date=g.get("released"),
                    rawg_slug=g.get("slug"),
                )
                for g in results
            ],
        )

    # -------- GET BY ID --------
    def get_by_id(self, game_id: int) -> ExternalGameDTO:
        try:
            data = self.rawg_client.get_game_by_id(game_id)
        except requests.RequestException as exc:
            raise ExternalApiError(
                "RAWG lookup failed",
                status_code=getattr(getattr(exc, "response", None), "status_code", None),
            ) from exc

        return ExternalGameDTO(
            id=data["id"],
            title=data["name"],
            communal_rating=data.get("rating"),
            image_url=data.get("background_image"),
            release_date=data.get("released"),
            rawg_slug=data.get("slug"),
        )
    
    # -------- IMPORT INTO LIBRARY --------
    def import_game_by_id(self, game_id: int):
        try:
            data = self.rawg_client.get_game_by_id(game_id)
        except requests.RequestException as exc:
            raise ExternalApiError(
                "RAWG import failed",
                status_code=getattr(getattr(exc, "response", None), "status_code", None),
            ) from exc
        platform = self._map_platform(data.get("platforms"))

        game = VideoGame(
            id=None,
            title=data["name"],
            communal_rating=data["rating"],
            personal_rating=0,
            play_state=PlayState.NOT_STARTED,
            platform=platform,
            image_url=data["background_image"],
            release_date=data["released"]
        )

        return self.repository.add(game)

    def _map_platform(self, rawg_platforms) -> Platform:
        names = self._extract_platform_names(rawg_platforms)

        for name in names:
            if "switch 2" in name or "nintendo switch 2" in name or "switch2" in name:
                return Platform.SWITCH2

        for name in names:
            if "switch" in name:
                return Platform.SWITCH

        for name in names:
            if "playstation 5" in name or "ps5" in name or "playstation5" in name:
                return Platform.PS5

        for name in names:
            if "playstation 4" in name or "ps4" in name or "playstation4" in name:
                return Platform.PS4

        for name in names:
            if "playstation 3" in name or "ps3" in name or "playstation3" in name:
                return Platform.PS3

        for name in names:
            if "playstation 2" in name or "ps2" in name or "playstation2" in name:
                return Platform.PS2

        for name in names:
            if "playstation portable" in name or "psp" in name:
                return Platform.PSP

        for name in names:
            if "3ds" in name or "nintendo 3ds" in name:
                return Platform.THREE_DS

        for name in names:
            if "nintendo ds" in name or (name == "ds" and "3ds" not in name):
                return Platform.DS

        for name in names:
            if "wii" in name:
                return Platform.WII

        for name in names:
            if "xbox" in name:
                return Platform.XBOX

        for name in names:
            if "playstation" in name or "ps1" in name or "playstation1" in name:
                return Platform.PS1

        return Platform.PS1

    def _extract_platform_names(self, rawg_platforms) -> List[str]:
        names: List[str] = []

        if isinstance(rawg_platforms, list):
            for item in rawg_platforms:
                candidate = None
                if isinstance(item, dict):
                    platform = item.get("platform")
                    if isinstance(platform, dict):
                        candidate = platform.get("name") or platform.get("slug")
                    else:
                        candidate = item.get("name") or item.get("slug")
                if candidate:
                    names.append(str(candidate).lower())
        elif isinstance(rawg_platforms, dict):
            candidate = rawg_platforms.get("name") or rawg_platforms.get("slug")
            if candidate:
                names.append(str(candidate).lower())
        elif isinstance(rawg_platforms, str):
            names.append(rawg_platforms.lower())

        return names
