import os
import pygame
from itertools import combinations
from random import shuffle

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет текста.
TEXT_COLOR = (43, 35, 217)
# Время на ответ в секундах.
TIME_LIMIT_ANSWER = 4


class Number():
    def __init__(self,
                 x_coordinate=SCREEN_WIDTH/3,
                 y_coordinate=SCREEN_HEIGHT/2):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.height_number = 10
        self.time_ansver = None
        self.color = TEXT_COLOR

    def answer_time(self, start_time, stop_time):
        self.time_ansver = stop_time - start_time


def handle_keys() -> None:
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                next_direction = UP
            elif event.key == pygame.K_DOWN:
                next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                next_direction = RIGHT


def display_clear(screen) -> None:
    """Очистка дисплея."""
    rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
    pygame.display.update()


def main():
    # Настройка игрового окна:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Пифагоровы штаны')

    set_stop_numbers = [2, 4]
    set_of_numbers = [x for x in range(1, 9) if x not in set_stop_numbers]
    combinations_numbers = list(combinations(set_of_numbers, 2))
    shuffle(combinations_numbers)
    while True:
        handle_keys()
    display_clear(screen)


if __name__ == '__main__':
    main()
