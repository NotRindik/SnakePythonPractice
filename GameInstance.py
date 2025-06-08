import os
import time
import threading
import keyboard

from GameObjects import Snake , Food
from Difficulty import Difficults

class GameInstance:
    def __init__(self):
        self.FIELD_SIZE = 20
        self.SNAKE_CHAR = 'O'
        self.FOOD_CHAR = '*'
        self.EMPTY_CHAR = ' '
        self.WALL_CHAR = '#'
        self.score = 0
        self.highscore = 0
        self.difficulty = Difficults.choose_difficulty(self)

        self.snake = Snake(start_pos=(self.FIELD_SIZE // 2, self.FIELD_SIZE // 2))
        self.food = Food(self.FIELD_SIZE, self.snake.body)

        self.input_thread = threading.Thread(target=self.listen_input, daemon=True)
        self.input_thread.start()

    def listen_input(self):
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name in ['w', 'a', 's', 'd']:
                    self.snake.next_direction = event.name

    def update(self):
        grow = self.snake.get_head() == self.food.position
        self.snake.move(grow=grow)

        if grow:
            self.score += 1
            self.highscore = max(self.highscore, self.score)
            self.food = Food(self.FIELD_SIZE, self.snake.body)

        if self.snake.check_collision(self.FIELD_SIZE):
            self.snake.alive = False

            self.draw()

    def draw(self):
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

        output = f"\x1b[HСчёт: {self.score}  Рекорд: {self.highscore}\n"
        output += '\n'.join(''.join(row) for row in field)
        print(output)

    def start(self):
        while self.snake.alive:
            self.update()
            time.sleep(self.difficulty)

        print("Игра окончена! Нажмите Enter для выхода.")
        input()

