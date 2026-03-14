from typing import Optional

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from domain.entities import Platform, PlayState, VideoGame
from domain.repositories import GameRepository
from infrastructure.databases.models import GameModel

class SQLAlchemyGameRepository(GameRepository):

    def __init__(self, db: Session):
        self.db = db

    def add(self, video_game: VideoGame) -> VideoGame:
        db_game = GameModel(
            title=video_game.title,
            communal_rating=video_game.communal_rating,
            personal_rating=video_game.personal_rating,
            play_state=video_game.play_state.name,
            platform=video_game.platform.name,
            image_url=video_game.image_url,
            release_date=video_game.release_date
        )

        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)

        return VideoGame(
            id=db_game.id,
            title=db_game.title,
            communal_rating=db_game.communal_rating,
            personal_rating=db_game.personal_rating,
            play_state=db_game.play_state,
            platform=db_game.platform,
            image_url=db_game.image_url,
            release_date=db_game.release_date
        )

    def list(
        self,
        platform: Optional[Platform] = None,
        play_state: Optional[PlayState] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ):
        query = self.db.query(GameModel)
        if platform is not None:
            query = query.filter(GameModel.platform == platform.name)
        if play_state is not None:
            query = query.filter(GameModel.play_state == play_state.name)
        if sort_by is not None:
            sort_column = getattr(GameModel, sort_by)
            order = asc if sort_order == "asc" else desc
            query = query.order_by(order(sort_column))

        video_games = query.all()
        return [
            VideoGame(
                id=g.id,
                title=g.title,
                communal_rating=g.communal_rating,
                personal_rating=g.personal_rating,
                play_state=PlayState[g.play_state],
                platform=Platform[g.platform],
                image_url=g.image_url,
                release_date=g.release_date
            )
            for g in video_games
        ]
    
    def delete_all(self) -> None:
        self.db.query(GameModel).delete(synchronize_session=False)
        self.db.commit()
    
    def delete(self, game_name: str) -> VideoGame:
        game_to_delete = self.db.execute(select(GameModel).filter_by(title=game_name)).scalar_one()
        self.db.delete(game_to_delete)
        self.db.commit()

        return VideoGame(
            id=game_to_delete.id,
            title=game_to_delete.title,
            communal_rating=game_to_delete.communal_rating,
            personal_rating=game_to_delete.personal_rating,
            play_state=PlayState[game_to_delete.play_state],
            platform=Platform[game_to_delete.platform],
            image_url=game_to_delete.image_url,
            release_date=game_to_delete.release_date,
        )
