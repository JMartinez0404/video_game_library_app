from sqlalchemy import Column, Integer, String, Float
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
