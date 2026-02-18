from sqlalchemy.orm import Session
from domain.entities import VideoGame
from domain.repositories import GameRepository
from infrastructure.database.models import GameModel

class SQLAlchemyGameRepository(GameRepository):

    def __init__(self, db: Session):
        self.db = db

    def add(self, video_game: VideoGame) -> VideoGame:
        db_game = GameModel(
            title=video_game.title,
            communal_rating=video_game.communal_rating,
            personal_rating=video_game.personal_rating,
            play_state=video_game.play_state,
            platform=video_game.platform,
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

    def list(self):
        video_games = self.db.query(GameModel).all()
        return [
            VideoGame(
                id=g.id,
                title=g.title,
                communal_rating=g.communal_rating,
                personal_rating=g.personal_rating,
                play_state=g.play_state,
                platform=g.platform,
                image_url=g.image_url,
                release_date=g.release_date
            )
            for g in video_games
        ]
