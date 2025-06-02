import os
import random
import time
import threading
import keyboard


class Snake:
    def __init__(self, start_pos):
        self.body = [start_pos]
        self.direction = 'd'
        self.next_direction = 'd'
        self.alive = True

    def get_head(self):
        return self.body[0]

    def move(self, grow=False):
        x, y = self.get_head()

        opposites = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
        if self.next_direction != opposites.get(self.direction):
            self.direction = self.next_direction

        if self.direction == 'w': y -= 1
        elif self.direction == 's': y += 1
        elif self.direction == 'a': x -= 1
        elif self.direction == 'd': x += 1

        new_head = (x, y)

        if not grow:
            self.body.pop()
        self.body.insert(0, new_head)

    def check_collision(self, field_size):
        head = self.get_head()
        if not (1 <= head[0] < field_size - 1 and 1 <= head[1] < field_size - 1):
            return True
        if head in self.body[1:]:
            return True
        return False


class Food:
    def __init__(self, field_size, snake_body):
        self.position = self.spawn(field_size, snake_body)

    def spawn(self, field_size, snake_body):
        while True:
            x = random.randint(1, field_size - 2)
            y = random.randint(1, field_size - 2)
            if (x, y) not in snake_body:
                return (x, y)


class GameInstance:
    def __init__(self):
        self.FIELD_SIZE = 20
        self.SNAKE_CHAR = 'O'
        self.FOOD_CHAR = '*'
        self.EMPTY_CHAR = ' '
        self.WALL_CHAR = '#'
        self.score = 0
        self.highscore = 0
        self.difficulty = self.choose_difficulty()

        self.snake = Snake(start_pos=(self.FIELD_SIZE // 2, self.FIELD_SIZE // 2))
        self.food = Food(self.FIELD_SIZE, self.snake.body)

        # запускаем поток ввода
        self.input_thread = threading.Thread(target=self.listen_input, daemon=True)
        self.input_thread.start()

    def choose_difficulty(self):
        print("Выберите сложность:")
        print("1 - Лёгкая")
        print("2 - Средняя")
        print("3 - Сложная")
        choice = input("Ваш выбор: ")
        if choice == '1':
            return 0.2
        elif choice == '2':
            return 0.1
        else:
            return 0.05

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

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
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

        print(f"Счёт: {self.score}  Рекорд: {self.highscore}")
        for row in field:
            print(''.join(row))

    def start(self):
        while self.snake.alive:
            self.update()
            self.draw()
            time.sleep(self.difficulty)

        print("Игра окончена! Нажмите Enter для выхода.")
        input()


if __name__ == '__main__':
    game = GameInstance()
    game.start()
