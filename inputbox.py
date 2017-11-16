import pygame as pg
import string
from pygame.locals import *

def get_key():
  while True:
    event = pg.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, pos_x, pos_y, width, height, message):
  font = pg.font.SysFont('ubuntu', 16)

  pg.draw.rect(screen, (255, 255, 255), (pos_x, pos_y, width, height), 0)

  pg.draw.rect(screen, (0, 0, 0), (pos_x - 2, pos_y - 2, width + 20, height), 1)

  if len(message) != 0:
    screen.blit(font.render(message, 1, (0 , 0, 0)), (pos_x, pos_y))

  pg.display.flip()

def ask(screen, pos_x, pos_y, width, height, question):
  pg.font.init()
  current_string = []
  display_box(screen, pos_x, pos_y, width, height, question + ": " + string.join(current_string,""))
  while True:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string.append(chr(inkey))

    display_box(screen, pos_x, pos_y, width, height, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")
