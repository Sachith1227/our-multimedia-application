import pygame
import sys
import random

def play_game():
    # Initialize pygame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Volleyball Game - Multiplayer")

    # Load background image
    background = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\background2.jpg"
    )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Colors
    NET_COLOR = (128, 0, 0)
    GROUND_COLOR = (124, 50, 0)
    SCORE_COLOR_P1 = (255, 255, 0)
    SCORE_COLOR_P2 = (255, 100, 100)
    GROUND_HEIGHT = 50

        # Button colors
    BUTTON_COLOR = (70, 130, 180)       # Steel blue
    BUTTON_HOVER = (100, 149, 237)      # Lighter blue
    BUTTON_SHADOW = (40, 90, 120)       # Darker shadow


    # --- Player 1 setup (Left) ---
    P1_RADIUS = 80
    p1_x = WIDTH // 4
    p1_y = HEIGHT - GROUND_HEIGHT - (P1_RADIUS * 2)
    p1_vx = 0
    p1_vy = 0
    PLAYER_SPEED = 6
    JUMP_STRENGTH = -8
    p1_on_ground = True

    # --- Player 2 setup (Right) ---
    P2_RADIUS = 80
    p2_x = 3 * WIDTH // 4
    p2_y = HEIGHT - GROUND_HEIGHT - (P2_RADIUS * 2)
    p2_vx = 0
    p2_vy = 0
    p2_on_ground = True

    # Load images
    p1_image = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\player.png"
    ).convert_alpha()
    p1_image = pygame.transform.scale(p1_image, (P1_RADIUS * 2, P1_RADIUS * 2))
    p2_image = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\cpu.png"
    ).convert_alpha()
    p2_image = pygame.transform.scale(p2_image, (P2_RADIUS * 2, P2_RADIUS * 2))

    # Masks for pixel-perfect collision
    p1_mask = pygame.mask.from_surface(p1_image)
    p2_mask = pygame.mask.from_surface(p2_image)

    # --- Ball setup ---
    BALL_RADIUS = 50
    ball_x = WIDTH // 2
    ball_y = 100
    ball_vx = 4
    ball_vy = 0
    GRAVITY = 0.2
    BOUNCE = -0.8
    MAX_VX = 7
    MAX_VY = 10

    ball_image = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\ball.png"
    ).convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
    ball_mask = pygame.mask.from_surface(ball_image)

    # Load sounds
    point_sound = pygame.mixer.Sound(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\sounds\point.wav")
    hit_sound = pygame.mixer.Sound(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\sounds\jump.wav")
    win_sound = pygame.mixer.Sound(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\sounds\win.wav")
    point_sound.set_volume(0.7)
    hit_sound.set_volume(0.5)
    win_sound.set_volume(0.7)

    # Score
    p1_score = 0
    p2_score = 0
    font = pygame.font.SysFont(None, 40)
    WIN_SCORE = 7

    # Floating +1 points
    floating_points = []

    # Buttons after win
    button_font = pygame.font.SysFont(None, 40)
    post_win_buttons = {
        "Play Again": pygame.Rect(WIDTH//2-100, 300, 200, 50),
        "Quit": pygame.Rect(WIDTH//2-100, 400, 200, 50)
    }


    # Custom font for winner
    font_path = r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\fonts\1.ttf"

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- PLAYER CONTROLS ---
        keys = pygame.key.get_pressed()

        # Player 1 (WASD)
        p1_vx = 0
        if keys[pygame.K_a]:
            p1_vx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            p1_vx = PLAYER_SPEED
        if keys[pygame.K_w] and p1_on_ground:
            p1_vy = JUMP_STRENGTH
            p1_on_ground = False

        # Player 2 (Arrows)
        p2_vx = 0
        if keys[pygame.K_LEFT]:
            p2_vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            p2_vx = PLAYER_SPEED
        if keys[pygame.K_UP] and p2_on_ground:
            p2_vy = JUMP_STRENGTH
            p2_on_ground = False

        # Apply gravity + movement
        p1_vy += GRAVITY
        p1_y += p1_vy
        p1_x += p1_vx

        p2_vy += GRAVITY
        p2_y += p2_vy
        p2_x += p2_vx

        # Ground collisions
        if p1_y + P1_RADIUS * 2 >= HEIGHT - GROUND_HEIGHT:
            p1_y = HEIGHT - GROUND_HEIGHT - P1_RADIUS * 2
            p1_vy = 0
            p1_on_ground = True
        if p2_y + P2_RADIUS * 2 >= HEIGHT - GROUND_HEIGHT:
            p2_y = HEIGHT - GROUND_HEIGHT - P2_RADIUS * 2
            p2_vy = 0
            p2_on_ground = True

        # Keep players inside their halves
        if p1_x - P1_RADIUS < 0:
            p1_x = P1_RADIUS
        if p1_x + P1_RADIUS > WIDTH // 2 - 15:
            p1_x = WIDTH // 2 - 15 - P1_RADIUS

        if p2_x - P2_RADIUS < WIDTH // 2 + 15:
            p2_x = WIDTH // 2 + 15 + P2_RADIUS
        if p2_x + P2_RADIUS > WIDTH:
            p2_x = WIDTH - P2_RADIUS

        # --- BALL PHYSICS ---
        ball_vy += GRAVITY
        ball_x += ball_vx
        ball_y += ball_vy
        ball_vx = max(min(ball_vx, MAX_VX), -MAX_VX)
        ball_vy = max(min(ball_vy, MAX_VY), -MAX_VY)

        # Ground collision for ball
        if ball_y + BALL_RADIUS > HEIGHT - GROUND_HEIGHT:
            ball_y = HEIGHT - GROUND_HEIGHT - BALL_RADIUS
            ball_vy *= BOUNCE

            if ball_x < WIDTH // 2:
                p2_score += 1
                text_surf = font.render("+1", True, SCORE_COLOR_P2)
                floating_points.append([WIDTH*3//4, HEIGHT//2 - 100, text_surf, 255])
            else:
                p1_score += 1
                text_surf = font.render("+1", True, SCORE_COLOR_P1)
                floating_points.append([WIDTH//4, HEIGHT//2 - 100, text_surf, 255])

            point_sound.play()

            # Reset ball
            ball_x = WIDTH // 2
            ball_y = 100
            ball_vx = 4 * random.choice([-1, 1])
            ball_vy = 0

        # Wall collisions
        if ball_x - BALL_RADIUS < 0:
            ball_x = BALL_RADIUS
            ball_vx *= -1
        if ball_x + BALL_RADIUS > WIDTH:
            ball_x = WIDTH - BALL_RADIUS
            ball_vx *= -1
        if ball_y - BALL_RADIUS < 0:
            ball_y = BALL_RADIUS
            ball_vy *= -1

        # Net collision
        net_x = WIDTH // 2
        net_width = 15
        NET_HEIGHT = 170
        net_rect = pygame.Rect(net_x - net_width // 2, HEIGHT - GROUND_HEIGHT - NET_HEIGHT, net_width, NET_HEIGHT)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if ball_rect.colliderect(net_rect):
            ball_vx *= -1

        # Pixel-perfect collision
        p1_pos = (int(p1_x - P1_RADIUS), int(p1_y))
        p2_pos = (int(p2_x - P2_RADIUS), int(p2_y))
        ball_pos = (int(ball_x - BALL_RADIUS), int(ball_y - BALL_RADIUS))

        offset_p1 = (ball_pos[0] - p1_pos[0], ball_pos[1] - p1_pos[1])
        offset_p2 = (ball_pos[0] - p2_pos[0], ball_pos[1] - p2_pos[1])

        if p1_mask.overlap(ball_mask, offset_p1):
            ball_vy = -abs(ball_vy) - 3
            ball_vx += (ball_x - p1_x) / P1_RADIUS * 3
            hit_sound.play()
        if p2_mask.overlap(ball_mask, offset_p2):
            ball_vy = -abs(ball_vy) - 3
            ball_vx += (ball_x - p2_x) / P2_RADIUS * 3
            hit_sound.play()

        # --- DRAW ---
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, NET_COLOR, net_rect)
        screen.blit(p1_image, p1_pos)
        screen.blit(p2_image, p2_pos)
        screen.blit(ball_image, ball_pos)

        # Draw floating points
        for fp in floating_points[:]:
            x, y, surf, alpha = fp
            surf.set_alpha(alpha)
            screen.blit(surf, (x - surf.get_width()//2, y))
            fp[1] -= 1
            fp[3] -= 5
            if fp[3] <= 0:
                floating_points.remove(fp)

        # Scoreboard
        score_font = pygame.font.SysFont(None, 60)
        p1_text = score_font.render(f"P1: {p1_score}", True, SCORE_COLOR_P1)
        p2_text = score_font.render(f"P2: {p2_score}", True, SCORE_COLOR_P2)
        screen.blit(p1_text, (50, 20))
        screen.blit(p2_text, (WIDTH - p2_text.get_width() - 50, 20))

        # --- WIN CONDITION POPUP ---
        winner = None
        if p1_score >= WIN_SCORE:
            winner = "Player 1"
        elif p2_score >= WIN_SCORE:
            winner = "Player 2"

        if winner:
            win_sound.play()
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,150))
            screen.blit(overlay,(0,0))

            # Winner text
            win_font = pygame.font.SysFont(None, 80)
            win_text = win_font.render(f"{winner} Wins!", True, (255,255,0))
            screen.blit(win_text, ((WIDTH-win_text.get_width())//2, 150))

            # Buttons after win
            button_font = pygame.font.SysFont(None, 40)
            post_win_buttons = {
                "Play Again": pygame.Rect(WIDTH//2-100, 300, 200, 50),
                "Quit": pygame.Rect(WIDTH//2-100, 400, 200, 50)
            }
            
            # Draw buttons
            mx,my = pygame.mouse.get_pos()
            for text, rect in post_win_buttons.items():
                color = BUTTON_HOVER if rect.collidepoint(mx,my) else BUTTON_COLOR
                shadow = rect.copy()
                shadow.x +=5
                shadow.y +=5
                pygame.draw.rect(screen,BUTTON_SHADOW,shadow,border_radius=15)
                pygame.draw.rect(screen,color,rect,border_radius=15)
                pygame.draw.rect(screen,(255,255,255),rect,3,border_radius=15)
                label = button_font.render(text, True, (255,255,255))
                screen.blit(label,label.get_rect(center=rect.center))
            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx,my = pygame.mouse.get_pos()
                        if post_win_buttons["Play Again"].collidepoint(mx, my):
                            # Reset scores
                            p1_score = 0
                            p2_score = 0

                            # Reset ball
                            ball_x, ball_y = WIDTH // 2, 100
                            ball_vx, ball_vy = 4, 0

                            # Reset players
                            p1_x, p1_y = WIDTH // 4, HEIGHT - GROUND_HEIGHT - P1_RADIUS * 2
                            p2_x, p2_y = 3 * WIDTH // 4, HEIGHT - GROUND_HEIGHT - P2_RADIUS * 2
                            p1_vx, p1_vy = 0, 0
                            p2_vx, p2_vy = 0, 0
                            p1_on_ground = True
                            p2_on_ground = True

                            # Clear floating points
                            floating_points.clear()

                            waiting = False

                        elif post_win_buttons["Quit"].collidepoint(mx,my):
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    play_game()
