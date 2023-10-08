from core.coordinate import Coordinate
from core.pieces.piece import Piece


class Pawn(Piece):
    code = 'p'
    value = 1

    def get_moves(self, initial_coordinate: Coordinate, game: 'GameCore') -> list[Coordinate]:
        coordinates = []

        # Move forward by 2
        coordinate = Coordinate.shift(self.player, initial_coordinate, 0, 1)
        if coordinate and game[coordinate] is None:
            coordinates = [coordinate]

        # Move forward by 2
        if not self.moved:
            coordinate = Coordinate.shift(self.player, initial_coordinate, 0, 2)
            if coordinate and game[coordinate] is None:
                coordinates.append(coordinate)

        # Capture left
        coordinate = Coordinate.shift(self.player, initial_coordinate, -1, 1)
        if coordinate and Piece.is_coordinate_capturable(game, coordinate, self.player):
            coordinates.append(coordinate)

        # Capture right
        coordinate = Coordinate.shift(self.player, initial_coordinate, 1, 1)
        if coordinate and Piece.is_coordinate_capturable(game, coordinate, self.player):
            coordinates.append(coordinate)

        return coordinates
