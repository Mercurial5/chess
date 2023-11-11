import pygame
from pygame import Surface
from pygame.event import Event

from core import GameCore, Coordinate


class GameUI:
    BOARD_WIDTH = BOARD_HEIGHT = 512
    DIMENSION = 8
    SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
    PIECE_SIZE = (SQUARE_SIZE, SQUARE_SIZE)
    IMAGES: dict[str, Surface] = {}
    MAX_FPS = 15

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.screen.fill(pygame.Color('white'))

        self.clock = pygame.time.Clock()
        self.__load_images()

        self.game_core = GameCore()
        # for column in range(8):
        #     for row in range(8):
        #         coordinate = Coordinate(row, column)
        #         print(self.game_core[coordinate], end=' ')
        #     print()

        self.last_selected_coordinate: Coordinate | None = None
        # Holds last two clicks so that we can make a move
        self.player_clicks: list[Coordinate] = []
        self.possible_moves: list[Coordinate] = []

        self.current_player = self.game_core.current_player

    def start(self):
        game_over = False

        while self.game_core.playable() and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

                self._handle_event(event)

            self._draw_board()
            self._draw_pieces()
            self._highlight_squares()

            if self.game_core.white_won:
                self.game_over_screen('White won!')
                game_over = True
            elif self.game_core.black_won:
                self.game_over_screen('Black won!')
                game_over = True

            self.clock.tick(self.MAX_FPS)
            pygame.display.flip()

        pygame.time.delay(3000)
        pygame.quit()

    def game_over_screen(self, message):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, pygame.Color('black'))
        text_rect = text.get_rect(center=(self.BOARD_WIDTH // 2, self.BOARD_HEIGHT // 2))

        self.screen.fill(pygame.Color('white'))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def _handle_event(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            column, row = int(location[0] // self.SQUARE_SIZE), int(location[1] // self.SQUARE_SIZE)

            coordinate = Coordinate(column, row)
            piece = self.game_core[coordinate]
            print(f'Selected coordinate - {coordinate}')
            print(f'Piece in selected coordinate - {piece}')

            # If this is the first click
            if self.last_selected_coordinate is None:
                print('First click')
                # If the coordinate is empty:
                if self.game_core[coordinate] is None:
                    print('Selected coordinate is empty, not doing anything')
                    return

                # If the coordinate holds piece of another player
                if piece.player != self.current_player:
                    print('Selected coordinate holds a piece of another player, not doing anything')
                    return

                # If the coordinate holds piece of current player
                self.last_selected_coordinate = coordinate
                self.player_clicks.append(coordinate)
                self.possible_moves = self.game_core.get_possible_moves_for_piece(piece, coordinate)
                print(f'Selected coordinate holds your piece, possible moves - {self.possible_moves}')
                return

            # Conditions below know, that this is the second click
            print('Second click')

            # If user clicked at the previous coordinate
            if coordinate == self.last_selected_coordinate:
                print('Selected previous coordinate, clearing everything')
                self.last_selected_coordinate = None
                self.player_clicks = []
                self.possible_moves = []
                return

            # If coordinate is one of the possible moves
            if coordinate in self.possible_moves:
                last_piece = self.game_core[self.last_selected_coordinate]

                # Check if the move puts the own king in check
                if not self.game_core.is_move_legal(self.last_selected_coordinate, coordinate, self.current_player):
                    print('Illegal move - puts own king in check')
                    return

                self.game_core.move(self.last_selected_coordinate, coordinate, last_piece)
                self.last_selected_coordinate = None
                self.player_clicks = []
                self.possible_moves = []
                self.current_player = self.game_core.current_player
                return

            print('Coordinate is not possible move, clearing everything')
            self.last_selected_coordinate = None
            self.player_clicks = []
            self.possible_moves = []

    def _draw_board(self) -> None:
        colors = [pygame.Color('white'), pygame.Color('gray')]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                color = colors[(row + column) % 2]

                rectangle_size = column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE
                pygame.draw.rect(self.screen, color, rectangle_size)

    def _draw_pieces(self) -> None:
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                coordinate = Coordinate(column, row)
                piece = self.game_core[coordinate]

                rectangle_size = column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE
                if piece is not None:
                    self.screen.blit(self.IMAGES[piece.code], pygame.Rect(rectangle_size))

    def _highlight_squares(self) -> None:
        if self.last_selected_coordinate is None:
            return

        piece = self.game_core[self.last_selected_coordinate]
        if piece.player == self.current_player:
            s = pygame.Surface(self.PIECE_SIZE)
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))

            row, column = self.last_selected_coordinate.x, self.last_selected_coordinate.y
            self.screen.blit(s, (row * self.SQUARE_SIZE, column * self.SQUARE_SIZE))

        for coordinate in self.possible_moves:
            s = pygame.Surface(self.PIECE_SIZE)
            s.set_alpha(100)
            s.fill(pygame.Color('yellow'))

            row, column = coordinate.x, coordinate.y
            self.screen.blit(s, (row * self.SQUARE_SIZE, column * self.SQUARE_SIZE))

    def __load_images(self):
        pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp', 'bp']
        for piece in pieces:
            self.IMAGES[piece] = self.__load_image(piece)

    def __load_image(self, piece: str) -> Surface:
        image_path = f'images/{piece}.png'
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, self.PIECE_SIZE)
