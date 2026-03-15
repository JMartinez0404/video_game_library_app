from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class PlayState(Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    PLAYED_ENOUGH = "PLAYED_ENOUGH"
    BEATEN = "BEATEN"
    PLAY_AGAIN = "PLAY_AGAIN"

class Platform(Enum):
    PC = 'PC'
    MAC = 'MAC'
    LINUX = 'LINUX'
    SWITCH = 'SWITCH'
    SWITCH2 = 'SWITCH2'
    PS1 = 'PS1'
    PS2 = 'PS2'
    PS3 = 'PS3'
    PS4 = 'PS4'
    PS5 = 'PS5'
    PS_VITA = 'PS_VITA'
    DS = 'DS'
    THREE_DS = 'THREE_DS'
    WII = 'WII'
    WII_U = 'WII_U'
    GAMECUBE = 'GAMECUBE'
    N64 = 'N64'
    SNES = 'SNES'
    NES = 'NES'
    GAMEBOY = 'GAMEBOY'
    GAMEBOY_COLOR = 'GAMEBOY_COLOR'
    GAMEBOY_ADVANCE = 'GAMEBOY_ADVANCE'
    PSP = 'PSP'
    XBOX = 'XBOX'
    XBOX_360 = 'XBOX_360'
    XBOX_ONE = 'XBOX_ONE'
    XBOX_SERIES = 'XBOX_SERIES'

@dataclass
class VideoGame:
    id: Optional[int]
    title: str
    communal_rating: float
    personal_rating: float
    play_state: PlayState
    platform: Platform
    image_url: str
    release_date: str
    rawg_slug: Optional[str] = None
    rawg_platforms: list[str] = None

    def __post_init__(self) -> None:
        if self.rawg_platforms is None:
            self.rawg_platforms = []
