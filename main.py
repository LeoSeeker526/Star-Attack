import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1250, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Attack")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 35
GROUND_HEIGHT = 60
PLAYER_VEL = 5
BADDIE_VEL = 2.5
BADDIE_WIDTH = 20
BADDIE_HEIGHT = 20
FONT = pygame.font.SysFont("ocraextended", 30)
TITLE_FONT = pygame.font.SysFont("ocraextended", 70)  # Larger font for title and game over



def draw(player, elapsed_time, baddies, lives, bullets, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    lives_text = FONT.render(f"Lives: {lives}", 1, "white")
    WIN.blit(lives_text, (10, 40))

    score_text = FONT.render(f"Score: {score}", 1, "white")  # Display the score
    WIN.blit(score_text, (10, 70))

    # Draw the player
    player_triangle = [
        (player.x + player.width // 2, player.y),  # Top point of the triangle
        (player.x, player.y + player.height),      # Bottom-left corner
        (player.x + player.width, player.y + player.height)  # Bottom-right corner
    ]
    pygame.draw.polygon(WIN, "red", player_triangle)

    # Draw baddies
    for baddie_data in baddies:
        baddie = baddie_data["rect"]
        baddie_triangle = [
            (baddie.x + baddie.width // 2, baddie.y + baddie.height),  # Bottom point of the triangle
            (baddie.x, baddie.y),                                      # Top-left corner
            (baddie.x + baddie.width, baddie.y)                       # Top-right corner
        ]
        pygame.draw.polygon(WIN, "purple", baddie_triangle)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(WIN, "yellow", (bullet.x, bullet.y), bullet.width // 2)

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
            if event.type == pygame.KEYDOWN:  # Wait for any key to be pressed
                return

def instructions_screen():
    WIN.fill("black")
    instructions_title = FONT.render("Instructions", 1, "white")
    instructions_text1 = FONT.render("Move: Arrow Keys", 1, "white")
    instructions_text2 = FONT.render("Shoot: Spacebar", 1, "white")
    instructions_text3 = FONT.render("Goal: Survive and destroy enemies to score points!", 1, "white")
    start_text = FONT.render("Press any key to Start the Game", 1, "white")

    WIN.blit(instructions_title, (WIDTH // 2 - instructions_title.get_width() // 2, HEIGHT // 2 - 150))
    WIN.blit(instructions_text1, (WIDTH // 2 - instructions_text1.get_width() // 2, HEIGHT // 2 - 50))
    WIN.blit(instructions_text2, (WIDTH // 2 - instructions_text2.get_width() // 2, HEIGHT // 2))
    WIN.blit(instructions_text3, (WIDTH // 2 - instructions_text3.get_width() // 2, HEIGHT // 2 + 50))
    WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # Wait for any key to be pressed
                return



def game_over_screen(elapsed_time, score):
    WIN.fill("black")
    game_over_text = TITLE_FONT.render("Game Over!", 1, "red")
    score_text = FONT.render(f"Time Survived: {round(elapsed_time)} seconds", 1, "white")
    final_score_text = FONT.render(f"Final Score: {score}", 1, "white")  # Display final score
    restart_text = FONT.render("Press R to Restart or Q to Quit", 1, "white")

    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 40))  # Display score
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()  # Restart the game
        if keys[pygame.K_q]:
            pygame.quit()
            exit()


def main():
    start_screen()        # Display the start screen
    instructions_screen() # Display the instructions screen

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    baddie_add_increment = 2000
    baddie_count = 0

    baddies = []
    bullets = []  # List to track bullets
    bullet_vel = 7  # Speed of bullets
    bullet_cooldown = 500  # 500 ms cooldown between bullets
    last_bullet_time = 0  # Timestamp of the last bullet fired
    last_time_bonus = 0  # Track last time bonus was given
    lives = 3
    hit = False
    score = 0  # Initialize score

    while run:
        baddie_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Increment score for every 10 seconds passed
        if elapsed_time - last_time_bonus >= 10:
            score += 10
            last_time_bonus += 10

        # Spawn baddies only from the top
        if baddie_count > baddie_add_increment:
            for _ in range(3):  # Add 3 baddies at a time
                baddie_x = random.randint(0, WIDTH - BADDIE_WIDTH)
                baddie = pygame.Rect(baddie_x, -BADDIE_HEIGHT, BADDIE_WIDTH, BADDIE_HEIGHT)
                baddies.append({"rect": baddie, "x_vel": 0, "y_vel": BADDIE_VEL})

            baddie_add_increment = max(200, baddie_add_increment - 50)
            baddie_count = 0

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
            if current_time - last_bullet_time > bullet_cooldown:  # Check if cooldown period has passed
                bullet = pygame.Rect(player.x + player.width // 2 - 5, player.y, 10, 10)  # Centered bullet
                bullets.append(bullet)
                last_bullet_time = current_time

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_vel
            if bullet.y < 0:  # Remove bullet if it goes out of bounds
                bullets.remove(bullet)

        # Move baddies and handle collisions
        for baddie_data in baddies[:]:
            baddie = baddie_data["rect"]
            baddie.x += baddie_data["x_vel"]
            baddie.y += baddie_data["y_vel"]

            # Remove baddie if it leaves the screen
            if baddie.y > HEIGHT:
                baddies.remove(baddie_data)
            elif baddie.colliderect(player):  # Handle collision with player
                baddies.remove(baddie_data)
                lives -= 1
                if lives <= 0:
                    hit = True
                break

        # Handle bullet-baddie collisions
        for bullet in bullets[:]:
            for baddie_data in baddies[:]:
                baddie = baddie_data["rect"]
                if baddie.colliderect(bullet):  # If bullet hits baddie
                    bullets.remove(bullet)
                    baddies.remove(baddie_data)
                    score += 5  # Increment score when baddie is destroyed
                    break

        draw(player, elapsed_time, baddies, lives, bullets, score)  # Pass score to draw function

        if hit:
            game_over_screen(elapsed_time, score)
            break

    pygame.quit()





if __name__ == "__main__":
    main()
