import pygame
import os
import random
import sys
import neat
import pickle

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEAT Car Racer 🚗")

# Load and scale images
PLAYER_CAR = pygame.image.load(os.path.join("assets", "player_car.png")).convert_alpha()
ENEMY_CAR = pygame.image.load(os.path.join("assets", "enemy_car.png")).convert_alpha()
TRACK_BG = pygame.image.load(os.path.join("assets", "track_bg.png")).convert()

PLAYER_CAR = pygame.transform.rotate(PLAYER_CAR, 90)
ENEMY_CAR = pygame.transform.rotate(ENEMY_CAR, 90)

PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (50, 100))
ENEMY_CAR = pygame.transform.scale(ENEMY_CAR, (50, 100))
TRACK_BG = pygame.transform.scale(TRACK_BG, (WIDTH, HEIGHT))

FPS = 500
LANES = [75, 175, 275, 375]  # 4-lane centers
GENERATION = 0

# Toggle between 'train' and 'test'
RUN_MODE = 'train'

class Player:
    def __init__(self):
        self.image = PLAYER_CAR
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = HEIGHT - 120
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.alive = True
        self.score = 0

    def move(self, decision):
        if decision == 0 and self.lane > 0:
            self.lane -= 1
        elif decision == 2 and self.lane < len(LANES) - 1:
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
        self.lane = random.randint(0, len(LANES) - 1)
        self.x = LANES[self.lane]
        self.y = -self.image.get_height()
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.centery = self.y

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

def get_inputs(player, enemies, speed):
    max_distance = HEIGHT
    front = left = right = max_distance
    for enemy in enemies:
        if enemy.y > player.y:
            continue
        dy = player.y - enemy.y
        if enemy.lane == player.lane:
            front = min(front, dy)
        elif enemy.lane == player.lane - 1:
            left = min(left, dy)
        elif enemy.lane == player.lane + 1:
            right = min(right, dy)
    return [
        player.lane / 3,
        front / HEIGHT,
        left / HEIGHT,
        right / HEIGHT,
        speed / 20.0
    ]

def eval_genomes(genomes, config):
    global GENERATION
    GENERATION += 1
    nets, players, ge = [], [], []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player())
        ge.append(genome)

    enemies = []
    enemy_timer = 0
    bg_y = 0
    speed = 5
    clock = pygame.time.Clock()
    run = True

    while run and len(players) > 0:
        clock.tick(FPS)
        bg_y += speed
        if bg_y >= HEIGHT:
            bg_y = 0

        enemy_timer += 1
        if enemy_timer > 60:
            enemies.append(Enemy(speed))
            enemy_timer = 0

        for i, player in enumerate(players):
            inputs = get_inputs(player, enemies, speed)
            output = nets[i].activate(inputs)
            decision = output.index(max(output))
            player.move(decision)
            ge[i].fitness += 0.1

        for enemy in enemies:
            enemy.move()

        for i in range(len(players) - 1, -1, -1):
            player = players[i]
            for enemy in enemies:
                if enemy.rect.colliderect(player.rect):
                    ge[i].fitness -= 1
                    players.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    break

        for enemy in enemies[:]:
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                speed += 0.05
                for g in ge:
                    g.fitness += 1

        WIN.blit(TRACK_BG, (0, bg_y))
        WIN.blit(TRACK_BG, (0, bg_y - HEIGHT))
        for enemy in enemies:
            enemy.draw(WIN)
        for player in players:
            player.draw(WIN)

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Gen: {GENERATION}  Alive: {len(players)}", True, (255, 255, 255))
        WIN.blit(text, (10, 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def run_neat(config_path):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(eval_genomes, 50)

    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("\n✅ Best model saved as 'best_genome.pkl'")

def test_best_model(config_path):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    with open("best_genome.pkl", "rb") as f:
        genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    player = Player()
    enemies = []
    bg_y = 0
    speed = 5
    score = 0
    enemy_timer = 0
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        bg_y += speed
        if bg_y >= HEIGHT:
            bg_y = 0

        enemy_timer += 1
        if enemy_timer > 60:
            enemies.append(Enemy(speed))
            enemy_timer = 0

        inputs = get_inputs(player, enemies, speed)
        output = net.activate(inputs)
        decision = output.index(max(output))
        player.move(decision)

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.colliderect(player.rect):
                print(f"\U0001F4A5 AI Crashed! Final Score: {score}")
                run = False
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 1
                speed += 0.05

        WIN.blit(TRACK_BG, (0, bg_y))
        WIN.blit(TRACK_BG, (0, bg_y - HEIGHT))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        WIN.blit(text, (10, 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    if RUN_MODE == 'train':
        run_neat(config_path)
    elif RUN_MODE == 'test':
        test_best_model(config_path)
    else:
        print("❌ Invalid RUN_MODE. Use 'train' or 'test'.")