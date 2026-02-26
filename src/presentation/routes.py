from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infrastructure.databases.sessions import get_db
from infrastructure.external_apis.dtos import ExternalGameDTO
from infrastructure.external_apis.rawg_client import RawgClient
from infrastructure.repositories.game_repository import SQLAlchemyGameRepository
from application.game_use_cases import GameService
from domain.entities import VideoGame
from presentation.schemas import VideoGameCreate, VideoGameResponse


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
def list_games(db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    return service.get_library()

@router.delete("/video_games")
def delete_all_games(db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    service.delete_all_video_games()

    return {"message": "All video games removed"}

@router.delete("/video_games/{game_name}")
def delete_games(game_name: str, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    return service.delete_video_game(game_name)

@router.get("/external/video_games")
def search_external_games_by_name(game_name: str, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = GameService(repository, rawg_client)

    return service.search_external_games_by_name(game_name)

@router.get("/external/video_games/{game_id}", response_model=ExternalGameDTO)
def get_external_game_by_id(game_id: int, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = GameService(repository, rawg_client)

    return service.search_external_game_by_id(game_id)

@router.post(
    "/external/video_games/{game_id}/import",
    response_model=VideoGameResponse
)
def import_external_game_by_id(game_id: int, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    rawg_client = RawgClient(RAWG_API_KEY)
    service = GameService(repository, rawg_client)

    return service.import_external_game_by_id(game_id)
