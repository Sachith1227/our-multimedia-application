import pygame
import sys
import random

def play_game():
    # Initialize pygame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Volleyball Game")

    # Load background image
    background = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\background2.jpg"
    )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Colors
    NET_COLOR = (128, 0, 0)
    GROUND_COLOR = (124, 50, 0)
    BUTTON_COLOR = (200, 50, 50)
    BUTTON_HOVER = (0, 200, 200)
    BUTTON_SHADOW = (220, 220, 20)
    SCORE_COLOR_PLAYER = (255, 255, 0)
    SCORE_COLOR_CPU = (255, 100, 100)
    GROUND_HEIGHT = 50

    # --- Player setup ---
    PLAYER_RADIUS = 80
    player_x = WIDTH // 4
    player_y = HEIGHT - GROUND_HEIGHT - (PLAYER_RADIUS * 2)
    player_vx = 0
    player_vy = 0
    PLAYER_SPEED = 6
    JUMP_STRENGTH = -8
    on_ground = True

    # --- CPU setup ---
    CPU_RADIUS = 80
    cpu_x = 3 * WIDTH // 4
    cpu_y = HEIGHT - GROUND_HEIGHT - (CPU_RADIUS * 2)
    CPU_SPEED = 2
    cpu_vy = 0
    cpu_on_ground = True
    CPU_JUMP_STRENGTH = -8

    # Load images
    player_image = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\player.png"
    ).convert_alpha()
    player_image = pygame.transform.scale(player_image, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
    cpu_image = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\cpu.png"
    ).convert_alpha()
    cpu_image = pygame.transform.scale(cpu_image, (CPU_RADIUS * 2, CPU_RADIUS * 2))

    # Masks for pixel-perfect collision
    player_mask = pygame.mask.from_surface(player_image)
    cpu_mask = pygame.mask.from_surface(cpu_image)

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
    player_score = 0
    cpu_score = 0
    font = pygame.font.SysFont(None, 40)
    WIN_SCORE = 7

    # Floating +1 points
    floating_points = []  # Each element: [x, y, surface, alpha]

    # Custom font for winner
    font_path = r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\fonts\1.ttf"

    # Game loop
    clock = pygame.time.Clock()
    running = True
    paused = False

    # Buttons for pause menu
    button_font = pygame.font.SysFont(None, 40)
    pause_buttons = {
        "Resume": pygame.Rect(WIDTH//2-100, 200, 200, 50),
        "Quit": pygame.Rect(WIDTH//2-100, 300, 200, 50)
    }

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Toggle pause
                    paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                mx, my = pygame.mouse.get_pos()
                if pause_buttons["Resume"].collidepoint(mx, my):
                    paused = False
                if pause_buttons["Quit"].collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        if paused:
            # Draw pause overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,150))
            screen.blit(overlay, (0,0))
            for text, rect in pause_buttons.items():
                color = BUTTON_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
                shadow = rect.copy()
                shadow.x += 5
                shadow.y += 5
                pygame.draw.rect(screen, BUTTON_SHADOW, shadow, border_radius=15)
                pygame.draw.rect(screen, color, rect, border_radius=15)
                pygame.draw.rect(screen, (255,255,255), rect, 3, border_radius=15)
                label = button_font.render(text, True, (255,255,255))
                screen.blit(label, label.get_rect(center=rect.center))
            pygame.display.flip()
            continue

        # --- PLAYER CONTROLS ---
        keys = pygame.key.get_pressed()
        player_vx = 0
        if keys[pygame.K_LEFT]:
            player_vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_vx = PLAYER_SPEED
        if keys[pygame.K_UP] and on_ground:
            player_vy = JUMP_STRENGTH
            on_ground = False

        # Apply gravity
        player_vy += GRAVITY
        player_y += player_vy
        player_x += player_vx
        cpu_vy += GRAVITY
        cpu_y += cpu_vy

        # Ground collisions
        if player_y + PLAYER_RADIUS * 2 >= HEIGHT - GROUND_HEIGHT:
            player_y = HEIGHT - GROUND_HEIGHT - PLAYER_RADIUS * 2
            player_vy = 0
            on_ground = True
        if cpu_y + CPU_RADIUS * 2 >= HEIGHT - GROUND_HEIGHT:
            cpu_y = HEIGHT - GROUND_HEIGHT - CPU_RADIUS * 2
            cpu_vy = 0
            cpu_on_ground = True

        # Keep player inside left half
        if player_x - PLAYER_RADIUS < 0:
            player_x = PLAYER_RADIUS
        if player_x + PLAYER_RADIUS > WIDTH // 2 - 15:
            player_x = WIDTH // 2 - 15 - PLAYER_RADIUS

        # CPU auto movement
        if ball_x > WIDTH // 2:
            if ball_x < cpu_x:
                cpu_x -= CPU_SPEED
            elif ball_x > cpu_x:
                cpu_x += CPU_SPEED
            if cpu_on_ground and abs(ball_x - cpu_x) < 120 and ball_y < cpu_y:
                cpu_vy = CPU_JUMP_STRENGTH
                cpu_on_ground = False

        if cpu_x - CPU_RADIUS < WIDTH // 2 + 15:
            cpu_x = WIDTH // 2 + 15 + CPU_RADIUS
        if cpu_x + CPU_RADIUS > WIDTH:
            cpu_x = WIDTH - CPU_RADIUS

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
                cpu_score += 1
                text_surf = font.render("+1", True, SCORE_COLOR_CPU)
                floating_points.append([WIDTH*3//4, HEIGHT//2 - 100, text_surf, 255])
            else:
                player_score += 1
                text_surf = font.render("+1", True, SCORE_COLOR_PLAYER)
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
        player_pos = (int(player_x - PLAYER_RADIUS), int(player_y))
        cpu_pos = (int(cpu_x - CPU_RADIUS), int(cpu_y))
        ball_pos = (int(ball_x - BALL_RADIUS), int(ball_y - BALL_RADIUS))

        offset_player = (ball_pos[0] - player_pos[0], ball_pos[1] - player_pos[1])
        offset_cpu = (ball_pos[0] - cpu_pos[0], ball_pos[1] - cpu_pos[1])

        if player_mask.overlap(ball_mask, offset_player):
            ball_vy = -abs(ball_vy) - 3
            ball_vx += (ball_x - player_x) / PLAYER_RADIUS * 3
            hit_sound.play()
        if cpu_mask.overlap(ball_mask, offset_cpu):
            ball_vy = -abs(ball_vy) - 3
            ball_vx += (ball_x - cpu_x) / CPU_RADIUS * 3
            hit_sound.play()

        # --- DRAW ---
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, NET_COLOR, net_rect)
        screen.blit(player_image, player_pos)
        screen.blit(cpu_image, cpu_pos)
        screen.blit(ball_image, ball_pos)

        # Draw floating points
        for fp in floating_points[:]:
            x, y, surf, alpha = fp
            surf.set_alpha(alpha)
            screen.blit(surf, (x - surf.get_width()//2, y))
            fp[1] -= 1  # move up
            fp[3] -= 5  # fade out
            if fp[3] <= 0:
                floating_points.remove(fp)

        # Scoreboard
        score_font = pygame.font.SysFont(None, 60)
        player_text = score_font.render(f"Player: {player_score}", True, SCORE_COLOR_PLAYER)
        cpu_text = score_font.render(f"CPU: {cpu_score}", True, SCORE_COLOR_CPU)
        screen.blit(player_text, (50, 20))
        screen.blit(cpu_text, (WIDTH - cpu_text.get_width() - 50, 20))

        # --- WIN CONDITION POPUP ---
        winner = None
        if player_score >= WIN_SCORE:
            winner = "Player"
        elif cpu_score >= WIN_SCORE:
            winner = "CPU"

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
                        if post_win_buttons["Play Again"].collidepoint(mx,my):
                            # Reset everything
                            player_score = cpu_score = 0
                            ball_x, ball_y = WIDTH//2, 100
                            ball_vx, ball_vy = 4,0
                            player_x, player_y = WIDTH//4, HEIGHT-GROUND_HEIGHT-PLAYER_RADIUS*2
                            cpu_x, cpu_y = 3*WIDTH//4, HEIGHT-GROUND_HEIGHT-CPU_RADIUS*2
                            player_vx=player_vy=cpu_vy=0
                            on_ground=cpu_on_ground=True
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
