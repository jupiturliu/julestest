# snake_game.py
# A simple implementation of the Greedy Snake game using Pygame.

import pygame
import random

# Define screen dimensions
screen_width = 600
screen_height = 400

# Initialize Pygame
pygame.init() # Initializes all the Pygame modules.

# Create the game display surface
screen = pygame.display.set_mode((screen_width, screen_height)) # Sets the window size.

# Set window title
pygame.display.set_caption("Greedy Snake") # Sets the title of the game window.

# Define colors (RGB tuples)
black = (0, 0, 0)         # Background color
white = (255, 255, 255)   # Text color / Score color
red = (213, 50, 80)       # Food color
green = (0, 255, 0)       # Snake color

# Define game parameters
snake_block_size = 10     # Size of each snake segment and food item (in pixels).
initial_snake_speed = 15  # Initial speed of the snake (frames per second).

# Define font styles
font_style = pygame.font.SysFont(None, 30)        # Font for score display.
message_font_style = pygame.font.SysFont(None, 50) # Font for game over messages.

# Snake Class: Manages the snake's properties, movement, and drawing.
class Snake:
    # __init__: Initializes the snake's properties.
    # Parameters:
    #   window_width: Width of the game window.
    #   window_height: Height of the game window.
    #   block_size: Size of one snake block.
    def __init__(self, window_width, window_height, block_size):
        self.block_size = block_size
        self.window_width = window_width
        self.window_height = window_height
        self.reset() # Set initial state

    # reset: Resets the snake to its initial state.
    # Sets position to center, clears movement, and sets length to 1.
    def reset(self):
        # Initial position in the middle of the screen
        self.x = self.window_width / 2
        self.y = self.window_height / 2
        # Initial movement direction (stationary)
        self.x_change = 0
        self.y_change = 0
        # Snake body as a list of [x, y] coordinates for each segment
        self.body = []
        self.length = 1 # Initial length (head only)

    # draw: Draws the snake on the game display.
    # Iterates through the snake's body segments and draws a rectangle for each.
    # Parameters:
    #   game_display: The Pygame display surface to draw on.
    #   color: The color to draw the snake.
    def draw(self, game_display, color):
        for segment in self.body:
            pygame.draw.rect(game_display, color, [segment[0], segment[1], self.block_size, self.block_size])

    # move: Updates the snake's position and body.
    # Adds a new head segment in the direction of movement and removes the tail if not growing.
    def move(self):
        self.x += self.x_change
        self.y += self.y_change

        # Update snake body by adding the new head position
        snake_head = []
        snake_head.append(self.x)
        snake_head.append(self.y)
        self.body.append(snake_head)

        # If the snake's body is longer than its current length, remove the oldest segment (tail)
        if len(self.body) > self.length:
            del self.body[0]

    # change_direction: Updates the snake's movement direction based on key press.
    # Prevents the snake from immediately reversing its direction.
    # Parameters:
    #   event: The Pygame event object (specifically a KEYDOWN event).
    def change_direction(self, event):
        if event.key == pygame.K_LEFT:
            # Prevent immediate reversal of direction
            if self.x_change == self.block_size: # If moving right, don't allow left
                return
            self.x_change = -self.block_size
            self.y_change = 0
        elif event.key == pygame.K_RIGHT:
            if self.x_change == -self.block_size: # If moving left, don't allow right
                return
            self.x_change = self.block_size
            self.y_change = 0
        elif event.key == pygame.K_UP:
            if self.y_change == self.block_size: # If moving down, don't allow up
                return
            self.y_change = -self.block_size
            self.x_change = 0
        elif event.key == pygame.K_DOWN:
            if self.y_change == -self.block_size: # If moving up, don't allow down
                return
            self.y_change = self.block_size
            self.x_change = 0

    # grow: Increases the length of the snake.
    # Called when the snake eats food.
    def grow(self):
        self.length += 1

    # check_collision_with_self: Checks if the snake's head has collided with its body.
    # Returns: True if collision occurs, False otherwise.
    def check_collision_with_self(self):
        # Check if the snake's head coordinates match any other segment in its body
        snake_head = [self.x, self.y]
        # Exclude the head itself from the check (last element of self.body)
        for segment in self.body[:-1]:
            if segment == snake_head:
                return True
        return False

    # check_collision_with_walls: Checks if the snake has collided with the game window boundaries.
    # Returns: True if collision occurs, False otherwise.
    def check_collision_with_walls(self):
        if self.x >= self.window_width or self.x < 0 or self.y >= self.window_height or self.y < 0:
            return True
        return False

# Food Class: Manages the food's properties, spawning, and drawing.
class Food:
    # __init__: Initializes the food's properties.
    # Parameters:
    #   window_width: Width of the game window.
    #   window_height: Height of the game window.
    #   block_size: Size of the food item.
    #   snake_body: List of snake's body segments to avoid spawning food on the snake.
    def __init__(self, window_width, window_height, block_size, snake_body=None):
        self.window_width = window_width
        self.window_height = window_height
        self.block_size = block_size
        # Store snake's body to avoid spawning food on it
        self.snake_body = snake_body if snake_body is not None else []
        self.x = 0 # Food x-coordinate
        self.y = 0 # Food y-coordinate
        self.spawn() # Place the food at an initial random position.

    # spawn: Places the food at a random position on the screen.
    # Ensures that the food does not spawn on a part of the snake's body.
    def spawn(self):
        # Keep generating new positions until it's not inside the snake's body
        while True:
            # Generate random x, y coordinates, aligned to the block grid
            self.x = round(random.randrange(0, self.window_width - self.block_size) / self.block_size) * self.block_size
            self.y = round(random.randrange(0, self.window_height - self.block_size) / self.block_size) * self.block_size
            # Check if the generated position overlaps with the snake's body
            if [self.x, self.y] not in self.snake_body:
                break # Valid position found

    # draw: Draws the food on the game display.
    # Parameters:
    #   game_display: The Pygame display surface to draw on.
    #   color: The color to draw the food.
    def draw(self, game_display, color):
        pygame.draw.rect(game_display, color, [self.x, self.y, self.block_size, self.block_size])

    # update_snake_body: Updates the food's knowledge of the snake's body.
    # Purpose: To ensure food doesn't spawn on the snake after the snake has moved or grown.
    # Parameters:
    #   snake_body: The current list of the snake's body segments.
    def update_snake_body(self, snake_body):
        self.snake_body = snake_body

# display_score: Renders and displays the current score on the screen.
# Parameters:
#   score: The current score to display.
#   game_display: The Pygame display surface.
#   font_style: The font used to render the score.
#   color: The color of the score text.
#   position: A list [x, y] defining the top-left corner for the score text.
def display_score(score, game_display, font_style, color, position):
    value = font_style.render("Your Score: " + str(score), True, color)
    game_display.blit(value, position)

# game_over_screen: Displays the game over message and options to play again or quit.
# Purpose: Handles the UI and logic when the game ends.
# How it works: Fills the screen, shows "Game Over!", final score, and options.
#               Waits for user input (Q to quit, C to play again).
# Returns: True if the player chooses to play again, False if they choose to quit.
# Parameters:
#   game_display: The Pygame display surface.
#   score: The final score achieved by the player.
#   current_font_style: The font style for messages (unused here, uses global message_font_style).
#   clock: Pygame clock object to control frame rate.
#   game_over_bg_color: Background color for the game over screen.
#   text_color: Color for the text messages.
#   window_width: Width of the game window.
#   window_height: Height of the game window.
def game_over_screen(game_display, score, current_font_style, clock, game_over_bg_color, text_color, window_width, window_height):
    game_display.fill(game_over_bg_color) # Fill screen with background color
    
    # Display "Game Over!" message
    msg_game_over = message_font_style.render("Game Over!", True, text_color) 
    msg_game_over_rect = msg_game_over.get_rect(center=(window_width / 2, window_height / 3))
    game_display.blit(msg_game_over, msg_game_over_rect)

    # Display final score
    display_score(score, game_display, font_style, text_color, [window_width / 2 - 70, window_height / 2]) # Adjust position as needed

    # Display options message with controls
    msg_options_text = "Controls: Arrows = Move | C = Play Again | Q = Quit"
    msg_options = font_style.render(msg_options_text, True, text_color) 
    msg_options_rect = msg_options.get_rect(center=(window_width / 2, window_height * 2 / 3))
    game_display.blit(msg_options, msg_options_rect)
    
    pygame.display.update() # Update the full display

    # Event loop for game over screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False # Player chose to Quit
                if event.key == pygame.K_c:
                    return True # Player chose to Play Again
            if event.type == pygame.QUIT: # Allow quitting via window close button
                return False 
        clock.tick(5) # Keep the event loop responsive without maxing out CPU

# gameLoop: Main function to run the Greedy Snake game.
# Purpose: Contains the primary game logic, event handling, and rendering loop.
def gameLoop():
    # Initialization of game state variables
    game_over = False  # Flag to control the main game loop (True when player quits entirely)
    game_close = False # Flag to indicate a single game session has ended (e.g., collision)

    clock = pygame.time.Clock() # Pygame clock for controlling game speed
    
    # Create snake and food objects using global screen dimensions and block size
    player_snake = Snake(screen_width, screen_height, snake_block_size)
    # Initialize food, passing the snake's initial (empty) body to avoid spawning on it
    current_food = Food(screen_width, screen_height, snake_block_size, player_snake.body)
    
    score = 0 # Player's score

    # Main game loop: continues as long as game_over is False
    while not game_over:
        # Game over/play again handling section
        if game_close: # True if a game-ending condition (collision) occurred in the previous iteration
            # Show game over screen and get user choice (play again or quit)
            if game_over_screen(screen, score, message_font_style, clock, black, white, screen_width, screen_height):
                # User chose to Play Again: Reset game state
                player_snake.reset()
                current_food.update_snake_body(player_snake.body) # Update with empty body before spawn
                current_food.spawn()
                score = 0
                game_close = False # Reset for the new game session
            else:
                # User chose to Quit
                game_over = True # Exit the main game loop
            continue # Skip the rest of the current game loop iteration if game_close was true

        # Event handling section: processes user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Player clicked the window close button
                game_over = True
            if event.type == pygame.KEYDOWN: # Player pressed a key
                player_snake.change_direction(event) # Update snake direction

        # Game logic section
        player_snake.move() # Update snake's position

        # Check for eating food
        if player_snake.x == current_food.x and player_snake.y == current_food.y:
            player_snake.grow() # Make snake longer
            # Update food's knowledge of snake's body *before* spawning new food
            current_food.update_snake_body(player_snake.body)
            current_food.spawn() # Spawn new food
            score += 1 # Increase score

        # Check for collisions (game ending conditions)
        if player_snake.check_collision_with_walls() or player_snake.check_collision_with_self():
            game_close = True # Set flag to trigger game over screen in the next iteration

        # Drawing section: renders all game elements to the screen
        screen.fill(black) # Fill background
        current_food.draw(screen, red) # Draw food
        player_snake.draw(screen, green) # Draw snake
        display_score(score, screen, font_style, white, [0, 0]) # Draw score at top-left

        pygame.display.update() # Update the full display surface
        
        # Game speed control: snake speed increases with score
        clock.tick(initial_snake_speed + score // 5) # Increase speed for every 5 points

    # End of game loop (game_over is True)
    pygame.quit() # De-initialize Pygame modules
    quit()        # Exit the Python script

# Start the game by calling the main game loop function
gameLoop()
