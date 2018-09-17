import pygame
import sys
import random
from pygame.locals import *
from main import PuzzleMap
from button import Button

FPS = 60
BOARD_HEIGHT = 5
BOARD_WIDTH = 5

BOX_SIZE = 100
GAP_SIZE = 5
MARGIN_SIZE = 10
CHOICE_WIDTH = 50
CHOICE_HEIGHT = 30
INFO_SIZE = 0
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FONT_SIZE = 24
FONT_SIZE_SMALL = 14
ANIMATE_SPEED = 20

ROW_INDEX = 0
CELL_INDEX = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BOX_COLOR = GREEN
FONT_COLOR = BLACK
BG_COLOR = BLUE


class Game:

    puzzle_pieces_choices = []
    scores = []
    best_index = -1
    index = 0
    iteration = 0

    def __init__(self):
        self.main()

    def finish(self):
        while not self.puzzle_map.flag_done:
            self.next_move()

    def next_move(self):
        try:
            self.puzzle_pieces_choices, self.scores, self.index, self.best_index = self.puzzle_map.reorder()
            print(self.puzzle_pieces_choices)
            self.iteration += 1
        except:
            print("TERMINADO")

    def main(self):
        global DISPLAY_SURFACE, FPSCLOCK, FONT, FONT_SMALL
        pygame.init()

        FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        FONT_SMALL = pygame.font.Font("freesansbold.ttf", FONT_SIZE_SMALL)
        FPSCLOCK = pygame.time.Clock()
        DISPLAY_SURFACE = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Puzzle IA")

        while True:
            self.play_game()

    def play_game(self):
        self.puzzle_map = PuzzleMap("imagen.png", 4)

        self.btn_movement = Button((10, 10, 200, 50), self.next_move,
                                   hover_color=(100, 100, 100), text="Siguiente Mov.")
        self.btn_complete = Button((220, 10, 220, 50), self.finish,
                                   hover_color=(100, 100, 100), text="Completar Puzzle")

        self.img_original = pygame.image.load(self.puzzle_map.route)
        self.img_original = pygame.transform.rotozoom(
            self.img_original, 0, 0.5)

        for i in range(0, len(self.puzzle_map.pieces)):
            temp_img = pygame.image.load(self.puzzle_map.pieces[i].route)
            temp_img = pygame.transform.rotozoom(
                temp_img, 0, 0.5)
            self.puzzle_map.pieces[i].pyimage = temp_img
        self.draw_board()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.btn_movement.on_click()
                    self.btn_complete.on_click()
            self.draw_board()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def game_start(self):
        print("GAME START")

    def draw_board(self):
        DISPLAY_SURFACE.fill(BG_COLOR)
        DISPLAY_SURFACE.blit(self.img_original, (10, 80))
        self.btn_movement.draw(DISPLAY_SURFACE)
        self.btn_complete.draw(DISPLAY_SURFACE)

        self.text_label((MARGIN_SIZE, WINDOW_HEIGHT - 24,
                         FONT_SIZE_SMALL, FONT_SIZE_SMALL), str(self.iteration))

        self.draw_box((MARGIN_SIZE + self.puzzle_map.width *
                       2 * 0.6, 80, self.puzzle_map.width * 0.6, self.puzzle_map.height * 0.6), "Solucion")

        for i in range(0, len(self.puzzle_map.pieces)):
            DISPLAY_SURFACE.blit(self.puzzle_map.pieces[i].pyimage, (
                self.puzzle_map.width * 0.6 + self.puzzle_map.pieces[i].x * 0.6, 80 + self.puzzle_map.pieces[i].y * 0.6))
            color = FONT_COLOR
            if i == self.index:
                color = RED
            self.text_box((
                self.puzzle_map.width * 0.6 + self.puzzle_map.pieces[i].x * 0.6, 80 + self.puzzle_map.pieces[i].y * 0.6), str(i), color)
            if self.puzzle_map.pieces[i].completed == True:
                self.text_box((
                    self.puzzle_map.width * 0.6 + self.puzzle_map.pieces[i].x * 0.6 + 16, 80 + self.puzzle_map.pieces[i].y * 0.6), "C", RED)

            if self.puzzle_map.pieces[i].solution_box is not None:
                x, y = self.puzzle_map.pieces[i].solution_box[0], self.puzzle_map.pieces[i].solution_box[1]
                DISPLAY_SURFACE.blit(self.puzzle_map.pieces[i].pyimage, (
                    MARGIN_SIZE + self.puzzle_map.width * 2 * 0.6 + x * 0.6, 80 + y * 0.6))

        count = 0
        for i in self.puzzle_pieces_choices:
            DISPLAY_SURFACE.blit(self.puzzle_map.pieces[i].pyimage, (
                MARGIN_SIZE + self.puzzle_map.pieces[i].width * 0.6 * count + CHOICE_WIDTH * count, 80 + self.puzzle_map.height * 0.7))
            color = FONT_COLOR
            if i == self.best_index:
                color = RED
            self.text_label((MARGIN_SIZE + self.puzzle_map.pieces[i].width * 0.6 * count + CHOICE_WIDTH * (count + 1), 80 +
                             self.puzzle_map.height * 0.7, CHOICE_HEIGHT, CHOICE_WIDTH), self.scores[count], color)
            count += 1

    def draw_box(self, rect, text):
        label = FONT.render(str(text), True, FONT_COLOR)
        label_rect = label.get_rect()
        box = pygame.Rect(rect)
        label_rect.center = box.center
        pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, box)
        DISPLAY_SURFACE.blit(label, label_rect)

    def text_box(self, dest, text, color=FONT_COLOR):
        label = FONT_SMALL.render(str(text), True, color)
        label_rect = dest
        DISPLAY_SURFACE.blit(label, label_rect)

    def text_label(self, rect, text, color=FONT_COLOR):
        label = FONT_SMALL.render(str(text), True, color)
        label_rect = pygame.Rect(rect)
        DISPLAY_SURFACE.blit(label, label_rect)


game = Game()
