from typing import Optional

from pydantic import BaseModel, field_validator, HttpUrl
from domain.entities import PlayState, Platform


class VideoGameCreate(BaseModel):
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: HttpUrl
    release_date: str
    rawg_slug: Optional[str] = None
    rawg_platforms: list[str] | None = None

    #TODO: Check if this is okay
    @field_validator('image_url', mode='after')
    @classmethod
    def convert_httpurl_to_str(cls, image_url: HttpUrl) -> HttpUrl:
        '''
            pydantic vaidates if the parameter is a HttpUrl so here we're
            converting it to a str to insert into a database.
        '''
        return str(image_url)

class VideoGameResponse(BaseModel):
    id: int
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: HttpUrl
    release_date: str
    rawg_slug: Optional[str] = None
    rawg_platforms: list[str] | None = None

    class Config:
        from_attributes = True


class ExternalGameResponse(BaseModel):
    id: int
    title: str
    communal_rating: Optional[float]
    image_url: Optional[HttpUrl]
    release_date: Optional[str]
    rawg_slug: Optional[str]
    rawg_platforms: list[str] | None = None


class VideoGameUpdate(BaseModel):
    personal_rating: Optional[float] = None
    platform: Optional[Platform] = None


class ExternalGameSearchResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: list[ExternalGameResponse]
