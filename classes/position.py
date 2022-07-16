from pathlib import Path
Path(__file__).resolve()
from enum import Enum


class Position(Enum):
    RB = 1
    WR = 2
    QB = 3
    TE = 4
    DST = 5