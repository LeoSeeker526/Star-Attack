import pygame
import time
import random
import math  # For drawing the hexagon
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1250, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Attack")

# --- Load assets from the 'assets' folder ---
BG = pygame.transform.scale(pygame.image.load("assets/bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 35
GROUND_HEIGHT = 60
PLAYER_VEL = 5
BADDIE_VEL = 2.5
BADDIE_WIDTH = 20
BADDIE_HEIGHT = 20
FONT = pygame.font.SysFont("ocraextended", 30)
TITLE_FONT = pygame.font.SysFont("ocraextended", 70)

# --- New constants for Mega Baddie ---
MEGA_BADDIE_WIDTH = 60
MEGA_BADDIE_HEIGHT = 60
MEGA_BADDIE_VEL = 0.8  # Reduced speed
MEGA_BADDIE_HEALTH = 10
MEGA_BADDIE_COLOR = "blue"
MEGA_PROJECTILE_RADIUS = 8
MEGA_PROJECTILE_VEL = 4
MEGA_FIRE_RATE = 1000  # Milliseconds between shots
MEGA_SCORE_VALUE = 50  # Score awarded for defeating the mega baddie
# -------------------------------------

# --- Load sound effects from the 'assets' folder ---
try:
    PLAYER_FIRE_SOUND = pygame.mixer.Sound("assets/fire.ogg")
    MEGA_BADDIE_FIRE_SOUND = pygame.mixer.Sound("assets/megafire.ogg")
    MEGA_BADDIE_EXPLODE_SOUND = pygame.mixer.Sound("assets/megaexplode.ogg")
    GAME_OVER_SOUND = pygame.mixer.Sound("assets/gameover.ogg")
    HULL_DAMAGE_SOUND = pygame.mixer.Sound("assets/hulldamage.ogg") # Added sound
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    PLAYER_FIRE_SOUND = None
    MEGA_BADDIE_FIRE_SOUND = None
    MEGA_BADDIE_EXPLODE_SOUND = None
    GAME_OVER_SOUND = None
    HULL_DAMAGE_SOUND = None
# --------------------------

def draw_hexagon(surface, color, center, size):
    points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        x = center[0] + size * math.cos(angle)
        y = center[1] + size * math.sin(angle)
        points.append((int(x), int(y)))
    pygame.draw.polygon(surface, color, points)

class MegaBaddie(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, MEGA_BADDIE_WIDTH, MEGA_BADDIE_HEIGHT)
        self.health = MEGA_BADDIE_HEALTH
        self.x_vel = MEGA_BADDIE_VEL * random.choice([-1, 1])
        # Ensure initial vertical velocity is not zero
        self.y_vel = MEGA_BADDIE_VEL * random.choice([-1, 1])
        while self.y_vel == 0:
            self.y_vel = MEGA_BADDIE_VEL * random.choice([-1, 1])
        self.last_shot_time = pygame.time.get_ticks()
        self.projectiles = []

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.left < 0 or self.right > WIDTH:
            self.x_vel *= -1
        if self.top < 0 or self.bottom > HEIGHT:
            self.y_vel *= -1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > MEGA_FIRE_RATE:
            projectile_x = self.centerx
            projectile_y = self.centery
            projectile = pygame.Rect(projectile_x - MEGA_PROJECTILE_RADIUS,
                                     projectile_y - MEGA_PROJECTILE_RADIUS,
                                     MEGA_PROJECTILE_RADIUS * 2,
                                     MEGA_PROJECTILE_RADIUS * 2)
            self.projectiles.append(projectile)
            self.last_shot_time = current_time
            # Play sound effect
            if MEGA_BADDIE_FIRE_SOUND:
                MEGA_BADDIE_FIRE_SOUND.play()

    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.y += MEGA_PROJECTILE_VEL
            if projectile.top > HEIGHT:
                self.projectiles.remove(projectile)

    def draw(self, surface):
        draw_hexagon(surface, MEGA_BADDIE_COLOR, self.center, MEGA_BADDIE_WIDTH // 2)
        for projectile in self.projectiles:
            pygame.draw.circle(surface, "lightblue", projectile.center, MEGA_PROJECTILE_RADIUS)

def draw(player, elapsed_time, baddies, lives, bullets, score, mega_baddie):
    WIN.blit(BG, (0, 0))

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = FONT.render(f"Time: {minutes:02d}:{seconds:02d}", 1, "white")
    WIN.blit(time_text, (10, 10))

    lives_text = FONT.render(f"Lives: {lives}", 1, "white")
    WIN.blit(lives_text, (10, 40))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (10, 70))

    # Draw the player
    player_triangle = [
        (player.x + player.width // 2, player.y),
        (player.x, player.y + player.height),
        (player.x + player.width, player.y + player.height)
    ]
    pygame.draw.polygon(WIN, "red", player_triangle)

    # Draw baddies
    for baddie_data in baddies:
        baddie = baddie_data["rect"]
        baddie_triangle = [
            (baddie.x + baddie.width // 2, baddie.y + baddie.height),
            (baddie.x, baddie.y),
            (baddie.x + baddie.width, baddie.y)
        ]
        pygame.draw.polygon(WIN, "purple", baddie_triangle)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(WIN, "yellow", (bullet.x, bullet.y), bullet.width // 2)

    # Draw Mega Baddie if it exists
    if mega_baddie:
        mega_baddie.draw(WIN)

    pygame.display.update()

def start_screen():
    WIN.fill("black")
    title_text = TITLE_FONT.render("Star Attack", 1, "white")
    proceed_text = FONT.render("Press any key to continue", 1, "white")

    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    WIN.blit(proceed_text, (WIDTH // 2 - proceed_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

def instructions_screen():
    WIN.fill("black")
    instructions_title = FONT.render("Instructions", 1, "white")
    instructions_text1 = FONT.render("Move: Arrow Keys", 1, "white")
    instructions_text2 = FONT.render("Shoot: Spacebar", 1, "white")
    instructions_text3 = FONT.render("Goal: Survive and destroy enemies to score points!", 1, "white")
    mega_baddie_info = FONT.render("Mega Baddie appears at 30s and 40s after defeat!", 1, "yellow")
    mega_baddie_attack = FONT.render("It shoots light blue projectiles and takes 10 hits!", 1, "yellow")
    start_text = FONT.render("Press any key to Start the Game", 1, "white")

    WIN.blit(instructions_title, (WIDTH // 2 - instructions_title.get_width() // 2, HEIGHT // 2 - 200))
    WIN.blit(instructions_text1, (WIDTH // 2 - instructions_text1.get_width() // 2, HEIGHT // 2 - 100))
    WIN.blit(instructions_text2, (WIDTH // 2 - instructions_text2.get_width() // 2, HEIGHT // 2 - 50))
    WIN.blit(instructions_text3, (WIDTH // 2 - instructions_text3.get_width() // 2, HEIGHT // 2))
    WIN.blit(mega_baddie_info, (WIDTH // 2 - mega_baddie_info.get_width() // 2, HEIGHT // 2 + 75))
    WIN.blit(mega_baddie_attack, (WIDTH // 2 - mega_baddie_attack.get_width() // 2, HEIGHT // 2 + 100))
    WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 175))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

def game_over_screen(elapsed_time, score):
    WIN.fill("black")
    game_over_text = TITLE_FONT.render("Game Over!", 1, "red")
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    score_text = FONT.render(f"Time Survived: {minutes:02d}:{seconds:02d}", 1, "white")
    final_score_text = FONT.render(f"Final Score: {score}", 1, "white")
    restart_text = FONT.render("Press R to Restart or Q to Quit", 1, "white")

    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 40))
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()
        if keys[pygame.K_q]:
            pygame.quit()
            exit()

def main():
    start_screen()
    instructions_screen()

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    baddie_add_increment = 2000
    baddie_count = 0
    baddies = []

    bullets = []
    bullet_vel = 7
    bullet_cooldown = 250  # Reduced cooldown for more action
    last_bullet_time = 0
    last_time_bonus = 0
    lives = 3
    hit = False
    score = 0
    # hull_damage_played = False # removed general flag
    life_lost_2 = False
    life_lost_1 = False
    life_lost_0 = False #added flag

    mega_baddie = None
    mega_baddie_spawned = False
    mega_baddie_last_spawn_time = 0  # To track last spawn time

    while run:
        baddie_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Increment score for every 10 seconds passed
        if elapsed_time - last_time_bonus >= 10:
            score += 10
            last_time_bonus += 10

        # Spawn regular baddies if Mega Baddie is not present
        if mega_baddie is None:
            if baddie_count > baddie_add_increment:
                for _ in range(3):
                    baddie_x = random.randint(0, WIDTH - BADDIE_WIDTH)
                    baddie = pygame.Rect(baddie_x, -BADDIE_HEIGHT, BADDIE_WIDTH, BADDIE_HEIGHT)
                    baddies.append({"rect": baddie, "x_vel": 0, "y_vel": BADDIE_VEL})

                baddie_add_increment = max(200, baddie_add_increment - 50)
                baddie_count = 0

        # Spawn Mega Baddie at 30 seconds initially, and then every 40 seconds after the previous one is defeated
        if (elapsed_time >= 30 and not mega_baddie_spawned and (elapsed_time - mega_baddie_last_spawn_time >= 40 or mega_baddie_last_spawn_time == 0)):
            mega_baddie_x = random.randint(0, WIDTH - MEGA_BADDIE_WIDTH)
            mega_baddie_y = random.randint(50, HEIGHT // 2 - MEGA_BADDIE_HEIGHT)  # Spawn in the upper half
            mega_baddie = MegaBaddie(mega_baddie_x, mega_baddie_y)
            mega_baddie_spawned = True
            mega_baddie_last_spawn_time = elapsed_time  # update last spawn time
            baddies = []  # Clear regular baddies when mega baddie appears

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        # Handle shooting with cooldown
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_bullet_time > bullet_cooldown:
                bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y, 10, 10)
                bullets.append(bullet)
                last_bullet_time = current_time
                # Play sound effect
                if PLAYER_FIRE_SOUND:
                    PLAYER_FIRE_SOUND.play()

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_vel
            if bullet.y < 0:
                bullets.remove(bullet)

        # Move baddies and handle collisions
        if mega_baddie:
            mega_baddie.move()
            mega_baddie.shoot()
            mega_baddie.update_projectiles()
            for projectile in mega_baddie.projectiles[:]:
                if projectile.colliderect(player):
                    mega_baddie.projectiles.remove(projectile)
                    lives -= 1
                    if lives <= 0:
                        hit = True
                        break
                if projectile.top > HEIGHT:
                    mega_baddie.projectiles.remove(projectile)

            # Handle bullet-mega baddie collisions
            for bullet in bullets[:]:
                if mega_baddie.colliderect(bullet):
                    bullets.remove(bullet)
                    mega_baddie.health -= 1
                    if mega_baddie.health <= 0:
                        mega_baddie = None
                        mega_baddie_spawned = False
                        mega_baddie_last_spawn_time = elapsed_time  # record time of death for next spawn
                        baddie_add_increment = 2000  # Reset baddie spawn rate
                        baddie_count = 0  # Reset baddie spawn counter
                        score += MEGA_SCORE_VALUE  # Award score for defeating mega baddie
                        # Play explosion sound
                        if MEGA_BADDIE_EXPLODE_SOUND:
                            MEGA_BADDIE_EXPLODE_SOUND.play()
                    break  # Only one bullet can hit the mega baddie per frame
        else:
            for baddie_data in baddies[:]:
                baddie = baddie_data["rect"]
                baddie.x += baddie_data["x_vel"]
                baddie.y += baddie_data["y_vel"]

                if baddie.y > HEIGHT:
                    baddies.remove(baddie_data)
                elif baddie.colliderect(player):
                    baddies.remove(baddie_data)
                    lives -= 1
                    if lives <= 0:
                        hit = True
                        break
            # Handle bullet-baddie collisions (only if no mega baddie)
            for bullet in bullets[:]:
                for baddie_data in baddies[:]:
                    baddie = baddie_data["rect"]
                    if baddie.colliderect(bullet):
                        bullets.remove(bullet)
                        baddies.remove(baddie_data)
                        score += 5
                        break

        draw(player, elapsed_time, baddies, lives, bullets, score, mega_baddie)

        if hit:
            # Play game over sound
            if GAME_OVER_SOUND:
                GAME_OVER_SOUND.play()
            game_over_screen(elapsed_time, score)
            break
        
        # Play hull damage sound
        if lives == 2 and not life_lost_2:
            if HULL_DAMAGE_SOUND:
                HULL_DAMAGE_SOUND.play()
            life_lost_2 = True
        elif lives == 1 and not life_lost_1:
            if HULL_DAMAGE_SOUND:
                HULL_DAMAGE_SOUND.play()
            life_lost_1 = True
        elif lives == 0 and not life_lost_0: #added condition
            if HULL_DAMAGE_SOUND:
                HULL_DAMAGE_SOUND.play()
            life_lost_0 = True

    pygame.quit()

if __name__ == "__main__":
    main()
