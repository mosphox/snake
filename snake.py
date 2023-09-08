import pygame, sys, random
pygame.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid
        self.color = (0, 0, 0)

        self.surf = pygame.Surface((18, 18))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(topleft = (self.tid[0] * 20 + 1, self.tid[1] * 20 + 1))

    def set_color(self, color):
        self.color = color
        self.surf.fill(color)

class Snake():
    movement = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}

    def __init__(self, facing, pos):
        self.facing = facing
        self.queue = []
        self.pos = pos

    def move(self, apple):
        if self.queue != []:
            self.facing = self.queue.pop(0)

        head = (self.pos[0][0] + self.movement[self.facing][0], self.pos[0][1] + self.movement[self.facing][1])

        if head in self.pos:
            sys.exit()

        if head[0] < 0 or head[0] > 29 or head[1] < 0 or head[1] > 29:
            sys.exit()

        if head == apple.pos:
            self.pos = [head] + self.pos
            return True

        else:
            self.pos.remove(self.pos[::-1][0])
            self.pos = [head] + self.pos
            return False

class Apple():
    cells = [(x, y) for y in range(30) for x in range(30)]

    def __init__(self, pos):
        self.pos = pos

    def spawn(self, snake):
        allowed = [cell for cell in self.cells if cell not in snake.pos]
        self.pos = random.choice(allowed)

class Engine():
    def __init__(self):
        self.snake = Snake("w", [(15, 15), (16, 15), (17, 15)])
        self.apple = Apple((5, 5))

        self.tiles = [Tile((x, y)) for y in range(30) for x in range(30)]

    def facing(self, direction):
        if self.snake.queue != []:
            current_dir = self.snake.queue[::-1][0]
        else:
            current_dir = self.snake.facing

        if (current_dir == "n" or current_dir == "s") and (direction == "n" or direction == "s"):
            return None
        if (current_dir == "e" or current_dir == "w") and (direction == "e" or direction == "w"):
            return None

        if len(self.snake.queue) < 2:
            self.snake.queue.append(direction)

    def update(self):
        if self.snake.move(self.apple):
            self.apple.spawn(self.snake)

        for tile in self.tiles:
            if tile.tid in self.snake.pos:
                if tile.tid == self.snake.pos[0]:
                    tile.set_color((0, 255, 0))
                else:
                    tile.set_color((0, 120, 0))

            elif tile.tid == self.apple.pos:
                tile.set_color((255, 0, 0))

            else:
                if tile.color != (0, 0, 0):
                    tile.set_color((0, 0, 0))

    def render(self, screen):
        self.update()

        for tile in self.tiles:
            screen.blit(tile.surf, tile.rect)

width, height = 600, 600
fps = 7

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
engine = Engine()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                engine.facing("n")
            if event.key == pygame.K_s:
                engine.facing("s")
            if event.key == pygame.K_d:
                engine.facing("e")
            if event.key == pygame.K_a:
                engine.facing("w")

            if event.key == pygame.K_SPACE:
                fps = 15

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fps = 7

    engine.render(screen)
    pygame.display.flip()

    clock.tick(fps)