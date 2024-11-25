import pygame as pg
import os
from pygame.locals import *
from Game import * 

square_size = 50
board_size = 10  # 10x10 grid

grid_width = square_size * board_size
grid_height = square_size * board_size

# Calculate the top-left corner to center the grid
center_x = (1024 - grid_width) // 2
center_y = (768 - grid_height) // 2

# Initialize board state
board_state = [['default' for _ in range(board_size)] for _ in range(board_size)]


# Function to draw the game board
def draw_board(board_state, screen):
    # Draw each square in the grid
    for row in range(board_size):
        for col in range(board_size):
            color = (255, 255, 255) if board_state[row][col] == 'default' else (255, 0, 0)  # default or clicked color
            pg.draw.rect(screen, color, (center_x + col * square_size, center_y + row * square_size, square_size, square_size))
            pg.draw.rect(screen, (0, 0, 0), (center_x + col * square_size, center_y + row * square_size, square_size, square_size), 2)  # Grid lines


# Function to handle a mouse click on the grid
def handle_click(x, y):
    # Calculate which square was clicked
    col = (x - center_x) // square_size
    row = (y - center_y) // square_size

    # Check if the click is within the bounds of the grid
    if 0 <= col < board_size and 0 <= row < board_size:
        print(f"Clicked on square: Row {row}, Col {col}")  # Debugging line
        # Toggle the color of the clicked square
        if board_state[row][col] == 'default':
            board_state[row][col] = 'clicked'
        else:
            board_state[row][col] = 'default'
    else:
        print("Clicked outside the grid.")  # Debugging line


# Game loop to play the game
def play_game(screen):
    # Initialize Pygame
    pg.init()

    # Set the name of the display
    pg.display.set_caption("BATTLESHIP GAMEPLAY")

    # Game variables
    game_running = True

    # Game loop
    while game_running:
        # Clear the screen
        screen.fill((255, 255, 255))

        for event in pg.event.get():
            if event.type == QUIT:
                game_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    handle_click(event.pos[0], event.pos[1])

        # Draw the board
        draw_board(board_state, screen)

        # Update the display
        pg.display.flip()

    pg.quit()


# Start screen
def main():
    # Initialize Pygame
    pg.init()

    # Set the name of the display
    pg.display.set_caption("BATTLESHIP START SCREEN")

    battleship_icon_path = os.path.join('assets', 'battleship_icon.jpg')
    battleship_icon = pg.image.load(battleship_icon_path)
    # Set the icon of the display
    pg.display.set_icon(battleship_icon)

    # Create a screen object
    screen = pg.display.set_mode([1024, 768])

    start_gif_folder = "assets/battleship_start_gif"
    frames = [pg.image.load(os.path.join(start_gif_folder, frame_name)) for frame_name in os.listdir(start_gif_folder)]

    # Resize frames to fit the screen
    frames = [pg.transform.scale(frame, (1024, 768)) for frame in frames]

    battleship_logo_path = os.path.join('assets', 'battleship_logo.png')
    battleship_logo = pg.image.load(battleship_logo_path)

    # Resize logo
    logo_width, logo_height = 500, 175
    battleship_logo = pg.transform.scale(battleship_logo, (logo_width, logo_height))

    logo_x = 10
    logo_y = 10

    font_path = os.path.join("assets", "USAAF_FONT", "USAAF_Stencil.ttf")

    # Setup text
    font = pg.font.Font(font_path, 50)  # default font, size 50
    text_color = (255, 255, 255)  # white text
    text = font.render("Press SPACE to start", True, text_color)

    text_x = (1024 - text.get_width()) // 2
    text_y = 600

    # Frame rate for the animation
    fps = 9
    clock = pg.time.Clock()

    frame_index = 0

    blink_interval = 950  # Blink every 950 milliseconds
    last_blink_time = pg.time.get_ticks()
    show_text = True

    game_running = True

    while game_running:
        current_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == QUIT:
                game_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_running = False
                if event.key == K_SPACE:
                    play_game(screen)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Display the current frame
        screen.blit(frames[frame_index], (0, 0))

        # Display the battleship logo over top
        screen.blit(battleship_logo, (logo_x, logo_y))

        if current_time - last_blink_time > blink_interval:
            show_text = not show_text
            last_blink_time = current_time

        if show_text:
            # Display the start text
            screen.blit(text, (text_x, text_y))

        # Update the display
        pg.display.flip()

        # Advance to the next frame
        frame_index = (frame_index + 1) % len(frames)

        # Control the frame rate
        clock.tick(fps)

    pg.quit()


if __name__ == "__main__":
    main()