from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infrastructure.databases.sessions import get_db
from infrastructure.repositories.game_repository import SQLAlchemyGameRepository
from application.game_use_cases import GameService
from domain.entities import VideoGame

router = APIRouter()

@router.post("/video_games")
def add_game(game_data: dict, db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    video_game = VideoGame(id=None, **game_data)
    return service.add_video_game(video_game)

@router.get("/video_games")
def list_games(db: Session = Depends(get_db)):
    repository = SQLAlchemyGameRepository(db)
    service = GameService(repository)

    return service.get_library()
