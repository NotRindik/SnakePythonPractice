import os
import time
import threading
import msvcrt

from Snake import Snake
from Food import Food
from Difficulty import Difficults

class GameInstance:
    def __init__(self):
        self.FIELD_SIZE = 20
        self.SNAKE_CHAR = 'O'
        self.FOOD_CHAR = '*'
        self.EMPTY_CHAR = ' '
        self.WALL_CHAR = '#'
        self.score = 0
        self.HIGH_SCORE_FILE = 'highscore.txt'
        self.highscore = self.load_highscore()
        self.difficulty = Difficults.choose_difficulty(self)
        self.snake = Snake(start_pos=(self.FIELD_SIZE // 2, self.FIELD_SIZE // 2))
        self.food = Food(self.FIELD_SIZE, self.snake.body)

        self.direction_lock = threading.Lock()
        self.input_thread = threading.Thread(target=self.listen_input, daemon=True)
        self.input_thread.start()

    def listen_input(self):
        while True:
            while msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key in ['w', 'a', 's', 'd']:
                    with self.direction_lock:
                        self.snake.next_direction = key

    def update(self):
        grow = self.snake.get_head() == self.food.position
        self.snake.move(grow=grow)

        if grow:
            self.score += 1
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
            self.food = Food(self.FIELD_SIZE, self.snake.body)

        if self.snake.check_collision(self.FIELD_SIZE):
            self.snake.alive = False
    def load_highscore(self):
        try:
            with open(self.HIGH_SCORE_FILE, 'r') as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open(self.HIGH_SCORE_FILE, 'w') as f:
            f.write(str(self.highscore))
    def draw(self):
        print('\033[H', end='')
        field = [[self.EMPTY_CHAR for _ in range(self.FIELD_SIZE)] for _ in range(self.FIELD_SIZE)]

        for i in range(self.FIELD_SIZE):
            field[0][i] = self.WALL_CHAR
            field[self.FIELD_SIZE - 1][i] = self.WALL_CHAR
            field[i][0] = self.WALL_CHAR
            field[i][self.FIELD_SIZE - 1] = self.WALL_CHAR

        fx, fy = self.food.position
        field[fy][fx] = self.FOOD_CHAR

        for i, (x, y) in enumerate(self.snake.body):
            field[y][x] = self.SNAKE_CHAR if i == 0 else 'o'

        lines = []
        lines.append(f"СЧЁТ: {self.score}    РЕКОРД: {self.highscore}")
        lines.append('-' * self.FIELD_SIZE)
        lines.extend(''.join(row) for row in field)
        lines.append('-' * self.FIELD_SIZE)
        print('\n'.join(lines))

    def flush_input(self):
        while msvcrt.kbhit():
            msvcrt.getch()

    def start(self):
        os.system('cls')
        while True:
            while self.snake.alive:
                self.update()
                self.draw()
                time.sleep(self.difficulty)
            os.system('cls')
            print("Game Over \n1 — Начать заново\n2 — Выйти")
            self.flush_input()
            inp = input()
            if inp == "2":
                break
            elif inp == "1":
                self.__init__()
