from pydantic import BaseModel, HttpUrl
from domain.entities import PlayState, Platform


class VideoGameCreate(BaseModel):
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: HttpUrl
    release_date: str


class VideoGameResponse(BaseModel):
    id: int
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: HttpUrl
    release_date: str

    class Config:
        from_attributes = True
