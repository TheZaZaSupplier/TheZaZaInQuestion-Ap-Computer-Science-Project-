import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create a custom event for adding a new cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Load images
fighter_jet_image = pygame.image.load("fighterjet.jpg").convert_alpha()
missile_image = pygame.Surface((10, 20))
missile_image.fill((255, 0, 0))

# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(fighter_jet_image, (80, 60))
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
"""
# Define the Enemy object by extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
"""
# Define the Cloud object by extending pygame.sprite.Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Define the Missile object by extending pygame.sprite.Sprite
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
  def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
# Check for collisions between enemies and the player
ADDMISSILE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDMISSILE, 1000)  # Adjust the interval as needed

if pygame.sprite.spritecollide(player, missiles, True):
        running = False  

# Check for collisions between missiles and enemies
missiles = pygame.sprite.Group()

# Create player instance
player = Player()

# Create sprite groups
clouds = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set up the game clock
clock = pygame.time.Clock()

# Variable to control the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            missiles.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Create missiles on SPACE key press
    if pressed_keys[pygame.K_SPACE]:
        new_missile = Missile(player.rect.centerx, player.rect.centery)
        missiles.add(new_missile)
        all_sprites.add(new_missile)
for event in pygame.event.get():
    if event.type == ADDMISSILE:
        new_missile = Missile()
        missiles.add(new_missile)
        all_sprites.add(new_missile)
    clouds.update()
    missiles.update()
    # Check for collisions between missiles and enemies
    for missile in missiles:
        missiles_hit = pygame.sprite.spritecollide(missile, True)
        if missiles_hit:
            missile.kill()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.flip()
    clock.tick(30)  # Control the frame rate

pygame.quit()
