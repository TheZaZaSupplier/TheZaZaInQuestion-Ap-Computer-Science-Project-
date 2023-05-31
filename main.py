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

# Define dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create event for adding a missile
ADDMISSILE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDMISSILE, 400)  # Adjust the interval as needed

# Load images
fighter_jet_image = pygame.image.load("pngtree-super-fighter-mig-29-png-image_4500660-removebg-preview.png").convert_alpha()
missile_image = pygame.image.load("missile-removebg-preview.png").convert_alpha()
bullet_bill_image = pygame.image.load("BulletClipArt.png").convert_alpha()
gun_turret_image = pygame.image.load("MinigunTurret.png").convert_alpha()
explosion_image = pygame.image.load("Explosion.png").convert_alpha()

# Define Player by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(fighter_jet_image, (100, 80))
        self.turret_image = pygame.transform.scale(gun_turret_image, (30, 30))
        self.rect = self.image.get_rect()
        self.turret_offset_x = -30  # X offset of the gun turret from the player's rect
        self.turret_offset_y = 0  # Y offset of the gun turret from the player's rect
        self.shoot_delay = 500  # Delay between shots in milliseconds
        self.last_shot = pygame.time.get_ticks()  # Time of the last shot in milliseconds
        self.lives = 3  # Number of lives
        self.immunity_duration = 3000  # Duration of immunity in milliseconds
        self.immunity_end_time = 0  # Time when the immunity ends

    def update(self, pressed_keys):
        if not game_paused:
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
        # Check if enough time has passed since last shot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            bullet = Bullet(
                self.rect.right + self.turret_offset_x,
                self.rect.centery + self.turret_offset_y,
                size=(50, 30)
            )
            bullets.add(bullet)
            all_sprites.add(bullet)
            self.last_shot = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        turret_position = (
            self.rect.right + self.turret_offset_x,
            self.rect.top + self.turret_offset_y
        )
        screen.blit(self.turret_image, turret_position)

# Define Bullet object by extending pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(50, 20)):
        super(Bullet, self).__init__()
        self.image = pygame.transform.scale(bullet_bill_image, size)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 30

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define Missile object by extending pygame.sprite.Sprite
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
        self.speed = random.randint(10, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define Explosion object by extending pygame.sprite.Sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Explosion, self).__init__()
        self.image = pygame.transform.scale(explosion_image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = 1000  # Duration of the explosion in milliseconds
        self.creation_time = pygame.time.get_ticks()  # Time of creation in milliseconds

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.duration:
            self.kill()

# Create player instance
player = Player()

# Create sprite groups
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Game clock
clock = pygame.time.Clock()

# Game over variables
game_over = False
game_paused = False
play_again = False

# Game over screen
game_over_text = pygame.font.Font(None, 36)
play_again_text = pygame.font.Font(None, 24)
game_over_message = game_over_text.render("Game Over", True, (255, 0, 0))
play_again_message = play_again_text.render("Press 'R' to play again or 'Q' to quit", True, (255, 0, 0))
game_over_rect = game_over_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
play_again_rect = play_again_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Variable to control the game loop
running = True
respawn_delay = 2000  # 2 seconds
respawn_time = 0
# Score counter for missiles shot down
score = 0

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False    
            elif event.key == pygame.K_r and game_over:
                if not play_again:
                    play_again = True
                else:
                    # Reset game
                    player.lives = 3
                    game_over = False
                    play_again = False
                    respawn_time = 0
                    score = 0
                    missiles.empty()
                    explosions.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    game_paused = False
            elif event.key == pygame.K_q and game_over:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDMISSILE:
            new_missile = Missile()
            missiles.add(new_missile)
            all_sprites.add(new_missile)

    if player not in all_sprites and not game_over:
        if pygame.time.get_ticks() >= respawn_time:
            player = Player()
            all_sprites.add(player)

    if not game_paused:
        # Take input again
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        bullets.update()

        for bullet in bullets:
            missiles_hit = pygame.sprite.spritecollide(bullet, missiles, True)
            if missiles_hit:
                bullet.kill()
                score += 1
        if not player.immunity_end_time and pygame.sprite.spritecollide(player, missiles, True):
            explosions.add(Explosion(player.rect.centerx, player.rect.centery))
            player.lives -= 1
            if player.lives <= 0:
                game_over = True
                game_paused = True
            else:
                player.immunity_end_time = pygame.time.get_ticks() + player.immunity_duration

        if player.immunity_end_time and pygame.time.get_ticks() >= player.immunity_end_time:
            player.immunity_end_time = 0

        missiles.update()

        explosions.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    for explosion in explosions:
        screen.blit(explosion.image, explosion.rect)

    # Draw life counter and scour counter
    life_counter_font = pygame.font.Font(None, 24)
    life_counter_text = life_counter_font.render("Lives: " + str(player.lives), True, (0, 0, 0))
    screen.blit(life_counter_text, (10, 10))
    score_font = pygame.font.Font(None, 24)
    score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 40))
    
    if game_over:
        screen.blit(game_over_message, game_over_rect)
        screen.blit(play_again_message, play_again_rect)
        game_paused = True

    pygame.display.flip()
    clock.tick(60)  # Frame rate

pygame.quit()

