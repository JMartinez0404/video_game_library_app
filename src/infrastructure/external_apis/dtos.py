from pydantic import BaseModel
from typing import Optional


class ExternalGameDTO(BaseModel):
    id: int
    title: str
    communal_rating: Optional[float]
    image_url: Optional[str]
    release_date: Optional[str]
