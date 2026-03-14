from dataclasses import asdict

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.databases.sessions import get_db
from infrastructure.external_apis.rawg_client import RawgClient
from infrastructure.repositories.game_repository import SQLAlchemyGameRepository
from application.external_game_service import ExternalGameService
from application.game_use_cases import GameService
from application.errors import ExternalApiError
from domain.entities import PlayState, Platform, VideoGame
from presentation.schemas import (
    ExternalGameResponse,
    ExternalGameSearchResponse,
    VideoGameCreate,
    VideoGameResponse,
)


RAWG_API_KEY = "ca49543276b64af4b3af67f44b3944eb"

router = APIRouter()

@router.post("/video_games", response_model=VideoGameResponse)
def add_game(
    game_data: VideoGameCreate,
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    video_game = VideoGame(
        id=None,
        **game_data.model_dump()
    )

    return service.add_video_game(video_game)


@router.get("/video_games", response_model=list[VideoGameResponse])
def list_games(
    platform: Optional[Platform] = None,
    play_state: Optional[PlayState] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    db: Session = Depends(get_db),
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    try:
        return service.get_library(
            platform=platform,
            play_state=play_state,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.delete("/video_games")
def delete_all_games(db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    service.delete_all_video_games()

    return {"message": "All video games removed"}

@router.delete("/video_games/{game_name}", response_model=VideoGameResponse)
def delete_games(game_name: str, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    return service.delete_video_game(game_name)

@router.get(
    "/external/video_games/search",
    response_model=ExternalGameSearchResponse,
)
def search_external_games_by_name(
    game_name: str,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)

    try:
        results = service.search_by_name(
            game_name,
            page=page,
            page_size=page_size,
        )
    except ExternalApiError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return ExternalGameSearchResponse(
        count=results.count,
        next=results.next,
        previous=results.previous,
        results=[ExternalGameResponse(**asdict(dto)) for dto in results.results],
    )

@router.get(
    "/external/video_games/{game_id}",
    response_model=ExternalGameResponse,
)
def get_external_game_by_id(game_id: int, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)

    try:
        dto = service.get_by_id(game_id)
    except ExternalApiError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc
    return ExternalGameResponse(**asdict(dto))

@router.post(
    "/external/video_games/{game_id}/import",
    response_model=VideoGameResponse
)
def import_external_game(game_id: int, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)

    try:
        return service.import_game_by_id(game_id)
    except ExternalApiError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc

@router.post("/external/video_games/backfill_slugs")
def backfill_external_game_slugs(db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)

    return service.backfill_rawg_slugs()
