from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GameModel(Base):
    __tablename__ = "video_games"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    communal_rating = Column(Float)
    personal_rating = Column(Float)
    play_state = Column(String)
    platform = Column(String)
    image_url = Column(String)
    release_date = Column(String)
    rawg_slug = Column(String, nullable=True)
    rawg_platforms = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    progress = Column(Float, nullable=True)
    favorite = Column(Boolean, nullable=True)
    added_at = Column(String, nullable=True)
    last_updated = Column(String, nullable=True)

class ActivityModel(Base):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, nullable=True)
    title = Column(String)
    type = Column(String)
    details = Column(String, nullable=True)
    timestamp = Column(String)
