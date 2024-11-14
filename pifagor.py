import time
import pygame
from itertools import combinations
from random import shuffle
from collections import defaultdict

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

    def delta(self, x=0, y=0):
        self.coordinate = (self.coordinate[0]+x, self.coordinate[1]+y)

    def draw(self, screen):
        """Вывод текста на экран."""
        pygame.font.init()
        font = pygame.font.Font(None, self.height_number)
        text = font.render(str(self.value), True, self.color)
        text_rect = text.get_rect(topleft=(self.coordinate))
        screen.blit(text, text_rect)


class Button():
    "Класс кнопок."

    def __init__(self, name, coordinats,
                 flag=False, color=GREEN,
                 width=50, height=50):
        self.name = name
        self.coordinats = coordinats
        self.color = color
        self.flag = [flag for _ in range(2, 10)]
        self.width = width
        self.height = height
        self.incorrect_answer = defaultdict(int)

    def __str__(self) -> str:
        return str(self.name) + ' - ' + ', '.join(str(x) for x in self.flag)

    def draw_point(self, screen):
        for i, point in enumerate(self.flag):
            circle_center = (self.coordinats[0] + self.width // 2,
                             self.coordinats[1] - 10 * i-10)
            circle_radius = 3
            if point is True:
                color = GREEN
            else:
                color = RED
            pygame.draw.circle(screen, color, circle_center, circle_radius, 0)

    def draw(self, screen):
        "Отрисовка кнопки."
        button_rect = pygame.Rect(self.coordinats[0], self.coordinats[1],
                                  self.width, self.height)
        pygame.draw.rect(screen, self.color, button_rect)
        # Определяем шрифт и текст кнопки
        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        self.draw_point(screen)


def handle_keys() -> None:
    """Функция обработки действий пользователя."""
    pressed_digit = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            """ if button_rect.collidepoint(mouse_pos):
                print("Кнопка была нажата!")"""
        elif event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key) )
            if event.key in (NUMBER_KEYBOARD_HI):
                pressed_digit = pygame.key.name(event.key)
            elif event.key in NUMBER_KEYBOARD:
                pressed_digit = pygame.key.name(event.key)[1]
            elif pygame.key.name(event.key) == 'backspace':
                pressed_digit = 'backspace'
            elif (pygame.key.name(event.key) == 'enter' or
                  pygame.key.name(event.key) == 'return'):
                pressed_digit = 'enter'
    return pressed_digit


def display_clear(screen) -> None:
    """Очистка дисплея."""
    rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
    pygame.display.update()


def display_write(screen, arr_num: list):
    "Отрисовка вопроса"
    display_clear(screen)
    for x in arr_num:
        x.draw(screen)


def create_buttons(buttons_list):
    for x in range(2, 10):
        btn = Button(name=str(x), coordinats=(x*60-30, SCREEN_HEIGHT - 80))
        buttons_list.append(btn)


def draw_buttons(buttons_list, screen):
    "Отрисовка кнопок цифр и пройденных заданий"
    for btn in buttons_list:
        btn.draw(screen)
    pygame.display.update()


def save_answer(buttons_list, answer, correct_flag):
    num = answer[0]-2
    if correct_flag:
        buttons_list[num].flag[answer[1]-2] = correct_flag
        print(buttons_list[num])
    else:
        buttons_list[num].incorrect_answer[answer[1]] += 1
        print(f'ошибка {answer[0]} +1', buttons_list[num].incorrect_answer)


def main():
    # Настройка игрового окна:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Пифагоровы штаны')
    buttons_list = []
    create_buttons(buttons_list)
    set_stop_numbers = []
    set_of_numbers = [x for x in range(2, 10) if x not in set_stop_numbers]*2
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
    draw_buttons(buttons_list, screen)
    start_time = time.time()
    while True:
        h_k = handle_keys()
        if h_k == 'enter':
            if int(num_1.value) * int(num_2.value) == int(answer.value):
                check_text.value = 'Правильно!'
                check_text.color = GREEN
                time_delay = 1000
                print(time.time() - start_time)
                if time.time() - start_time > TIME_LIMIT_ANSWER:
                    combinations_numbers.append(pop_num)
                    print('append')
                save_answer(buttons_list, (num_1.value, num_2.value), True)
            else:
                check_text.value = 'НЕ Правильно!'
                check_text.color = RED
                combinations_numbers.append(pop_num)
                print('append')
                save_answer(buttons_list, (num_1.value, num_2.value), False)
                time_delay = 2000
            # Вывод ответа.
            check_text_answer.value += f'{num_1.value} x {num_2.value} = '
            check_text_answer.value += str(int(num_1.value) * int(num_2.value))
            display_write(screen, [check_text, check_text_answer])
            draw_buttons(buttons_list, screen)
            pygame.display.update()
            pygame.time.delay(time_delay)
            display_clear(screen)
            # Новый вопрос.
            check_text_answer.value = ''
            count_question.value = 'Осталось примеров: '
            count_question.value += str(len(combinations_numbers))
            pop_num = combinations_numbers.pop(0)
            num_1.value = pop_num[0]
            num_2.value = pop_num[1]
            answer.value = '?'
            display_write(screen, task)
            draw_buttons(buttons_list, screen)
            start_time = time.time()
        if h_k and h_k.isdigit() and int(h_k) >= 0:
            if answer.value.isdigit():
                answer.value += h_k
            else:
                answer.value = h_k
            display_write(screen, task)
            draw_buttons(buttons_list, screen)
        if h_k == 'backspace' and len(answer.value) > 0:
            answer.value = answer.value[:-1]
            display_write(screen, task)
            draw_buttons(buttons_list, screen)


if __name__ == '__main__':
    main()
