import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 150, 0)
PURPLE = (150, 0, 200)
ORANGE = (255, 165, 0)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

# Path for enemies
PATH = [
    (0, 150),
    (300, 150),
    (300, 400),
    (600, 400),
    (600, 200),
    (900, 200),
    (900, 500),
    (WIDTH, 500)
]

# Tower types
TOWER_TYPES = {
    'basic': {'cost': 100, 'damage': 20, 'range': 120, 'fire_rate': 30, 'color': BLUE},
    'sniper': {'cost': 200, 'damage': 50, 'range': 250, 'fire_rate': 60, 'color': PURPLE},
    'cannon': {'cost': 150, 'damage': 15, 'range': 100, 'fire_rate': 20, 'color': ORANGE}
}


class Enemy:
    def __init__(self, health, speed, reward):
        self.health = health
        self.max_health = health
        self.speed = speed
        self.reward = reward
        self.path_index = 0
        self.x = PATH[0][0]
        self.y = PATH[0][1]
        self.radius = 15
        
    def move(self):
        if self.path_index < len(PATH) - 1:
            target_x, target_y = PATH[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < self.speed:
                self.path_index += 1
                if self.path_index >= len(PATH) - 1:
                    return True  # Reached end
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        return False
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        # Health bar
        health_width = 30
        health_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - 15, self.y - 25, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.x - 15, self.y - 25, health_width * health_ratio, health_height))
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0


class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.damage = TOWER_TYPES[tower_type]['damage']
        self.range = TOWER_TYPES[tower_type]['range']
        self.fire_rate = TOWER_TYPES[tower_type]['fire_rate']
        self.color = TOWER_TYPES[tower_type]['color']
        self.cooldown = 0
        self.target = None
        
    def find_target(self, enemies):
        closest = None
        min_dist = self.range
        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range:
                if closest is None or dist < min_dist:
                    closest = enemy
                    min_dist = dist
        return closest
    
    def shoot(self, enemies):
        if self.cooldown <= 0:
            target = self.find_target(enemies)
            if target:
                self.target = target
                target.take_damage(self.damage)
                self.cooldown = self.fire_rate
                return True
        return False
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def draw(self, screen, show_range=False):
        if show_range:
            pygame.draw.circle(screen, (255, 255, 255, 50), (self.x, self.y), self.range, 1)
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 20, 2)
        
        # Draw shooting line
        if self.target and self.cooldown > self.fire_rate - 5:
            pygame.draw.line(screen, YELLOW, (self.x, self.y), (int(self.target.x), int(self.target.y)), 2)


class Game:
    def __init__(self):
        self.money = 500
        self.lives = 20
        self.wave = 1
        self.enemies = []
        self.towers = []
        self.selected_tower_type = None
        self.game_over = False
        self.wave_active = False
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        
    def spawn_wave(self):
        self.wave_active = True
        enemy_count = 5 + self.wave * 3
        for i in range(enemy_count):
            health = 50 + self.wave * 20
            speed = 1 + self.wave * 0.1
            reward = 20 + self.wave * 5
            self.enemies_to_spawn.append(Enemy(health, min(speed, 3), reward))
    
    def update(self):
        if self.game_over:
            return
        
        # Spawn enemies from queue
        if self.enemies_to_spawn:
            self.spawn_timer += 1
            if self.spawn_timer >= 40:  # Spawn every 40 frames
                self.enemies.append(self.enemies_to_spawn.pop(0))
                self.spawn_timer = 0
        elif self.wave_active and not self.enemies:
            self.wave_active = False
            self.wave += 1
            self.money += 100  # Bonus for completing wave
        
        # Update enemies
        for enemy in self.enemies[:]:
            reached_end = enemy.move()
            if reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
        
        # Update towers
        for tower in self.towers:
            tower.update()
            if tower.shoot(self.enemies):
                # Remove dead enemies
                for enemy in self.enemies[:]:
                    if enemy.health <= 0:
                        self.money += enemy.reward
                        self.enemies.remove(enemy)
    
    def draw(self):
        screen.fill((34, 139, 34))  # Grass green
        
        # Draw path
        for i in range(len(PATH) - 1):
            pygame.draw.line(screen, GRAY, PATH[i], PATH[i + 1], 40)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
    
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 28)
        
        # Top bar
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, 60))
        
        money_text = font.render(f"Money: ${self.money}", True, YELLOW)
        lives_text = font.render(f"Lives: {self.lives}", True, RED)
        wave_text = font.render(f"Wave: {self.wave}", True, WHITE)
        
        screen.blit(money_text, (10, 15))
        screen.blit(lives_text, (250, 15))
        screen.blit(wave_text, (450, 15))
        
        # Tower selection buttons
        button_y = HEIGHT - 100
        button_x = 50
        
        for i, (name, info) in enumerate(TOWER_TYPES.items()):
            x = button_x + i * 150
            color = info['color'] if self.selected_tower_type != name else YELLOW
            pygame.draw.rect(screen, color, (x, button_y, 120, 80))
            pygame.draw.rect(screen, BLACK, (x, button_y, 120, 80), 3)
            
            name_text = small_font.render(name.capitalize(), True, BLACK)
            cost_text = small_font.render(f"${info['cost']}", True, BLACK)
            screen.blit(name_text, (x + 10, button_y + 10))
            screen.blit(cost_text, (x + 10, button_y + 45))
        
        # Start wave button
        if not self.wave_active:
            start_button_x = WIDTH - 200
            pygame.draw.rect(screen, GREEN, (start_button_x, button_y, 150, 80))
            pygame.draw.rect(screen, BLACK, (start_button_x, button_y, 150, 80), 3)
            start_text = font.render("Start Wave", True, BLACK)
            screen.blit(start_text, (start_button_x + 10, button_y + 25))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)
        
        game_over_text = font.render("GAME OVER", True, RED)
        wave_text = small_font.render(f"You survived {self.wave - 1} waves!", True, WHITE)
        restart_text = small_font.render("Press R to Restart", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(wave_text, (WIDTH//2 - 150, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 50))
    
    def handle_click(self, pos):
        x, y = pos
        
        # Check tower selection buttons
        button_y = HEIGHT - 100
        button_x = 50
        
        for i, (name, info) in enumerate(TOWER_TYPES.items()):
            btn_x = button_x + i * 150
            if btn_x <= x <= btn_x + 120 and button_y <= y <= button_y + 80:
                if self.money >= info['cost']:
                    self.selected_tower_type = name
                return
        
        # Check start wave button
        if not self.wave_active:
            start_button_x = WIDTH - 200
            if start_button_x <= x <= start_button_x + 150 and button_y <= y <= button_y + 80:
                self.spawn_wave()
                return
        
        # Place tower
        if self.selected_tower_type and y < HEIGHT - 120:
            cost = TOWER_TYPES[self.selected_tower_type]['cost']
            if self.money >= cost:
                # Check if not on path
                on_path = False
                for i in range(len(PATH) - 1):
                    x1, y1 = PATH[i]
                    x2, y2 = PATH[i + 1]
                    dist = self.point_to_line_distance(x, y, x1, y1, x2, y2)
                    if dist < 40:
                        on_path = True
                        break
                
                if not on_path:
                    self.towers.append(Tower(x, y, self.selected_tower_type))
                    self.money -= cost
                    self.selected_tower_type = None
    
    def point_to_line_distance(self, px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.sqrt((px - x1)**2 + (py - y1)**2)
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.sqrt((px - proj_x)**2 + (py - proj_y)**2)


# Main game loop
def main():
    game = Game()
    running = True
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = Game()  # Restart
        
        game.update()
        game.draw()
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()