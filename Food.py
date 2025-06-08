import random

class Food:
    def __init__(self, field_size, snake_body):
        self.position = self.spawn(field_size, snake_body)

    def spawn(self, field_size, snake_body):
        while True:
            x = random.randint(1, field_size - 2)
            y = random.randint(1, field_size - 2)
            if (x, y) not in snake_body:
                return (x, y)
