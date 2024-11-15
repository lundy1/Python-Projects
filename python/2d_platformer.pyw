import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

player_size = (50, 50)
player_color = BLUE
player_speed = 5
player_jump_speed = -15
gravity = 0.5

platform_color = GREEN
platform_size = (100, 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(player_size)
        self.image.fill(player_color)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - player_size[1] - 10
        self.speed_y = 0
        self.on_ground = False

    def update(self):
        self.speed_y += gravity
        self.rect.y += self.speed_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.speed_y > 0:
                self.rect.bottom = platform.rect.top
                self.speed_y = 0
                self.on_ground = True

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.speed_y = player_jump_speed
            self.on_ground = False

    def move(self, direction):
        self.rect.x += direction * player_speed

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    global platforms
    platforms = pygame.sprite.Group()

    platforms.add(Platform(200, 500, 100, 20))
    platforms.add(Platform(400, 400, 100, 20))
    platforms.add(Platform(600, 300, 100, 20))
    all_sprites.add(platforms)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()                   

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)

        all_sprites.update()

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
