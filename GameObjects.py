import random

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
