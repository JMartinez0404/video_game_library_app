from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infrastructure.databases.sessions import get_db
from infrastructure.repositories.game_repository import SQLAlchemyGameRepository
from application.game_use_cases import GameService
from domain.entities import VideoGame
from presentation.schemas import VideoGameCreate, VideoGameResponse


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
