from core import Coordinate
from core.pieces.piece import Piece


class Rook(Piece):
    code = 'R'
    value = 5

    def get_moves(self, initial_coordinate: 'Coordinate', game: 'GameCore') -> list[Coordinate]:
        coordinates = []

        # Forward
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, 0, i):
                coordinates.append(coordinate)
            else:
                break

        # Backward
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, 0, -i):
                coordinates.append(coordinate)
            else:
                break

        # Left
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, i, 0):
                coordinates.append(coordinate)
            else:
                break

        # Right
        for i in range(1, 8):
            if coordinate := self._get_move(initial_coordinate, game, -i, 0):
                coordinates.append(coordinate)
            else:
                break

        return coordinates
