from random import choice, randrange
import pygame

pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения змейки:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (28, 30, 33)
BORDER_COLOR = (245, 250, 255)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 11

# Настройка игрового окна и его заголовка:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=(0, 0, 0),
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """Абстрактный метод отрисовки на экране для переопределения
        в дочерних классах.
        """
        pass

    def draw_rect(self, surface, color, rect, width=0):
        """Метод для отрисовки прямоугольников."""
        pygame.draw.rect(surface, color, rect, width)


class Apple(GameObject):
    """Наследуемый от базового класс объекта Яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод для установки случайного положения яблока
        на игровом поле
        """
        self.position = (randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE))

    def draw(self, surface):
        """Переопределенный метод отрисовки яблока на экране."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        self.draw_rect(surface, self.body_color, rect)
        self.draw_rect(surface, BORDER_COLOR, rect, 3)


class Snake(GameObject):
    """Наследуемый от базового класс объекта Змейка."""

    def __init__(self, length=1, next_direction=None, direction=RIGHT,
                 body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = length
        self.positions = [self.position]
        self.direction = direction
        self.next_direction = next_direction
        self.last = None

    def update_direction(self):
        """Метод для обновления направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления положения змейки,
        проверки столкновения с собой.
        """
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head_position in self.positions[2:-1]:
            self.reset()
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self, surface):
        """Переопределенный метод для отрисовки змейки на экране."""
        # Отрисовка всей змейки
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            self.draw_rect(surface, self.body_color, rect)
            self.draw_rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка только головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        self.draw_rect(surface, self.body_color, head_rect)
        self.draw_rect(surface, BORDER_COLOR, head_rect, 5)

        # Затирание последнего сегмента змейки
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            self.draw_rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для возвращения положения головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод для сброса длины, позиции змейки и случайного выбора
        направления ее движения.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки нажатия клавиш для смены движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            dict_direction = {
                pygame.K_UP: DOWN,
                pygame.K_DOWN: UP,
                pygame.K_LEFT: RIGHT,
                pygame.K_RIGHT: LEFT
            }
            dict_next_direction = {
                pygame.K_UP: UP,
                pygame.K_DOWN: DOWN,
                pygame.K_LEFT: LEFT,
                pygame.K_RIGHT: RIGHT
            }
            if game_object.direction != dict_direction[event.key]:
                game_object.next_direction = dict_next_direction[event.key]


def main():
    """Функция с основным игровым циклом."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        if apple.position in snake.positions:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
