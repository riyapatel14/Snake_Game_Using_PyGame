import pygame
import random

pygame.init()

# Set up the game window
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up the fonts
font_style = pygame.font.SysFont("helvetica", 30, 0, 1)
font_style2 = pygame.font.SysFont("helvetica", 50, 0, 1)

# Load sound effects (removed for simplicity)

# Define functions to manage high score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()

# Define the function to display the score
def display_score(score):
    score_text = font_style.render("Score: " + str(score), 1, "black")
    window.blit(score_text, [10, 10])

    # Display high score
    high_score_text = font_style.render("High Score: " + str(high_score), 1, "black")
    window.blit(high_score_text, [window_width - high_score_text.get_width() - 10, 10])

# Define function to display game over
def display_game_over():
    game_over_text = font_style2.render("GAME OVER", 1, "black")
    window.blit(game_over_text, (150, 225))
    pygame.display.flip()

    # Display instructions to restart
    restart_text = font_style.render("Press R to Restart", 1, "black")
    window.blit(restart_text, (160, 300))

# Reset game function
def reset_game():
    global snake_length, snake_list, snake_x, snake_y, snake_x_change, snake_y_change
    global food_x, food_y, high_score

    # Reset snake variables
    snake_list = []
    snake_length = 1
    snake_x = round((window_width / 2) / snake_block_size) * snake_block_size
    snake_y = round((window_height / 2) / snake_block_size) * snake_block_size
    snake_x_change = 0
    snake_y_change = 0

    # Reset food position
    food_on_snake = True
    while food_on_snake:
        food_x = round(random.randrange(0, window_width - food_block_size) / snake_block_size) * snake_block_size
        food_y = round(random.randrange(0, window_height - food_block_size) / snake_block_size) * snake_block_size
        food_on_snake = False
        for block in snake_list:
            if block[0] == food_x and block[1] == food_y:
                food_on_snake = True
                break

    # Update high score if necessary
    if snake_length - 1 > high_score:
        high_score = snake_length - 1
        save_high_score(high_score)

# Set up the snake
snake_block_size = 20
snake_speed = 15
snake_list = []
snake_length = 1
snake_x = round((window_width / 2) / snake_block_size) * snake_block_size
snake_y = round((window_height / 2) / snake_block_size) * snake_block_size
snake_x_change = 0
snake_y_change = 0

# Set up the food
food_block_size = 20
food_x = round(random.randrange(0, window_width - food_block_size) / snake_block_size) * snake_block_size
food_y = round(random.randrange(0, window_height - food_block_size) / snake_block_size) * snake_block_size

# Define the function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, "black", [x[0], x[1], snake_block_size, snake_block_size])

# Define the function to draw a gradient background
def draw_gradient_background():
    color1 = (144, 238, 144)  # light green
    color2 = (0, 128, 0)      # dark green
    for y in range(window_height):
        color = (
            color1[0] + (color2[0] - color1[0]) * y // window_height,
            color1[1] + (color2[1] - color1[1]) * y // window_height,
            color1[2] + (color2[2] - color1[2]) * y // window_height,
        )
        pygame.draw.line(window, color, (0, y), (window_width, y))

# Start the game loop
run = True
game_over = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
                game_over = False

    if not game_over:
        # Move the snake
        snake_x += snake_x_change
        snake_y += snake_y_change

        # Check for collision with the food
        if snake_x == food_x and snake_y == food_y:
            # Play eat sound (if desired, add back the sound effect code here)
            # eat_sound.play()
            # Generate a new position for the food
            food_on_snake = True
            while food_on_snake:
                food_x = round(random.randrange(0, window_width - food_block_size) / snake_block_size) * snake_block_size
                food_y = round(random.randrange(0, window_height - food_block_size) / snake_block_size) * snake_block_size
                food_on_snake = False
                for block in snake_list:
                    if block[0] == food_x and block[1] == food_y:
                        food_on_snake = True
                        break
            snake_length += 1

        # Update the snake list
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with the walls
        if snake_x < 0 or snake_x >= window_width or snake_y < 0 or snake_y >= window_height:
            game_over = True

        # Check for collision with the snake's body
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        # Draw the game objects
        draw_gradient_background()
        pygame.draw.rect(window, "green", [food_x, food_y, food_block_size, food_block_size])
        draw_snake(snake_block_size, snake_list)
        display_score(snake_length - 1)
        pygame.display.flip()

        # Set the game speed
        clock = pygame.time.Clock()
        clock.tick(snake_speed)

        # Get the user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake_x_change != snake_block_size:
            snake_x_change = -snake_block_size
            snake_y_change = 0
        elif keys[pygame.K_RIGHT] and snake_x_change != -snake_block_size:
            snake_x_change = snake_block_size
            snake_y_change = 0
        elif keys[pygame.K_UP] and snake_y_change != snake_block_size:
            snake_y_change = -snake_block_size
            snake_x_change = 0
        elif keys[pygame.K_DOWN] and snake_y_change != -snake_block_size:
            snake_y_change = snake_block_size
            snake_x_change = 0
    else:
        display_game_over()
        pygame.time.delay(1000)

pygame.quit()