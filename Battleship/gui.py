import pygame as pg
import os
from pygame.locals import *

def main():
  # Initialize Pygame
  pg.init()

  # Set the name of the display
  pg.display.set_caption("BATTLESHIP")
  
  battleship_icon_path = os.path.join("Battleship",'assets', 'battleship_icon.jpg')
  battleship_icon = pg.image.load(battleship_icon_path)
  # Set the icon of the display
  pg.display.set_icon(battleship_icon)

  # Create a screen object
  screen = pg.display.set_mode([1024, 768])

  start_gif_folder = "Battleship/assets/battleship_start_gif"
  frames = [pg.image.load(os.path.join(start_gif_folder, frame_name)) for frame_name in os.listdir(start_gif_folder)]

  # Resize frames to fit the screen
  frames = [pg.transform.scale(frame, (1024, 768)) for frame in frames] 

  battleship_logo_path = os.path.join('Battleship', 'assets', 'battleship_logo.png')
  battleship_logo = pg.image.load(battleship_logo_path)

  # resize logo
  logo_width, logo_height = 500, 175
  battleship_logo = pg.transform.scale(battleship_logo, (logo_width, logo_height))

  logo_x = 10
  logo_y = 10

  font_path = os.path.join("Battleship", "assets", "USAAF_FONT", "USAAF_Stencil.ttf")

  # setup text
  font = pg.font.Font(font_path, 50) # default font, size 50
  text_color = (255, 255, 255) # white text
  text = font.render("Press SPACE to start", True, text_color)

  text_x = (1024 - text.get_width()) // 2
  text_y = 600

  # frame rate for the animation
  fps = 9
  clock = pg.time.Clock()

  frame_index = 0

  blink_interval = 950 # blink every 500 milliseconds
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
            print('hi')
    
    # Clear the screen
    screen.fill((0,0,0))

    # Display the current frame
    screen.blit(frames[frame_index], (0,0))

    # display the battleship logo over top
    screen.blit(battleship_logo, (logo_x, logo_y))

    if current_time - last_blink_time > blink_interval:
       show_text = not show_text
       last_blink_time = current_time

    if show_text:
      # display the start text
      screen.blit(text, (text_x, text_y))

    # Update the display
    pg.display.flip()

    # Advance to the next frame
    frame_index = (frame_index + 1) % len(frames)

    # control the frame rate
    clock.tick(fps)
  
  pg.quit()

if __name__ == "__main__":
  main()
  # pg.quit()