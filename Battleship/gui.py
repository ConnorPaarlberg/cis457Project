import pygame as pg
import os
import colors
from pygame.locals import *
from enum import Enum

class GameState(Enum):
    START_SCREEN = 1
    MAIN_GAME = 2
    GAME_OVER = 3

class Gui:
  def __init__(self):
    # initialize pygame
    pg.init()

    # set the name of the display
    pg.display.set_caption("BATTLESHIP")

    # dimensions of the display
    self.dimensions = [1024, 768]

    # create a screen object
    self.screen = pg.display.set_mode(self.dimensions)

    # paths for relevant assets
    self.battleship_icon_path = os.path.join("Battleship",'assets', 'battleship_icon.jpg')
    self.battleship_logo_path = os.path.join('Battleship', 'assets', 'battleship_logo.png')
    self.font_path = os.path.join("Battleship", "assets", "USAAF_FONT", "USAAF_Stencil.ttf")
    self.start_screen_gif_path = os.path.join("Battleship", "assets", "battleship_start_gif")

    # load the assets
    self.battleship_icon = pg.image.load(self.battleship_icon_path)
    self.battleship_logo = pg.image.load(self.battleship_logo_path)
    self.font = pg.font.Font(self.font_path, 50)
    self.start_screen_frames = [pg.image.load(os.path.join(self.start_screen_gif_path, frame_name))
                                for frame_name in os.listdir(self.start_screen_gif_path)]
    
    # resize the start screen frames to fit the screen
    self.start_screen_frames = [pg.transform.scale(frame, self.dimensions) for frame in self.start_screen_frames]
    # resize the logo
    self.battleship_logo = pg.transform.scale(self.battleship_logo, (500, 175))

    # set the icon of the display
    pg.display.set_icon(self.battleship_icon)

    self.game_state = GameState.START_SCREEN
    self.game_running = True

  def display_start_screen(self):
    clock = pg.time.Clock() # create a clock (for the blinking text)

    current_time = pg.time.get_ticks() # the current time (using our clock)
    last_blink_time = pg.time.get_ticks() # the last time the text has blinked
    blink_interval = 950 # the interval of blinks (in ms)

    frame_index = 0 # the current frame in the gif
    fps = 9 # the desired fps of the startup gif
    
    startup_text = self.font.render("Press SPACE to start", True, colors.white)
    text_visible = True # text starts as visible
    
    while self.game_state == GameState.START_SCREEN:
      for event in pg.event.get():
        if event.type == QUIT:
          self.game_running = False
          self.game_state = None

        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.game_running = False
            self.game_state = None

          elif event.key == K_SPACE:
            self.game_state = GameState.MAIN_GAME

      # clear the screen
      self.screen.fill((0,0,0))

      self.screen.blit(self.start_screen_frames[frame_index], (0,0)) # display the current frame
      self.screen.blit(self.battleship_logo, (10, 10))  # display the battleship logo over top

      if current_time - last_blink_time > blink_interval:
        show_text = not show_text
        last_blink_time = current_time

      if text_visible:
        # display the start text
        self.screen.blit(startup_text, ((1024 - startup_text.get_width()) // 2, 600))

      # update the display
      pg.display.flip()

      # Advance to the next frame
      frame_index = (frame_index + 1) % len(self.start_screen_frames)

      # control the frame rate
      clock.tick(fps)
    
  def display_gameplay(self):
    GRID_SIZE = 10 # 10x10 grid
    SQUARE_SIZE = 50 # the size of each square
    BOARD_DIMENSION = GRID_SIZE * SQUARE_SIZE

    background_image_path = os.path.join("Battleship", "assets", "black_background.png")
    background_image = pg.image.load(background_image_path)
    background_image = pg.transform.scale(background_image, self.dimensions)

    battleship_icon_path = os.path.join("Battleship", "assets", "battleship_logo2.png")
    battleship_icon = pg.image.load(battleship_icon_path)
    battleship_icon = pg.transform.scale(battleship_icon, (500, 125))

    icon_rect = self.battleship_icon.get_rect()
    icon_rect.center = (530, 270)

    game_board = pg.Rect(0, 0,  BOARD_DIMENSION, BOARD_DIMENSION)

    start_x = (self.dimensions[0] - BOARD_DIMENSION) // 2
    start_y = (self.dimensions[1] - BOARD_DIMENSION) // 2

    selected_row = 0
    selected_col = 0

    while self.game_state == GameState.MAIN_GAME:
      for event in pg.event.get():
        if event.type == QUIT:
          self.game_running = False
          self.game_state = None

        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.game_running = False
            self.game_state = None

          elif event.key == K_UP:
             selected_row = max(0, selected_row - 1)
          elif event.key == K_DOWN:
             selected_row = min(GRID_SIZE - 1, selected_row + 1)
          elif event.key == K_LEFT:
             selected_col = max(0, selected_col - 1)
          elif event.key == K_RIGHT:
             selected_col = min(GRID_SIZE - 1, selected_col + 1)
        
        elif event.type == MOUSEBUTTONDOWN:
          if event.button == 1: # the left mouse button was clicked
            mouse_x, mouse_y = pg.mouse.get_pos()

            if (start_x <= mouse_x <= start_x + BOARD_DIMENSION) and \
              (start_y <= mouse_y <= start_y + BOARD_DIMENSION):
              col = (mouse_x - start_x) // SQUARE_SIZE
              row = (mouse_y - start_y) // SQUARE_SIZE
              selected_col = col
              selected_row = row
              print(f"Clicked on square at row {row}, column {col}")

      # clear the screen
      self.screen.fill((0,0,0))

      # draw the background image
      self.screen.blit(background_image, (0,0))

      # draw the battleship logo
      self.screen.blit(battleship_icon, icon_rect)

      # draw the battleship grid
      for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pg.Rect(start_x + col * SQUARE_SIZE, start_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(self.screen, (255, 255, 255),
                             rect, 2)

                if row == selected_row and col == selected_col:
                   pg.draw.rect(self.screen, (255, 255, 0), rect, 4)


      # update the display
      pg.display.flip()

  def run(self):
    while self.game_running:
      if self.game_state == GameState.START_SCREEN:
        self.display_start_screen()
      elif self.game_state == GameState.MAIN_GAME:
        self.display_gameplay()
      elif self.game_state == GameState.GAME_OVER:
        pass

    pg.quit()

def main():
  gui = Gui()
  gui.run()

if __name__ == "__main__":
    main()