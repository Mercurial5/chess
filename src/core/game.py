from __future__ import annotations

from typing import Iterator

from core.pieces import Piece
from core.pieces.bishop import Bishop
from core.pieces.king import King
from core.pieces.knight import Knight
from core.pieces.pawn import Pawn
from core.pieces.queen import Queen
from core.pieces.rook import Rook
from core.player import Player, PlayerType


class GameCore:
    white: Player = Player(type=PlayerType.white)
    black: Player = Player(type=PlayerType.black)
    _board: list[list[Piece | None]]

    def __init__(self):
        self._board = self.__initialize_board()

        def __get_current_player() -> Iterator[Player]:
            while True:
                yield self.white
                yield self.black

        self.__get_current_player = __get_current_player()
        self._playable = True
        self.white_won = False
        self.black_won = False

    def playable(self) -> bool:
        return self._playable

    @property
    def current_player(self) -> Player:
        return self.__get_current_player.__next__()

    def get_possible_moves_for_piece(self, piece: Piece, initial_coordinate: 'Coordinate') -> list['Coordinate']:
        return piece.get_moves(initial_coordinate, self)

    def __initialize_board(self) -> list[list[Piece | None]]:
        order_of_pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        empty_rows = [[None for _ in range(8)] for _ in range(4)]

        first_row = [piece(self.black) for piece in order_of_pieces]
        second_row = [Pawn(self.black) for _ in range(8)]

        r_first_row = [piece(self.white) for piece in order_of_pieces]
        r_second_row = [Pawn(self.white) for _ in range(8)]

        board = [first_row, second_row, *empty_rows, r_second_row, r_first_row]

        return board

    def __getitem__(self, item: 'Coordinate') -> Piece | None:
        return self._board[item.y][item.x]

    def __setitem__(self, key: 'Coordinate', value) -> None:
        self._board[key.y][key.x] = value

    def move(self, coordinate: Coordinate, user_selected_coordinate: Coordinate, user_selected_piece: Piece):
        if piece_to_be_captured := self[user_selected_coordinate]:
            if piece_to_be_captured.code[1] == 'K':
                self._playable = False

                self.white_won = user_selected_piece.player.type == PlayerType.white
                self.black_won = user_selected_piece.player.type == PlayerType.black

        self[coordinate] = None
        self[user_selected_coordinate] = user_selected_piece
        user_selected_piece.moved = True


from core.coordinate import Coordinate
