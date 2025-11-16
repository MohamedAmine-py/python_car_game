import pygame
import random
import sys

# Initialize pygame
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Game")

# --- Colors ---
ROAD_COLOR = (40, 40, 40)
LINE_COLOR = (255, 255, 255)
BG_COLOR = (70, 100, 180)

# --- Load car images ---
player_car = pygame.image.load("car_blue_5.png")
enemy_cars = [
    pygame.image.load("car_red_5.png"),
    pygame.image.load("car_green_5.png"),
    pygame.image.load("car_yellow_5.png"),
]

# --- Resize images ---
car_width, car_height = 50, 100
player_car = pygame.transform.scale(player_car, (car_width, car_height))
enemy_cars = [pygame.transform.scale(img, (car_width, car_height)) for img in enemy_cars]

# --- Game variables ---
clock = pygame.time.Clock()
player = pygame.Rect(WIDTH // 2 - car_width // 2, HEIGHT - 150, car_width, car_height)
enemy_list = []
score = 0
game_active = False

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# --- Helper functions ---
def get_window_dimensions():
    """Get current window dimensions"""
    return win.get_size()

def get_lanes(width):
    """Calculate lane positions based on window width"""
    return [width // 2 - 100, width // 2, width // 2 + 100]

def get_road_lines(width, height):
    """Generate road lines based on window dimensions"""
    return [pygame.Rect(width // 2 - 5, i * 150, 10, 100) for i in range(6)]

def reset_game():
    global enemy_list, score, game_active, player, road_lines
    width, height = get_window_dimensions()
    player.x = width // 2 - car_width // 2
    player.y = height - 150
    enemy_list = []
    score = 0
    game_active = True
    road_lines = get_road_lines(width, height)

def draw_window():
    width, height = get_window_dimensions()
    win.fill(BG_COLOR)

    # Draw road
    pygame.draw.rect(win, ROAD_COLOR, (width // 2 - 150, 0, 300, height))
    pygame.draw.line(win, LINE_COLOR, (width // 2 - 150, 0), (width // 2 - 150, height), 5)
    pygame.draw.line(win, LINE_COLOR, (width // 2 + 150, 0), (width // 2 + 150, height), 5)

    # Draw road lines
    for line in road_lines:
        pygame.draw.rect(win, LINE_COLOR, line)

    # Draw cars
    win.blit(player_car, player)
    for enemy in enemy_list:
        win.blit(enemy[0], enemy[1])

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    pygame.display.update()

def move_lines(speed):
    height = get_window_dimensions()[1]
    for line in road_lines:
        line.y += speed
        if line.y > height:
            line.y = -100

def create_enemy():
    width = get_window_dimensions()[0]
    lanes = get_lanes(width)
    
    # Check if we should spawn a new enemy (reduced frequency)
    if len(enemy_list) < 3 and random.randint(0, 100) < 1.5:
        # Count how many cars are in each lane in the spawn zone (top 300 pixels)
        lane_counts = {lane: 0 for lane in lanes}
        for enemy in enemy_list:
            if enemy[1].y < 300:  # Check a larger spawn zone
                # Find which lane this car is in
                for lane in lanes:
                    if abs(enemy[1].centerx - lane) < car_width:
                        lane_counts[lane] += 1
                        break
        
        # Never allow all lanes to be blocked - always keep at least one lane completely free
        blocked_lanes = [lane for lane, count in lane_counts.items() if count > 0]
        
        # If 2 or more lanes are blocked, don't spawn
        if len(blocked_lanes) >= 2:
            return
        
        # Get available lanes (lanes with no cars near spawn)
        available_lanes = [lane for lane, count in lane_counts.items() if count == 0]
        
        # Only spawn if there are available lanes
        if available_lanes:
            lane = random.choice(available_lanes)
            car = random.choice(enemy_cars)
            rect = pygame.Rect(lane - car_width // 2, -120, car_width, car_height)
            enemy_list.append((car, rect))

def move_enemies(speed):
    global game_active
    height = get_window_dimensions()[1]
    for enemy in list(enemy_list):
        enemy[1].y += speed
        if enemy[1].y > height:
            enemy_list.remove(enemy)
        if player.colliderect(enemy[1]):
            game_active = False

# Initialize road lines
road_lines = get_road_lines(WIDTH, HEIGHT)

# --- Main game loop ---
running = True
while running:
    clock.tick(60)
    width, height = get_window_dimensions()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle window resize
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            road_lines = get_road_lines(width, height)
            # Recenter player
            player.x = width // 2 - car_width // 2

    keys = pygame.key.get_pressed()

    if game_active:
        # Player movement
        if keys[pygame.K_LEFT] and player.x > width // 2 - 150 + 10:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x < width // 2 + 150 - car_width - 10:
            player.x += 5
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y < height - car_height:
            player.y += 5

        # Update score
        score += 1

        # Difficulty scaling (smooth + capped)
        difficulty = 1 + (score / 5000)
        difficulty = min(difficulty, 3)

        # Move lines and enemies
        move_lines(5 * difficulty)
        create_enemy()
        move_enemies(5 * difficulty)

        draw_window()

    else:
        # Display start or game over screen
        win.fill(BG_COLOR)
        title = big_font.render(
            "Press Enter to Start" if score == 0 else "Game Over! Press Enter to Restart",
            True, (255, 255, 255)
        )
        win.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 50))

        pygame.display.update()

        # Wait for Enter to start or restart
        if keys[pygame.K_RETURN]:
            reset_game()