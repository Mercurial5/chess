from core import Coordinate
from core.pieces.piece import Piece


class King(Piece):
    code = 'K'
    value = 100

    def get_moves(self, initial_coordinate: 'Coordinate', game: 'GameCore') -> list['Coordinate']:
        coordinates = [
            self._get_move(initial_coordinate, game, 0, 1),
            self._get_move(initial_coordinate, game, 0, -1),
            self._get_move(initial_coordinate, game, 1, 0),
            self._get_move(initial_coordinate, game, -1, 0),
            self._get_move(initial_coordinate, game, 1, -1),
            self._get_move(initial_coordinate, game, -1, 1),
            self._get_move(initial_coordinate, game, 1, 1),
            self._get_move(initial_coordinate, game, -1, -1),
        ]

        return [coordinate for coordinate in coordinates if coordinate]
