from __future__ import annotations

from dataclasses import dataclass

from core.player import PlayerType, Player


@dataclass
class Coordinate:
    x: int
    y: int

    @classmethod
    def parse(cls, msg: str) -> Coordinate:
        x, y = map(int, input(msg).split())
        return Coordinate(x, y)

    @staticmethod
    def shift(player: Player, initial_coordinate: Coordinate, x: int = 0, y: int = 0) -> Coordinate | None:
        if player.type == PlayerType.white:
            x *= -1
            y *= -1

        coordinate = Coordinate(initial_coordinate.x + x, initial_coordinate.y + y)
        if 0 <= coordinate.y <= 7 and 0 <= coordinate.x <= 7:
            return coordinate
