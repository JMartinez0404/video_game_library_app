from dataclasses import asdict
from datetime import datetime

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.databases.sessions import get_db
from infrastructure.external_apis.rawg_client import RawgClient
from infrastructure.repositories.activity_repository import SQLAlchemyActivityRepository
from infrastructure.repositories.game_repository import SQLAlchemyGameRepository
from application.external_game_service import ExternalGameService
from application.game_use_cases import GameService
from application.errors import ExternalApiError
from domain.entities import PlayState, Platform, VideoGame, ActivityEntry
from presentation.auth import verify_api_key
from presentation.schemas import (
    ActivityResponse,
    ExternalGameResponse,
    ExternalGameSearchResponse,
    ImportHistoryResponse,
    VideoGameCreate,
    VideoGameResponse,
    VideoGameUpdate,
)


RAWG_API_KEY = "ca49543276b64af4b3af67f44b3944eb"

router = APIRouter()

@router.post("/video_games", response_model=VideoGameResponse)
def add_game(
    game_data: VideoGameCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)
    activity_repo = SQLAlchemyActivityRepository(db)

    video_game = VideoGame(
        id=None,
        **game_data.model_dump()
    )
    saved = service.add_video_game(video_game)
    activity_repo.add(
        ActivityEntry(
            id=None,
            game_id=saved.id,
            title=saved.title,
            type="add",
            details=None,
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return saved


@router.get("/video_games", response_model=list[VideoGameResponse])
def list_games(
    platform: Optional[Platform] = None,
    play_state: Optional[PlayState] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
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
def delete_all_games(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    service.delete_all_video_games()

    return {"message": "All video games removed"}

@router.delete("/video_games/{game_name}", response_model=VideoGameResponse)
def delete_games(
    game_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)
    activity_repo = SQLAlchemyActivityRepository(db)
    deleted = service.delete_video_game(game_name)
    activity_repo.add(
        ActivityEntry(
            id=None,
            game_id=deleted.id,
            title=deleted.title,
            type="remove",
            details=None,
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return deleted

@router.patch("/video_games/{game_id}", response_model=VideoGameResponse)
def update_game(
    game_id: int,
    game_data: VideoGameUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)
    activity_repo = SQLAlchemyActivityRepository(db)
    updated = service.update_video_game(
        game_id=game_id,
        personal_rating=game_data.personal_rating,
        platform=game_data.platform,
        notes=game_data.notes,
        tags=game_data.tags,
        progress=game_data.progress,
        favorite=game_data.favorite,
    )
    detail_parts = []
    if game_data.platform is not None:
        detail_parts.append(f"platform={game_data.platform.name}")
    if game_data.personal_rating is not None:
        detail_parts.append(f"personal_rating={game_data.personal_rating}")
    if game_data.notes is not None:
        detail_parts.append("notes")
    if game_data.tags is not None:
        detail_parts.append("tags")
    if game_data.progress is not None:
        detail_parts.append(f"progress={game_data.progress}")
    if game_data.favorite is not None:
        detail_parts.append(f"favorite={game_data.favorite}")
    activity_repo.add(
        ActivityEntry(
            id=None,
            game_id=updated.id,
            title=updated.title,
            type="update",
            details=", ".join(detail_parts) if detail_parts else None,
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return updated

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
    api_key: str = Depends(verify_api_key),
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)
    activity_repo = SQLAlchemyActivityRepository(db)

    try:
        imported = service.import_game_by_id(game_id)
        activity_repo.add(
            ActivityEntry(
                id=None,
                game_id=imported.id,
                title=imported.title,
                type="import",
                details=None,
                timestamp=datetime.utcnow().isoformat(),
            )
        )
        return imported
    except ExternalApiError as exc:
        raise HTTPException(status_code=502, detail=exc.message) from exc

@router.post("/external/video_games/backfill_slugs")
def backfill_external_game_slugs(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = ExternalGameService(repository, rawg_client)

    return service.backfill_rawg_slugs()

@router.get("/activity", response_model=list[ActivityResponse])
def list_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    activity_repo = SQLAlchemyActivityRepository(db)
    entries = activity_repo.list(limit=limit)
    return [
        ActivityResponse(
            id=entry.id,
            game_id=entry.game_id,
            title=entry.title,
            type=entry.type,
            details=entry.details,
            timestamp=entry.timestamp,
        )
        for entry in entries
    ]

@router.get("/imports", response_model=list[ImportHistoryResponse])
def list_import_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    activity_repo = SQLAlchemyActivityRepository(db)
    entries = activity_repo.list_imports(limit=limit)
    return [
        ImportHistoryResponse(
            game_id=entry.game_id or 0,
            title=entry.title,
            timestamp=entry.timestamp,
        )
        for entry in entries
    ]
