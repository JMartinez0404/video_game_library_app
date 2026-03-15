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
                    rawg_platforms=self._extract_platform_display_names(
                        g.get("platforms")
                    ),
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
            rawg_platforms=self._extract_platform_display_names(
                data.get("platforms")
            ),
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
        rawg_platforms = self._extract_platform_display_names(
            data.get("platforms")
        )

        game = VideoGame(
            id=None,
            title=data["name"],
            communal_rating=data["rating"],
            personal_rating=0,
            play_state=PlayState.NOT_STARTED,
            platform=platform,
            image_url=data["background_image"],
            release_date=data["released"],
            rawg_slug=data.get("slug"),
            rawg_platforms=rawg_platforms,
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
            if "playstation vita" in name or "ps vita" in name or "vita" in name:
                return Platform.PS_VITA

        for name in names:
            if "3ds" in name or "nintendo 3ds" in name:
                return Platform.THREE_DS

        for name in names:
            if "nintendo ds" in name or (name == "ds" and "3ds" not in name):
                return Platform.DS

        for name in names:
            if "wii u" in name:
                return Platform.WII_U

        for name in names:
            if "wii" in name:
                return Platform.WII

        for name in names:
            if "gamecube" in name:
                return Platform.GAMECUBE

        for name in names:
            if "nintendo 64" in name or "n64" in name:
                return Platform.N64

        for name in names:
            if "super nintendo" in name or "snes" in name:
                return Platform.SNES

        for name in names:
            if "nintendo entertainment system" in name or "nes" in name:
                return Platform.NES

        for name in names:
            if "game boy advance" in name or "gba" in name:
                return Platform.GAMEBOY_ADVANCE

        for name in names:
            if "game boy color" in name or "gbc" in name:
                return Platform.GAMEBOY_COLOR

        for name in names:
            if "game boy" in name or name == "gb":
                return Platform.GAMEBOY

        for name in names:
            if "xbox series" in name or "series x" in name or "series s" in name:
                return Platform.XBOX_SERIES

        for name in names:
            if "xbox one" in name:
                return Platform.XBOX_ONE

        for name in names:
            if "xbox 360" in name:
                return Platform.XBOX_360

        for name in names:
            if "xbox" in name:
                return Platform.XBOX

        for name in names:
            if "macos" in name or "mac os" in name or name == "mac":
                return Platform.MAC

        for name in names:
            if "linux" in name:
                return Platform.LINUX

        for name in names:
            if "pc" in name or "windows" in name:
                return Platform.PC

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

    def _extract_platform_display_names(self, rawg_platforms) -> List[str]:
        display_names: List[str] = []

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
                    display_names.append(str(candidate))
        elif isinstance(rawg_platforms, dict):
            candidate = rawg_platforms.get("name") or rawg_platforms.get("slug")
            if candidate:
                display_names.append(str(candidate))
        elif isinstance(rawg_platforms, str):
            display_names.append(rawg_platforms)

        return list(dict.fromkeys(display_names))

    def _normalize_title(self, title: str) -> str:
        return (
            title.lower()
            .replace("’", "'")
            .replace("'", "")
            .replace("-", " ")
            .replace(":", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace("!", " ")
            .replace("?", " ")
            .replace("(", " ")
            .replace(")", " ")
            .replace("[", " ")
            .replace("]", " ")
            .replace("{", " ")
            .replace("}", " ")
            .replace("_", " ")
            .replace("/", " ")
            .replace("\\", " ")
            .replace("+", " ")
            .replace("&", " ")
            .replace("  ", " ")
            .strip()
            .replace(" ", "")
        )

    def backfill_rawg_slugs(self) -> dict:
        games = self.repository.list()
        updated = 0
        skipped = 0
        failed = 0

        for game in games:
            needs_slug = not game.rawg_slug
            needs_platforms = not game.rawg_platforms
            if not needs_slug and not needs_platforms:
                skipped += 1
                continue

            try:
                data = self.rawg_client.search_games_by_name(
                    game.title,
                    page=1,
                    page_size=20,
                )
            except requests.RequestException:
                failed += 1
                continue

            results = data.get("results", [])
            release_date = game.release_date[:10] if game.release_date else None
            match = None

            if release_date:
                match = next(
                    (
                        result
                        for result in results
                        if result.get("released", "")[:10] == release_date
                    ),
                    None,
                )

            if match is None:
                normalized_title = self._normalize_title(game.title)
                match = next(
                    (
                        result
                        for result in results
                        if self._normalize_title(result.get("name", ""))
                        == normalized_title
                    ),
                    None,
                )

            if match:
                rawg_platforms = self._extract_platform_display_names(
                    match.get("platforms")
                )
                resolved_slug = game.rawg_slug or match.get("slug")
                resolved_platforms = rawg_platforms or game.rawg_platforms
                self.repository.update_rawg_metadata(
                    game.id,
                    resolved_slug,
                    resolved_platforms,
                )
                updated += 1
            else:
                failed += 1

        return {
            "updated": updated,
            "skipped": skipped,
            "failed": failed,
            "total": len(games),
        }
