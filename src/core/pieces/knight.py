from core import Coordinate
from core.pieces.piece import Piece


class Knight(Piece):
    code = 'N'
    value = 3

    def get_moves(self, initial_coordinate: 'Coordinate', game: 'GameCore') -> list['Coordinate']:
        coordinates = [
            self._get_move(initial_coordinate, game, 1, 2),
            self._get_move(initial_coordinate, game, 1, -2),
            self._get_move(initial_coordinate, game, -1, 2),
            self._get_move(initial_coordinate, game, -1, -2),
            self._get_move(initial_coordinate, game, 2, 1),
            self._get_move(initial_coordinate, game, 2, -1),
            self._get_move(initial_coordinate, game, -2, 1),
            self._get_move(initial_coordinate, game, -2, -1),
        ]

        return [coordinate for coordinate in coordinates if coordinate]
