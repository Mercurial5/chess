from core import Coordinate
from core.game import GameCore


def main():
    game = GameCore()

    while game.playable():
        print(game.current_player)
        continue
        coordinate = Coordinate.parse('Give coordinates -> ')
        user_selected_piece = game[coordinate]
        if not user_selected_piece:
            print('Selected empty coordinate')
            continue

        if user_selected_piece.player != game.current_player:
            print(f'Current player can\'t select this piece - {game.current_player}: {user_selected_piece}')
            continue

        print(f'Selected piece - {user_selected_piece}')
        possible_moves = game.get_possible_moves_for_piece(user_selected_piece, coordinate)
        print(f'Possible moves - {possible_moves}')

        if len(possible_moves) == 0:
            print('Can\'t move this peace')
            continue

        user_selected_coordinate = coordinate.parse('Give move coordinates -> ')
        if user_selected_coordinate in possible_moves:
            print('Right move!')
        else:
            print('Wrong move!')
            continue

        game.move(coordinate, user_selected_coordinate, user_selected_piece)


if __name__ == '__main__':
    main()
