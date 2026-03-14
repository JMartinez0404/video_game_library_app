from dataclasses import dataclass
from typing import Optional


@dataclass
class ExternalGameDTO:
    id: int
    title: str
    communal_rating: Optional[float]
    image_url: Optional[str]
    release_date: Optional[str]
