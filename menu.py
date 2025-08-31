import pygame
import sys
import math
from sPlayer import play_game as single_game
from mPlayer import play_game as multi_game

# Colors
WHITE = (255, 255, 0)
RED = (200, 50, 50)
YELLOW = (0, 200, 200)
SHADOW_COLOR = (220, 220, 20)
WIDTH, HEIGHT = 800, 600
button_font = None
menu_background = None

# Button class (same as before)
class Button:
    def __init__(self, text, x, y, w, h, action=None, delay=0, animated=False):
        self.text = text
        self.final_rect = pygame.Rect(x, y, w, h)
        self.rect = pygame.Rect(x, HEIGHT + 100, w, h)
        self.action = action
        self.hovered = False
        self.appear_time = delay
        self.animation_done = False
        self.animated = animated

    def update(self, start_time):
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed > self.appear_time and not self.animation_done:
            speed = 10
            if self.rect.y > self.final_rect.y:
                self.rect.y -= speed
            else:
                self.rect.y = self.final_rect.y
                self.animation_done = True

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse)
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=15)

        if self.animated:
            t = pygame.time.get_ticks() / 350
            pulse = (math.sin(t) + 1) / 2
            base_color = (
                int(RED[0] * (1 - pulse) + 10 * pulse),
                int(RED[1] * (1 - pulse) + 200 * pulse),
                int(RED[2] * (1 - pulse) + 200 * pulse)
            )
            hover_color = (0, 200, 200)
            color = hover_color if self.hovered else base_color
        else:
            color = YELLOW if self.hovered else RED

        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, self.rect, width=3, border_radius=15)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        if self.action:
            return self.action()
        return None

# -------------------------
# Actions
# -------------------------
def start_game_action(mode):
    pygame.mixer.music.stop()
    if mode == "single":
        single_game()
    else:
        multi_game()

def game_settings():
    print("Game Settings clicked!")

def mute_sound():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        print("Music paused")
    else:
        pygame.mixer.music.unpause()
        print("Music resumed")

def back_to_home():
    return "back"

# -------------------------
# Function to run menu in same window
# -------------------------
def run_menu_screen(mode, screen):
    global button_font, menu_background
    pygame.font.init()
    button_font = pygame.font.SysFont("comicsansms", 30)

    # Load menu background
    menu_background = pygame.image.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\menu.jpg"
    )
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # Load and play background music
    pygame.mixer.music.load(
        r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\sounds\background.mp3"
    )
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Setup buttons
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    buttons = [
        Button("Start", WIDTH//2 - 120, 250, 240, 50, lambda: start_game_action(mode), delay=0.75, animated=True),
        Button("Game Settings", WIDTH//2 - 150, 320, 300, 50, game_settings, delay=1.5),
        Button("Mute", WIDTH//2 - 120, 390, 240, 50, mute_sound, delay=2.25),
        Button("Back", WIDTH//2 - 120, 460, 240, 50, back_to_home, delay=3),
        Button("Quit", WIDTH//2 - 120, 530, 240, 50, sys.exit, delay=3.75)
    ]

    # Menu loop
    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        for button in buttons:
            button.update(start_time)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.hovered:
                        result = button.click()
                        if result == "back":
                            running = False  # exit menu loop, return to home

        pygame.display.flip()
        clock.tick(60)

# -------------------------
# Optional: run standalone
# -------------------------
if __name__ == "__main__":
    run_menu_screen("single", pygame.display.get_surface())
