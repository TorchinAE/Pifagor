# import os
import pygame
from itertools import combinations
from random import shuffle

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет текста.
TEXT_COLOR = (255, 255, 255)
# Время на ответ в секундах.
TIME_LIMIT_ANSWER = 4
# Смещение цифр по х.
DELTA_X = 30
# Высота шрифта.
HEIGH_NUM = 80

NUMBER_KEYBOARD = [1073741922, 1073741913, 1073741914, 1073741915, 1073741916,
                   1073741917, 1073741918, 1073741919, 1073741920, 1073741921]
NUMBER_KEYBOARD_HI = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]


class Number():
    def __init__(self,
                 value=0,
                 coordinate=(SCREEN_WIDTH/3-10, SCREEN_HEIGHT/2-HEIGH_NUM/2)
                 ):
        self.value = value
        self.coordinate = coordinate
        self.height_number = HEIGH_NUM
        self.time_ansver = None
        self.color = TEXT_COLOR
        self.len_num = len(str(value))

    def delta(self, x=0, y=0):
        self.coordinate = (self.coordinate[0]+x, self.coordinate[1]+y)

    def answer_time(self, start_time, stop_time):
        self.time_ansver = stop_time - start_time

    def draw(self, screen):
        """Вывод текста на экран."""
        pygame.font.init()
        font = pygame.font.Font(None, self.height_number)
        text = font.render(str(self.value), True, self.color)
        text_rect = text.get_rect(topleft=(self.coordinate))
        screen.blit(text, text_rect)
        pygame.display.update()


def handle_keys() -> None:
    """Функция обработки действий пользователя."""
    pressed_digit = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in (NUMBER_KEYBOARD_HI):
                pressed_digit = pygame.key.name(event.key)
            elif event.key in NUMBER_KEYBOARD:
                pressed_digit = pygame.key.name(event.key)[1]
            elif (pygame.key.name(event.key) == 'enter' or
                  pygame.key.name(event.key) == 'return'):
                pressed_digit = -1
    return pressed_digit


def display_clear(screen) -> None:
    """Очистка дисплея."""
    rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
    pygame.display.update()


def display_write(screen, arr_num):
    display_clear(screen)
    for x in arr_num:
        x.draw(screen)


def main():
    # Настройка игрового окна:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Пифагоровы штаны')

    set_stop_numbers = [2, 4]
    set_of_numbers = [x for x in range(1, 9) if x not in set_stop_numbers]
    combinations_numbers = list(combinations(set_of_numbers, 2))
    shuffle(combinations_numbers)
    pop_num = combinations_numbers[0]
    num_1 = Number(pop_num[0])
    sign_multiply = Number('x')
    num_2 = Number(pop_num[1])
    sign_equal = Number('=')
    answer = Number('?')
    sign_multiply.delta(40)
    num_2.delta(80)
    sign_equal.delta(120)
    answer.delta(160)
    task = [num_1, sign_multiply, num_2, sign_equal, answer]
    display_write(screen, task)
    while True:
        h_k = handle_keys()
        if h_k:
            print(h_k)
        if h_k and int(h_k) == -1:
            display_clear(screen)
            pop_num = combinations_numbers.pop()
            num_1.value = pop_num[0]
            num_2.value = pop_num[1]
            answer.value = '?'
            display_write(screen, task)
        if h_k and int(h_k) >= 0:
            if answer.value.isdigit():
                answer.value += h_k
            else:
                answer.value = h_k
            display_write(screen, task)


if __name__ == '__main__':
    main()
