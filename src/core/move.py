from dataclasses import dataclass

from core.coordinate import Coordinate
from core.pieces import Piece


@dataclass
class Move:
    old_square: Coordinate
    new_square: Coordinate
    moving_piece: Piece
    captured_piece: Piece | None
