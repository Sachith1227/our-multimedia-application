import pygame
import sys

# Import menu.py functions
try:
    from menu import run_menu_screen   # menu.py must define this function
except ImportError:
    print("Error: menu.py not found or run_menu_screen function missing.")
    sys.exit(1)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volleyball Game - Home")

# Colors
WHITE = (255, 255, 0)
RED = (200, 50, 50)
YELLOW = (0, 200, 200)
SHADOW_COLOR = (220, 220, 20)

# Fonts
button_font = pygame.font.SysFont("comicsansms", 30)

# Load home background
home_background_path = r"C:\Users\CHAMA COMPUTERS\Desktop\ICT2210-Mini Project\VolleyballGame\assets\menu.jpg"
home_background = pygame.image.load(home_background_path)
home_background = pygame.transform.scale(home_background, (WIDTH, HEIGHT))

# Button class
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.hovered = False

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse)

        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=15)

        # Button color
        color = YELLOW if self.hovered else RED
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, self.rect, width=3, border_radius=15)

        # Button text
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        if self.action:
            self.action()

# Button actions
def single_player_action():
    run_menu_screen("single", screen)   # run inside same window

def multiplayer_action():
    run_menu_screen("multi", screen)    # run inside same window

# Run home menu
def run_home():
    clock = pygame.time.Clock()

    buttons = [
        Button("Single Player", WIDTH//2 - 150, 300, 300, 60, single_player_action),
        Button("Multiplayer", WIDTH//2 - 150, 400, 300, 60, multiplayer_action)
    ]

    running = True
    while running:
        screen.blit(home_background, (0, 0))

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.hovered:
                        button.click()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_home()
