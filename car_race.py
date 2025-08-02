import pygame
import os
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEAT Car Racer 🚗")

# Load and rotate images
PLAYER_CAR = pygame.image.load(os.path.join("assets", "player_car.png")).convert_alpha()
ENEMY_CAR = pygame.image.load(os.path.join("assets", "enemy_car.png")).convert_alpha()
TRACK_BG = pygame.image.load(os.path.join("assets", "track_bg.png")).convert()

PLAYER_CAR = pygame.transform.rotate(PLAYER_CAR, 90)
ENEMY_CAR = pygame.transform.rotate(ENEMY_CAR, 90)

PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (50, 100))
ENEMY_CAR = pygame.transform.scale(ENEMY_CAR, (50, 100))
TRACK_BG = pygame.transform.scale(TRACK_BG, (WIDTH, HEIGHT))

FPS = 60
# 💡 4-lane positions based on 250px track width resized to 500px
LANES = [75, 175, 275, 375]  # 4-lane centers (even spacing)
  # 4 lanes: roughly centered (adjust if needed)


GENERATION = 0

class Player:
    def __init__(self):
        self.image = PLAYER_CAR
        self.lane = 1  # Start in 2nd lane
        self.x = LANES[self.lane]
        self.y = HEIGHT - 120
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANES[self.lane]
            self.update_rect()

    def move_right(self):
        if self.lane < len(LANES) - 1:
            self.lane += 1
            self.x = LANES[self.lane]
            self.update_rect()

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

class Enemy:
    def __init__(self, speed):
        self.image = ENEMY_CAR
        self.lane = random.randint(0, len(LANES) - 1)  # ✅ Full 4-lane support
        self.x = LANES[self.lane]
        self.y = -self.image.get_height()

        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.centery = self.y

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

def draw_window(win, player, enemies, bg_y, score):
    win.blit(TRACK_BG, (0, bg_y))
    win.blit(TRACK_BG, (0, bg_y - HEIGHT))

    for enemy in enemies:
        enemy.draw(win)
    player.draw(win)

    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.update()

def main():
    global GENERATION
    GENERATION += 1

    clock = pygame.time.Clock()
    run = True
    bg_y = 0
    score = 0
    speed = 5

    player = Player()
    enemies = []
    enemy_timer = 0

    while run:
        clock.tick(FPS)
        bg_y += speed
        if bg_y >= HEIGHT:
            bg_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        # Enemy spawner
        enemy_timer += 1
        if enemy_timer > 60:
            enemies.append(Enemy(speed))
            enemy_timer = 0

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.colliderect(player.rect):
                print(f"💥 Crash! Final Score: {score}")
                run = False
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 1
                speed += 0.1

        draw_window(WIN, player, enemies, bg_y, score)

    pygame.quit()

if __name__ == "__main__":
    main()