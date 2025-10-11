# dino_runner.py
import pygame
import random
import sys

# --------- Config ----------
WIDTH, HEIGHT = 800, 300
FPS = 60

GROUND_Y = HEIGHT - 40
DINO_X = 80

GRAVITY = 0.8
JUMP_VELOCITY = -13

OBSTACLE_MIN_GAP = 500  # ms
OBSTACLE_MAX_GAP = 1400  # ms

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
GREEN = (83, 199, 120)
SKY = (235, 245, 255)

# --------- Initialization ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 36)

# --------- Game objects ----------
class Dino:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = DINO_X
        self.y = GROUND_Y - self.height
        self.vy = 0
        self.on_ground = True
        self.ducking = False
        # simple animation frames: standing/leg-up
        self.frame = 0
        self.frame_timer = 0

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y - (self.height if not self.ducking else self.height//2):
            self.y = GROUND_Y - (self.height if not self.ducking else self.height//2)
            self.vy = 0
            self.on_ground = True

        # simple leg animation while running
        if self.on_ground:
            self.frame_timer += 1
            if self.frame_timer > 6:
                self.frame = (self.frame + 1) % 2
                self.frame_timer = 0
        else:
            self.frame = 0

    def duck(self, state):
        if state and self.on_ground:
            self.ducking = True
        else:
            self.ducking = False

    def get_rect(self):
        if self.ducking:
            return pygame.Rect(self.x, self.y + self.height//2, self.width, self.height//2)
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surf):
        r = self.get_rect()
        # body
        pygame.draw.rect(surf, BLACK, r)
        # eye
        pygame.draw.rect(surf, WHITE, (r.x + r.w - 12, r.y + 8, 6, 6))
        # legs (simple animation)
        if self.on_ground and not self.ducking:
            if self.frame == 0:
                pygame.draw.line(surf, BLACK, (r.x+10, r.y+r.h), (r.x+10, r.y+r.h+8), 4)
                pygame.draw.line(surf, BLACK, (r.x+25, r.y+r.h), (r.x+25, r.y+r.h+4), 4)
            else:
                pygame.draw.line(surf, BLACK, (r.x+10, r.y+r.h), (r.x+10, r.y+r.h+4), 4)
                pygame.draw.line(surf, BLACK, (r.x+25, r.y+r.h), (r.x+25, r.y+r.h+8), 4)
        if self.ducking:
            # small tail when ducking
            pygame.draw.line(surf, BLACK, (r.x-6, r.y+r.h//2), (r.x, r.y+r.h//2), 4)


class Obstacle:
    def __init__(self, x, kind="cactus", speed=6):
        self.x = x
        self.kind = kind
        self.speed = speed
        if kind == "cactus":
            self.width = random.choice([18, 22, 26])
            self.height = random.choice([30, 36, 40])
            self.y = GROUND_Y - self.height
        elif kind == "ptera":
            self.width = 40
            self.height = 30
            self.y = GROUND_Y - self.height - random.choice([60, 80])
        else:
            self.width = 20
            self.height = 20
            self.y = GROUND_Y - self.height

        # flapping for ptera
        self.frame = 0
        self.frame_timer = 0

    def update(self, dt, speed_increase=0):
        self.x -= (self.speed + speed_increase) * (dt / (1000 / FPS))
        if self.kind == "ptera":
            self.frame_timer += 1
            if self.frame_timer > 8:
                self.frame = (self.frame + 1) % 2
                self.frame_timer = 0

    def off_screen(self):
        return self.x + self.width < -50

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surf):
        r = self.get_rect()
        if self.kind == "cactus":
            # draw simple cactus with 2 arms
            pygame.draw.rect(surf, BLACK, r)
            pygame.draw.rect(surf, BLACK, (r.x - 6, r.y + r.h//3, 10, r.h//3))
            pygame.draw.rect(surf, BLACK, (r.x + r.w - 4, r.y + r.h//4, 8, r.h//3))
        elif self.kind == "ptera":
            # flying bird-like
            body = pygame.Rect(r.x, r.y+6, r.w//1.2, r.h//2)
            pygame.draw.ellipse(surf, BLACK, body)
            # wings
            if self.frame == 0:
                pygame.draw.polygon(surf, BLACK, [(r.x+10, r.y+12), (r.x+30, r.y), (r.x+50, r.y+12)])
            else:
                pygame.draw.polygon(surf, BLACK, [(r.x+10, r.y+12), (r.x+30, r.y+22), (r.x+50, r.y+12)])
        else:
            pygame.draw.rect(surf, BLACK, r)


# --------- Helpers ----------
def draw_ground(surf, offset):
    # simple moving ground stripes
    pygame.draw.line(surf, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
    for i in range(-50, WIDTH, 40):
        x = i + int(offset) % 40
        pygame.draw.line(surf, GRAY, (x, GROUND_Y), (x + 20, GROUND_Y), 2)

def draw_score(surf, score, hi):
    txt = font.render(f"Score: {score:04d}", True, BLACK)
    surf.blit(txt, (WIDTH - 150, 10))
    htxt = font.render(f"Best: {hi:04d}", True, BLACK)
    surf.blit(htxt, (WIDTH - 150, 30))

def spawn_obstacle(last_x, speed):
    # spawn at right edge plus little offset
    kinds = ["cactus", "cactus", "cactus", "ptera"]  # ptera rarer
    kind = random.choice(kinds)
    x = WIDTH + random.randint(10, 60)
    if kind == "cactus":
        return Obstacle(x, "cactus", speed)
    else:
        return Obstacle(x, "ptera", speed)

# --------- Main game loop ----------
def run_game():
    dino = Dino()
    obstacles = []
    running = True
    paused = False
    game_over = False

    spawn_timer = 0
    next_spawn = random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
    ground_offset = 0

    score = 0
    hi_score = 0
    speed_base = 6
    time_elapsed = 0

    while running:
        dt = clock.tick(FPS)  # ms since last frame
        time_elapsed += dt
        if not paused and not game_over:
            score += int(dt / 10)

        # Speed increases as score increases
        speed_increase = (score // 1000) * 0.5  # every 1000 score increases speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if not game_over and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck(True)
                if game_over and event.key == pygame.K_r:
                    return True  # restart
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.duck(False)

        if not running:
            break

        if not paused and not game_over:
            dino.update()
            ground_offset += (speed_base + speed_increase) * (dt / (1000 / FPS))

            # spawn management
            spawn_timer += dt
            if spawn_timer >= next_spawn:
                obstacles.append(spawn_obstacle(WIDTH, speed_base))
                spawn_timer = 0
                next_spawn = random.randint(OBSTACLE_MIN_GAP - int(speed_increase*50),
                                            OBSTACLE_MAX_GAP - int(speed_increase*50))
                # clamp
                if next_spawn < 350: next_spawn = 350

            # update obstacles
            for ob in obstacles:
                ob.update(dt, speed_increase)
            # remove off-screen
            obstacles = [o for o in obstacles if not o.off_screen()]

            # collisions
            drect = dino.get_rect()
            for ob in obstacles:
                if drect.colliderect(ob.get_rect()):
                    game_over = True
                    if score > hi_score:
                        hi_score = score
                    break

        # ------ draw ------
        screen.fill(SKY)
        # clouds (background)
        for i in range(3):
            cx = (i * 250) - (ground_offset/5 % 300)
            pygame.draw.ellipse(screen, WHITE, (cx, 40 + (i%2)*10, 80, 30))
        draw_ground(screen, ground_offset)
        dino.draw(screen)
        for ob in obstacles:
            ob.draw(screen)
        draw_score(screen, score, hi_score)

        if game_over:
            go_txt = big_font.render("Game Over", True, BLACK)
            sub = font.render("Press R to restart or Esc to quit", True, BLACK)
            screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 6))

        pygame.display.flip()

    return False  # not restarting

def main():
    restart = True
    while restart:
        restart = run_game()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
