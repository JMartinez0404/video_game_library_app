from dataclasses import dataclass
from enum import Enum, auto

class PlayState(Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    PLAYED_ENOUGH = "PLAYED_ENOUGH"
    BEATEN = "BEATEN"
    PLAY_AGAIN = "PLAY_AGAIN"

class Platform(Enum):
    SWITCH = 'SWITCH'
    SWITCH2 = 'SWITCH2'
    PS1 = 'PS1'
    PS2 = 'PS2'
    PS3 = 'PS3'
    PS4 = 'PS4'
    PS5 = 'PS5'
    DS = 'DS'
    THREE_DS = 'THREE_DS'
    WII = 'WII'
    PSP = 'PSP'
    XBOX = 'XBOX'

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
