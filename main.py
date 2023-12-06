# Snake game
# matthew watters
import pygame
from pygame import mixer
import random
pygame.init()

# Constants
screen_width, screen_height = 800, 600
grid_size = 20
FPS = 10

# Score
score = 0

# Colors
white = (255, 255, 255)
black = (0,0,0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Creating the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')



# snake and apple classes
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([grid_size, grid_size])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width / 2, screen_height / 2)
        self.segments = [(self.rect.x, self.rect.y)]
        self.speed = grid_size


    def update(self):
        # Update the character's position

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            snake.rect.x += self.speed
        if keys[pygame.K_UP]:
            snake.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            snake.rect.y += self.speed

        # wrap around the screen
        if self.rect.right < 0:
            self.rect.left = screen_width
        if self.rect.left > screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = screen_height
        if self.rect.top > screen_height:
            self.rect.bottom = 0

        self.segments.insert(0, (self.rect.x, self.rect.y))
        if len(self.segments) > score + 1:  # Adjusting segments based on the score
            self.segments.pop()

    def grow(self):
        self.segments.append(self.segments[-1])

    def draw(self, surface):
        for segment in self.segments:
            pygame.draw.rect(surface, blue, (segment[0], segment[1], grid_size, grid_size))


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([grid_size, grid_size])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.randomize()

    def randomize(self):
        self.rect.topleft = (random.randint(0, screen_width - grid_size),random.randint(0, screen_height - grid_size))

# function to displace game over screen
def display_play_again_screen():
    screen.fill(black)

    font = pygame.font.Font(None, 36)
    text = font.render("You hit the wall! Play again? (Y/N)", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.blit(text, text_rect)
    pygame.display.flip()


# Game variables
all_sprites = pygame.sprite.Group()
snake = Snake()
apple = Apple()

all_sprites.add(snake)
all_sprites.add(apple)

clock = pygame.time.Clock()
running = True

# add walls to game
bottom_rect = pygame.Rect(0, 580, screen_width, 1)
right_rect = pygame.Rect(screen_width - 20, 0, 20, screen_height)
top_rect = pygame.Rect(0,0, screen_width, 20)
left_rect = pygame.Rect(0, 0, 20, screen_height)

hit_wall = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Checking for collision between snake and walls
    if snake.rect.colliderect(bottom_rect) or snake.rect.colliderect(right_rect) or snake.rect.colliderect(
        left_rect) or snake.rect.colliderect(top_rect):
        hit_wall = True
        # Reset the snake's position and score
        snake.rect.topleft = (screen_width / 2, screen_height / 2)
        score = 0
        snake.segments = [(snake.rect.x, snake.rect.y)]

    if hit_wall:
        display_play_again_screen()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        hit_wall = False
                        waiting = False
                    elif event.key == pygame.K_n:
                        running = False
                        waiting = False

    # Checking for collision between snake and apple
    if pygame.sprite.collide_rect(snake,apple):
        apple.randomize()
        score += 1
        snake.grow()

    # checking for wall collisions
    if snake.rect.colliderect(bottom_rect) or snake.rect.colliderect(right_rect) or snake.rect.colliderect(
            left_rect) or snake.rect.colliderect(top_rect):
        # Reset the snake's position to the center
        snake.rect.topleft = (screen_width / 2, screen_height / 2)
        # Reset the score
        score = 0
        # Reset the snake's segments
        snake.segments = [(snake.rect.x, snake.rect.y)]

    # update sprites
    all_sprites.update()

    # creating the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(green)

    # rendering text
    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Score " + str(score), True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() - 100, y=10)
        background.blit(text, textpos)

    # Draw everything
    screen.fill(black)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    snake.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()