import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
GRAVITY = 0.5
FLAP_POWER = -8
PIPE_SPEED = 3
PIPE_GAP = 200  # Adjusted the gap between pipes to make it easier
BIRD_X = 30

# Load images
bird_img = pygame.image.load('Assets/flappy-bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 50))  # Resize the bird image if necessary

bg_img = pygame.image.load('Assets/fp-bg.jpg')
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the background to fit the screen

# Screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Font for text display
font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
                return True
        return False

# Bird class
class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_POWER

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, bird_img.get_width(), bird_img.get_height())

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)  # Adjusted the height range for better gameplay
        self.width = 60

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, self.width, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, self.width, self.height),
            pygame.Rect(self.x, self.height + PIPE_GAP, self.width, SCREEN_HEIGHT - self.height - PIPE_GAP)
        ]

# Front screen function
def show_front_screen():
    play_button = Button("Play", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50, GREEN, BLUE)
    running = True
    while running:
        screen.blit(bg_img, (0, 0))
        play_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if play_button.is_clicked():
            running = False

        pygame.display.flip()
        clock.tick(30)

# Game over screen function
def show_game_over_screen(score):
    screen.fill(BLACK)  # Fill the screen with black for better visibility of buttons
    screen.blit(bg_img, (0, 0))  # Draw the background image

    # Display the score
    game_over_text = font.render(f'Game Over! Your Score: {score}', True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(game_over_text, game_over_rect)

    # Create buttons
    button_width = 130
    button_height = 50
    play_again_button = Button("Play Again", SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2 - 10, button_width, button_height, GREEN, BLACK)
    quit_button = Button("Quit", SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height // 2 + 10, button_width, button_height, GREEN, BLACK)

    play_again_button.draw()
    quit_button.draw()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if play_again_button.is_clicked():
            running = False
            return True  # Return True to indicate restarting the game

        if quit_button.is_clicked():
            pygame.quit()
            exit()

        pygame.display.flip()
        clock.tick(30)

# Game loop
def game_loop():
    while True:  # Main loop to allow restarting the game
        bird = Bird()
        pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
        score = 0
        running = True
        paused = False

        # Create a pause button
        pause_button = Button("Pause", SCREEN_WIDTH - 80, 10, 70, 30, GREEN, BLACK)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()
                    if event.key == pygame.K_p:  # Press 'P' to pause or unpause
                        paused = not paused

            if not paused:
                bird.update()

                # Draw background
                screen.blit(bg_img, (0, 0))

                # Draw bird
                bird.draw()

                for pipe in pipes:
                    pipe.update()
                    pipe.draw()

                    if pipe.x + pipe.width < 0:
                        pipes.remove(pipe)
                        pipes.append(Pipe(SCREEN_WIDTH))
                        score += 1

                    if bird.get_rect().collidelist(pipe.get_rects()) != -1:
                        running = False

                if bird.y > SCREEN_HEIGHT or bird.y < 0:
                    running = False

            # Draw the pause button
            pause_button.draw()

            # Render and display the score
            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))  # Display score at the top-left corner

            # Update the screen
            pygame.display.flip()
            clock.tick(30)

        # Show the game over screen and decide whether to restart or quit
        if not show_game_over_screen(score):
            break  # Exit the main loop to quit the game

# Run the front screen first, then the game loop
show_front_screen()
game_loop()
