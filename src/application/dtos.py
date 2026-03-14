from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ExternalGameDTO:
    id: int
    title: str
    communal_rating: Optional[float]
    image_url: Optional[str]
    release_date: Optional[str]
    rawg_slug: Optional[str]
    rawg_platforms: list[str]


@dataclass
class ExternalGameSearchResult:
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[ExternalGameDTO]
