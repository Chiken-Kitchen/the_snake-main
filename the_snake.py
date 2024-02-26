"""Импорт модулей из библиотеки."""
from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центральная точка экрана:
INITIAL_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Цвет по умолчанию:
BODY_COLOR = (0, 0, 0)


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс."""

    def __init__(self, body_color=BODY_COLOR, position=INITIAL_POSITION):
        """Родительский конструктор принимающий атрибуты позиции и цвета."""
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """Абстрактный метод, реализуется в дочерних классах."""
        raise NotImplementedError('The draw method must be defined!')


class Apple(GameObject):
    """Дочерний класс описывающий игровое яблоко."""

    def __init__(self, body_color=APPLE_COLOR, position=INITIAL_POSITION):
        """Дочерний конструктор принимающий атрибуты позиции и цвета."""
        super().__init__(body_color, position)
        self.body_color = body_color
        self.randomize_position()

    @classmethod
    def randomize_position(cls):
        """Метод устанавливающий яблоко в случайном порядке."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Метод отрисовывающий яблоко на игровом поле."""
        rect = pygame.Rect(
            (self.position),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс определяющий объект: Змейка."""

    def __init__(self, body_color=SNAKE_COLOR, position=INITIAL_POSITION):
        """Дочерний конструктор с атрибутами длинны, цвета, позиции."""
        super().__init__(body_color, position)
        self.reset()

    def get_head_position(self):
        """Метод определяющий позицию головы змейки."""
        return self.positions[0]

    def draw(self, surface):
        """Метод отрисовывающий змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние."""
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.positions = [INITIAL_POSITION]
        self.last = None

    def update_direction(self, new_direction):
        """Метод обновляющий направление движения змейки."""
        if new_direction:
            self.direction = new_direction
            self.new_direction = (UP, DOWN, RIGHT, LEFT)

    def move(self):
        """Метод обновляющий положение змейки."""
        head = self.get_head_position()
        directions = {
            RIGHT: (head[0] + GRID_SIZE, head[1]),
            LEFT: (head[0] - GRID_SIZE, head[1]),
            UP: (head[0], head[1] - GRID_SIZE),
            DOWN: (head[0], head[1] + GRID_SIZE)
        }
        new_head = directions[self.direction]

        x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()


def handle_keys(game_object):
    """Функция недопускающая движение в обратном направлении."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Функция определяющая и описывающая логику игры."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    # Тут опишите основную логику игры.
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        apple.draw(screen)
        snake.draw(screen)

        if snake.get_head_position() == apple.position:
            snake.length += 1
        """Увеличение змейки."""
        while apple.position in snake.positions:
            """Проверка не находится ли яблоко в змейке."""
            apple.position = apple.randomize_position()
        pygame.display.update()
        """Сброс змейки."""
        if snake.get_head_position() in snake.positions[-1]:
            snake.reset()


if __name__ == '__main__':
    main()
"""Условный оператор запускающий код напрямую."""
