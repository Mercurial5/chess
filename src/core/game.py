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

    def get_possible_moves_for_piece(self, piece: Piece, initial_coordinate: Coordinate) -> list[Coordinate]:
        all_possible_moves = piece.get_moves(initial_coordinate, self)
        legal_moves = []

        for move in all_possible_moves:
            if self.is_move_legal(initial_coordinate, move, piece.player):
                legal_moves.append(move)

        return legal_moves

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

    def is_move_legal(self, start_coordinate, end_coordinate, current_player):
        # Copy the current board to simulate the move
        simulated_board = [row[:] for row in self._board]
        piece_to_move = simulated_board[start_coordinate.y][start_coordinate.x]
        simulated_board[start_coordinate.y][start_coordinate.x] = None
        simulated_board[end_coordinate.y][end_coordinate.x] = piece_to_move

        # Check if the move exposes the own king to check (i.e., not legal)
        if self.is_king_in_check(simulated_board, current_player):
            return False

        # Check if the moved piece is pinned
        if self.is_pinned_piece(start_coordinate, end_coordinate, current_player):
            return False

        return True

    def is_pinned_piece(self, start_coordinate, end_coordinate, current_player):
        # Check if the moved piece is pinned
        piece_to_move = self._board[start_coordinate.y][start_coordinate.x]
        king_coordinate = self.find_king_coordinate(self._board, current_player)

        # Check if the piece is pinned along the line of sight to the king
        for direction in piece_to_move.get_moves(start_coordinate, self):
            # Check each square along the line of sight
            temp_coordinate = start_coordinate + direction
            while 0 <= temp_coordinate.x < 8 and 0 <= temp_coordinate.y < 8:
                if temp_coordinate == end_coordinate:
                    break  # Stop when reaching the destination square
                elif self._board[temp_coordinate.y][temp_coordinate.x] is not None:
                    # If there's a piece in the line of sight, check if it's an enemy piece
                    blocking_piece = self._board[temp_coordinate.y][temp_coordinate.x]
                    if blocking_piece.player != current_player:
                        # Check if the blocking piece is a rook or queen, pinning the piece
                        if isinstance(blocking_piece, Rook) or isinstance(blocking_piece, Queen):
                            # The moved piece is pinned
                            return True
                    break  # Stop checking along the line of sight if there's a piece
                temp_coordinate += direction

        return False

    def is_king_in_check(self, board: list[list[Piece | None]], player: Player) -> bool:
        # Check if the king of the specified player is in check
        king_coordinate = self.find_king_coordinate(board, player)
        opposing_player = self.white if player.type == PlayerType.black else self.black

        # Check if any opposing player's piece can attack the king's coordinate
        for row in board:
            for piece in row:
                if piece and piece.player == opposing_player:
                    possible_moves = piece.get_moves(Coordinate(row.index(piece), board.index(row)), self)
                    if king_coordinate in possible_moves:
                        return True

        return False

    @staticmethod
    def find_king_coordinate(board: list[list[Piece | None]], player: Player) -> Coordinate:
        # Find the coordinate of the king of the specified player
        for row in board:
            for piece in row:
                if isinstance(piece, King) and piece.player == player:
                    return Coordinate(row.index(piece), board.index(row))

    def in_checkmate(self, current_player) -> bool:
        # Check if the current player is in checkmate
        # A player is in checkmate if their king is in check, and there are no legal moves to get out of check

        # Copy the current board to simulate each possible move
        for row in self._board:
            for piece in row:
                if piece and piece.player == current_player:
                    current_coordinate = Coordinate(row.index(piece), self._board.index(row))
                    possible_moves = self.get_possible_moves_for_piece(piece, current_coordinate)
                    for move in possible_moves:
                        if self.is_move_legal(current_coordinate, move, current_player):
                            return False

        return True


from core.coordinate import Coordinate
