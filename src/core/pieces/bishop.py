from core import Coordinate
from core.pieces.piece import Piece


class Bishop(Piece):
    code = 'B'
    value = 3

    def get_moves(self, initial_coordinate: Coordinate, game: 'GameCore') -> list[Coordinate]:
        coordinates = []

        # Upper right
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, i, i):
                coordinates.append(coordinate)
            else:
                break

        # Upper left
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, -i, i):
                coordinates.append(coordinate)
            else:
                break

        # Bottom right
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, i, -i):
                coordinates.append(coordinate)
            else:
                break

        # Bottom left
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, -i, -i):
                coordinates.append(coordinate)
            else:
                break

        return coordinates

    def _get_move(self, initial_coordinate: Coordinate, game: 'GameCore', x: int, y: int) -> Coordinate | None:
        coordinate = Coordinate.shift(self.player, initial_coordinate, x, y)
        if not coordinate:
            return

        if game[coordinate] is not None:
            if Piece.is_coordinate_capturable(game, coordinate, self.player):
                return coordinate
            return

        return coordinate
