from dataclasses import dataclass
from enum import Enum, auto

class PlayState(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    PLAYED_ENOUGH = auto()
    BEATEN = auto()
    PLAY_AGAIN = auto()

class Platform(Enum):
    SWITCH = auto()
    SWITCH2 = auto()
    PS1 = auto()
    PS2 = auto()
    PS3 = auto()
    PS4 = auto()
    PS5 = auto()
    DS = auto()
    THREE_DS = auto()
    WII = auto()
    PSP = auto()

@dataclass
class VideoGame:
    id: int | None
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: str
    release_date: str
