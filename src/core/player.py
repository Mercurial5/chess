from dataclasses import dataclass
from enum import Enum


class PlayerType(Enum):
    white = 'white'
    black = 'black'


@dataclass
class Player:
    type: PlayerType
