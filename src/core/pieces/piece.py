from __future__ import annotations

from abc import ABC, abstractmethod

from core import Coordinate
from core.player import Player


class Piece(ABC):
    value: int
    code: str
    moved: bool = False
    player: Player

    def __init__(self, player: Player):
        self.player = player
        self.code = player.type.value[0] + self.code
        self.captured = False

    def _get_move(self, initial_coordinate: Coordinate, game: 'GameCore', x: int, y: int) -> Coordinate | None:
        coordinate = Coordinate.shift(self.player, initial_coordinate, x, y)
        if not coordinate:
            return

        if game[coordinate] is not None:
            if not self.captured and Piece.is_coordinate_capturable(game, coordinate, self.player):
                self.captured = True
                return coordinate
            return

        return coordinate

    @abstractmethod
    def get_moves(self, initial_coordinate: 'Coordinate', game: 'GameCore') -> list['Coordinate']:
        raise NotImplementedError

    @staticmethod
    def is_coordinate_capturable(game: 'GameCore', coordinate: Coordinate, player: Player) -> bool:
        return game[coordinate] is not None and game[coordinate].player != player

    @staticmethod
    def is_coordinate_empty(game: 'GameCore', coordinate: Coordinate) -> bool:
        return game[coordinate] is None

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.player}>'
