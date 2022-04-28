#!/usr/bin/env python3
import pygame
import pygame_textinput

from art import Exhibition
from network import Network
from player import PlayerState

clock = pygame.time.Clock()
width = 1600
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
pygame.font.init()
font = pygame.font.SysFont("arial", 42)
textinput = pygame_textinput.TextInputVisualizer()

network = Network()
pid = int(network.getP())


def redrawWindow(win, game):
  win.fill((60,60,60))

  if not(game.connected()):
    font = pygame.font.SysFont("arial", 42)
    text = font.render("Waiting for more players", 1, (0,200,200), True)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
  else:
    game.draw_exhibition(win)

  pygame.display.update()


def run_game():
  run = True

  while run:
    clock.tick(60)
    try:
      game = network.send("get")
    except:
      run = False
      print("Couldn't get game")
      break

    if game.allSubmitted():
      for move in game.moves:
        text = font.render(game.moves[move],
          1, (0,200,200))
        win.blit(text,
          (width/2 - text.get_width()/2, height/2 - text.get_height()/2 + pid*100))
        pygame.display.update()
      clock.tick(60*10)
      try:
        game = network.send("reset")
        return game
      except:
        print("Couldn't reset game")
      pygame.display.update()
    else:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            run = False
            break
          if event.key == pygame.K_RETURN:
            # move = str(pid) + " " + textinput.value
            network.send(textinput.value)
      textinput.update(events)
      text = textinput.surface
      win.blit(text,
        (width/2 - text.get_width()/2, 3*height/4 - text.get_width()/2))
      pygame.display.update()
      redrawWindow(win, game)


def is_winner(game):
  if game.winner() == -1:
    return False
  if game.winner() == pid:
    text = font.render("You Won!", 1, (255,0,0))
  elif game.winner() != -1:
    text = font.render("You Lost...", 1, (255, 0, 0))
  font = pygame.font.SysFont("arial", 90)
  win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
  return True


def menu_screen():
  run = True

  while run:
    clock.tick(60)
    try:
      game = network.send("get")
    except:
      run = False
      print("Couldn't get game")
      pygame.quit()
      break

    num_clients = len(game.players)

    font = pygame.font.SysFont("arial", 42)
    win.fill((60,60,60))
    text = font.render(f"Number of players: {num_clients}", 1, (0,200,200))
    win.blit(text, (100,200))
    pygame.display.update()

    if num_clients > 3:
      run = False

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          run = False
          break
        if event.key == pygame.K_SPACE:
          run = False
          break

def main():
  menu_screen()
  run_game()


if __name__ == "__main__":
  main()
