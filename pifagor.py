"""Пифагор. Приложени для повторения таблицы умножения."""

import time
import datetime
import pygame
from itertools import product
from random import shuffle
from collections import defaultdict
from bot import send_message

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
# Цвета
GREEN = (0, 128, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
# Коды цифр
TextSting_KEYBOARD = [1073741922, 1073741913, 1073741914, 1073741915,
                      1073741916, 1073741917, 1073741918, 1073741919,
                      1073741920, 1073741921]
TextSting_KEYBOARD_HI = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
# не играемые цифры
set_stop_text_trings: list = []

with open('passwords.txt', 'r') as f:
    TOKEN = f.readline().strip()
    CHAT_ID = f.readline().strip()


class TextSting():
    """Класс вывода текста."""

    def __init__(self,
                 value=0,
                 coordinate=(SCREEN_WIDTH/3-10, SCREEN_HEIGHT/2-HEIGH_NUM/2),
                 color=TEXT_COLOR):
        """Инициация класса."""
        self.value = value
        self.coordinate = coordinate
        self.height_TextSting = HEIGH_NUM
        self.color = color

    def delta(self, x=0, y=0):
        """Смещение координат для текста."""
        self.coordinate = (self.coordinate[0]+x, self.coordinate[1]+y)

    def draw(self, screen):
        """Вывод текста на экран."""
        pygame.font.init()
        font = pygame.font.Font(None, self.height_TextSting)
        text = font.render(str(self.value), True, self.color)
        text_rect = text.get_rect(topleft=(self.coordinate))
        screen.blit(text, text_rect)


class Button():
    """Класс кнопок."""

    def __init__(self, name, coordinats,
                 flag=False, color=GREEN,
                 width=50, height=50):
        """Инициация класса."""
        self.name = name
        self.coordinats = coordinats
        self.color = color
        self.flag = [flag for _ in range(2, 10)]
        self.width = width
        self.height = height
        self.incorrect_answer = defaultdict(int)
        self.rect = pygame.Rect(coordinats[0], coordinats[1], width, height)
        self.block = False

    def __str__(self) -> str:
        """Строковое представление."""
        return str(self.name) + ' - ' + ', '.join(str(x) for x in self.flag)

    @staticmethod
    def write_text(text_input, button_rect, screen) -> None:
        """Отрисовка текста."""
        # Определяем шрифт и текст кнопки
        font = pygame.font.Font(None, 36)
        text = font.render(text_input, True, TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    def draw_point(self, screen) -> None:
        """Отрисовка точек правильных ответов."""
        for i in range(len(self.flag)):
            circle_center = (self.coordinats[0] + self.width // 2,
                             self.coordinats[1] - 10 * i-10)
            circle_radius = 3
            if self.flag[i] is True:
                color = GREEN
            else:
                color = RED
            if self.name in set_stop_text_trings:
                color = GREY
            pygame.draw.circle(screen, color,
                               circle_center, circle_radius, 0)

    def draw(self, screen) -> None:
        """Отрисовка кнопки."""
        global r
        pygame.draw.rect(screen, self.color, self.rect)
        self.write_text(self.name, self.rect, screen)

    @staticmethod
    def report(buttons_list: list, count_comb: int):
        """Отчет по резульатам игры."""
        report_str = ''
        with open('report.txt', 'a', encoding='utf-8') as f:
            report_str = ''
            report_str += '\n\n'
            report_str += '\n**********************************\n'
            report_str += 'Отчет об ошибках: '
            report_str += datetime.datetime.now().date().strftime('%d/%m/%y')
            report_str += ' '
            report_str += datetime.datetime.now().time().strftime('%H:%M:%S')
            report_str += '\nНе используемые цифры: '
            report_str += ', '.join([str(x) for x in set_stop_text_trings])
            report_str += '\n{ число : кол-во ошибок }'
            for but in buttons_list:
                if but.incorrect_answer:
                    report_str += f'\nс {but.name}-й ошибки на '
                    report_str += f'{dict(but.incorrect_answer)}'
            report_str += f'\nОсталось не решённых {count_comb} примеров'
            report_str += '\n**********************************\n'
            f.write(report_str)
            send_message(TOKEN, CHAT_ID, report_str)


def handle_keys(buttons_list: list, count_comb, screen) -> str:
    """Функция обработки действий пользователя."""
    global r
    pressed_digit = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Button.report(buttons_list, count_comb)
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for but in buttons_list:
                if but.block is False and but.rect.collidepoint(mouse_pos):
                    print("Кнопка была нажата!", but.name)
                    if but.name != 'СТАРТ!' and but.color == GREEN:
                        but.color = GREY
                        set_stop_text_trings.append(int(but.name))
                    elif but.name != 'СТАРТ!' and but.color == GREY:
                        but.color = GREEN
                        set_stop_text_trings.remove(int(but.name))
                    if but.name == 'СТАРТ!':
                        print("Кнопка была нажата выхода", but.name)
                        return but.name
                    but.draw(screen)
                    pygame.display.update(but.rect)
                    mouse_pos = (0, 0)
        elif event.type == pygame.KEYDOWN:
            if event.key in (TextSting_KEYBOARD_HI):
                pressed_digit = pygame.key.name(event.key)
            elif event.key in TextSting_KEYBOARD:
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


def display_write(screen, arr_num: list) -> None:
    """Отрисовка вопроса."""
    display_clear(screen)
    for x in arr_num:
        x.draw(screen)


def create_buttons(buttons_list: list) -> None:
    """Cоздание списка кнопок."""
    for x in range(2, 10):
        btn = Button(name=str(x), coordinats=(x*60-30, SCREEN_HEIGHT - 80))
        buttons_list.append(btn)


def draw_buttons(buttons_list: list, screen) -> None:
    """Отрисовка кнопок цифр и пройденных заданий."""
    for btn in buttons_list:
        btn.draw(screen)
        if btn.name not in set_stop_text_trings and btn.name != 'СТАРТ!':
            btn.draw_point(screen)
    pygame.display.update()


def save_answer(buttons_list, answer, correct_flag: bool) -> None:
    """Сохранение ответа в свойства."""
    num = answer[0]-2
    if correct_flag:
        buttons_list[num].flag[answer[1]-2] = correct_flag
        print(buttons_list[num])
    else:
        buttons_list[num].incorrect_answer[answer[1]] += 1
        print(f'ошибка {answer[0]} +1', buttons_list[num].incorrect_answer)


def start_menu(buttons_list, screen):
    """Стартовое меню."""
    text = TextSting('Выбери цифры', (SCREEN_WIDTH//6, SCREEN_HEIGHT//4 - 50))
    text.draw(screen)
    btn = Button('СТАРТ!',
                 (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25),
                 False, RED,
                 100, 50)
    buttons_list.append(btn)
    draw_buttons(buttons_list, screen)
    pygame.display.update()
    while True:
        if handle_keys(buttons_list, [], screen) == 'СТАРТ!':
            print('buttons_list', [x.name for x in buttons_list])
            buttons_list.pop(-1)
            print('buttons_list 2', [x.name for x in buttons_list])
            for btn in buttons_list:
                btn.block = True
            display_clear(screen)
            return


def finish(screen):
    """Финишная заставка."""
    text1 = TextSting(
        'Молодец!', (SCREEN_WIDTH//4 + 15, SCREEN_HEIGHT//2 - 50))
    text2 = TextSting('Игра закончена.', (SCREEN_WIDTH//6, SCREEN_HEIGHT//2))
    text1.draw(screen)
    text2.draw(screen)
    pygame.display.update()
    pygame.time.delay(3000)
    global buttons_list
    Button.report(buttons_list, 0)
    pygame.quit()
    raise SystemExit


def main():
    """Главный цикл."""
    # Настройка игрового окна:
    global r
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Пифагоровы штаны')
    buttons_list = []
    create_buttons(buttons_list)
    start_menu(buttons_list, screen)
    set_of_text_stings = [x for x in range(2, 10)
                          if x not in set_stop_text_trings]
    print('set_of_text_stings', set_of_text_stings)
    combinations_text_strings = list(product(set_of_text_stings, range(2, 10)))
    print(combinations_text_strings)
    shuffle(combinations_text_strings)
    pop_num = combinations_text_strings.pop(0)
    num_1 = TextSting(pop_num[0])
    sign_multiply = TextSting('x')
    num_2 = TextSting(pop_num[1])
    sign_equal = TextSting('=')
    answer = TextSting('?')
    count_comb = len(combinations_text_strings)
    count_question = TextSting(f'Осталось примеров: {count_comb}',
                               (SCREEN_WIDTH - 260, 10))
    count_question.height_TextSting = 30
    sign_multiply.delta(40)
    num_2.delta(80)
    sign_equal.delta(120)
    answer.delta(160)
    check_text = TextSting('Правильно', color=(255, 0, 0))
    check_text.delta(-40, - check_text.height_TextSting - 10)
    check_text_answer = TextSting('')
    task = [num_1, sign_multiply, num_2, sign_equal, answer, count_question]
    display_write(screen, task)
    draw_buttons(buttons_list, screen)
    start_time = time.time()
    while True:
        h_k = handle_keys(buttons_list, count_comb, screen)
        if h_k == 'enter' and answer.value.isdigit():
            if int(num_1.value) * int(num_2.value) == int(answer.value):
                check_text.value = 'Правильно!'
                check_text.color = GREEN
                time_delay = 1000
                print(time.time() - start_time)
                if time.time() - start_time > TIME_LIMIT_ANSWER:
                    combinations_text_strings.append(pop_num)
                    print('append')
                save_answer(buttons_list, (num_1.value, num_2.value), True)
            else:
                check_text.value = 'НЕ Правильно!'
                check_text.color = RED
                combinations_text_strings.append(pop_num)
                print('append')
                save_answer(buttons_list, (num_1.value, num_2.value), False)
                time_delay = 2500
            # Вывод ответа.
            check_text_answer.value += f'{num_1.value} x {num_2.value} = '
            check_text_answer.value += str(int(num_1.value) * int(num_2.value))
            display_write(screen, [check_text, check_text_answer])
            draw_buttons(buttons_list, screen)
            pygame.display.update()
            pygame.time.delay(time_delay)
            display_clear(screen)
            # Новый вопрос.
            if len(combinations_text_strings) == 0:
                finish(screen)
            check_text_answer.value = ''
            count_question.value = 'Осталось примеров: '
            count_question.value += str(len(combinations_text_strings))
            if check_text.value == 'Правильно!':
                pop_num = combinations_text_strings.pop(0)
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
