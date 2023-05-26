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

# Create a custom event for adding a new missile
ADDMISSILE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDMISSILE, 750)  # Adjust the interval as needed

# Load images
fighter_jet_image = pygame.image.load("pngtree-super-fighter-mig-29-png-image_4500660-removebg-preview.png").convert_alpha()
missile_image = pygame.image.load("missile-removebg-preview.png").convert_alpha()
gun_image = pygame.Surface((5, 10))
gun_image.fill((255, 0, 0))

# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(fighter_jet_image, (100, 80))
        self.rect = self.image.get_rect()
        self.gun_offset_x = 60  # X offset of the gun from the player's rect
        self.gun_offset_y = 25  # Y offset of the gun from the player's rect

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
        if pressed_keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.right + self.gun_offset_x, self.rect.centery + self.gun_offset_y)
        bullets.add(bullet)
        all_sprites.add(bullet)

# Define the Bullet object by extending pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = gun_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define the Missile object by extending pygame.sprite.Sprite
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()
        self.image = pygame.transform.scale(missile_image, (50, 20))
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

# Create player instance
player = Player()

# Create sprite groups
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()

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
        elif event.type == ADDMISSILE:
            new_missile = Missile()
            missiles.add(new_missile)
            all_sprites.add(new_missile)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    bullets.update()

    for bullet in bullets:
        missiles_hit = pygame.sprite.spritecollide(bullet, missiles, True)
        if missiles_hit:
            bullet.kill()

    # Check for collisions between missiles and player
    if pygame.sprite.spritecollide(player, missiles, True):
        running = False

    missiles.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.flip()
    clock.tick(30)  # Control the frame rate

pygame.quit()
