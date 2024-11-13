import time
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
# Зелёный
GREEN = (0, 128, 0)
# Красный
RED = (255, 0, 0)

NUMBER_KEYBOARD = [1073741922, 1073741913, 1073741914, 1073741915, 1073741916,
                   1073741917, 1073741918, 1073741919, 1073741920, 1073741921]
NUMBER_KEYBOARD_HI = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]


class Number():
    def __init__(self,
                 value=0,
                 coordinate=(SCREEN_WIDTH/3-10, SCREEN_HEIGHT/2-HEIGH_NUM/2),
                 color=TEXT_COLOR):
        self.value = value
        self.coordinate = coordinate
        self.height_number = HEIGH_NUM
        self.color = color
        self.len_num = len(str(value))

    def delta(self, x=0, y=0):
        self.coordinate = (self.coordinate[0]+x, self.coordinate[1]+y)

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

    set_stop_numbers = [2]
    set_of_numbers = [x for x in range(2, 10) if x not in set_stop_numbers]*2
    print(set_of_numbers)
    combinations_numbers = list(combinations(set_of_numbers, 2))
    shuffle(combinations_numbers)
    pop_num = combinations_numbers.pop(0)
    num_1 = Number(pop_num[0])
    sign_multiply = Number('x')
    num_2 = Number(pop_num[1])
    sign_equal = Number('=')
    answer = Number('?')
    count_question = Number(f'Осталось примеров: {len(combinations_numbers)}',
                            (SCREEN_WIDTH - 260, 10))
    count_question.height_number = 30
    sign_multiply.delta(40)
    num_2.delta(80)
    sign_equal.delta(120)
    answer.delta(160)
    check_text = Number('Правильно', color=(255, 0, 0))
    check_text.delta(-40, - check_text.height_number - 10)
    check_text_answer = Number('')
    task = [num_1, sign_multiply, num_2, sign_equal, answer, count_question]
    display_write(screen, task)
    start_time = time.time()
    while True:
        h_k = handle_keys()
        if h_k and int(h_k) == -1:
            print(combinations_numbers)
            if int(num_1.value) * int(num_2.value) == int(answer.value):
                check_text.value = 'Правильно!'
                check_text.color = GREEN
                time_delay = 1000
                print(time.time() - start_time)
                if time.time() - start_time > TIME_LIMIT_ANSWER:
                    combinations_numbers.append(pop_num)
                    print('append')
            else:
                check_text.value = 'НЕ Правильно!'
                check_text.color = RED
                combinations_numbers.append(pop_num)
                print('append')
                time_delay = 2000
            check_text_answer.value += f'{num_1.value} x {num_2.value} = '
            check_text_answer.value += str(int(num_1.value) * int(num_2.value))    
            display_write(screen, [check_text, check_text_answer])
            pygame.time.delay(time_delay)
            display_clear(screen)
            check_text_answer.value = ''
            count_question.value = 'Осталось примеров: '
            count_question.value += str(len(combinations_numbers))
            pop_num = combinations_numbers.pop(0)
            num_1.value = pop_num[0]
            num_2.value = pop_num[1]
            answer.value = '?'
            display_write(screen, task)
            start_time = time.time()
        if h_k and int(h_k) >= 0:
            if answer.value.isdigit():
                answer.value += h_k
            else:
                answer.value = h_k
            display_write(screen, task)


if __name__ == '__main__':
    main()
