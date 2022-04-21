from multiprocessing.connection import Connection
import pickle
import pygame
from pyrfc3339 import generate
import pygame_textinput

from art import Exhibition
from game import Game
from network import Network

pygame.font.init()
width = 1600
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
textinput = pygame_textinput.TextInputVisualizer()

num_clients = 0


def redrawWindow(win, game, exhibition):
  win.fill((128,128,128))

  if not(game.connected()):
    font = pygame.font.SysFont("arial", 80)
    text = font.render("Waiting for more players", 1, (255,0,0), True)
    win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
  else:
    exhibition.draw(win)

  pygame.display.update()


def generate_new_exhibition():
  e = Exhibition(0, 0, 1600, 900)
  e.generate_exhibition()
  return e


def run_game(exhibition):
  run = True
  clock = pygame.time.Clock()
  network = Network()
  pid = int(network.getP())
  exhib = exhibition

  while run:
    clock.tick(60)
    try:
      game = network.send("get")
    except:
      run = False
      print("Couldn't get game")
      break

    if game.allSubmitted():
      print('all players submitted')
      exhib = generate_new_exhibition()
      redrawWindow(win, game, exhib)
      textinput.value = ""
      try:
          game = network.send("reset")
          print('reset received')
      except:
          run = False
          print("Couldn't reset game")
          break

      if game.winner() != -1:
        if game.winner() == pid:
          text = font.render("You Won!", 1, (255,0,0))
        elif game.winner() != -1:
          text = font.render("You Lost...", 1, (255, 0, 0))
        font = pygame.font.SysFont("arial", 90)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
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
            game.players[pid].text = textinput.surface
            game = network.send("play")
      textinput.update(events)
      win.blit(textinput.surface, (800, 800))
      pygame.display.update()
      redrawWindow(win, game, exhib)


def menu_screen():
  clock = pygame.time.Clock()
  run = True

  while run:
    clock.tick(60)
    win.fill((128, 128, 128))
    font = pygame.font.SysFont("arial", 60)
    text = font.render(f"Number of players: {num_clients}", 1, (255,0,0))
    win.blit(text, (100,200))
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          run = False
          break
        if event.key == pygame.K_SPACE:
          run = False
          break

  run_game()

def main():
  # menu_screen()
  run_game(generate_new_exhibition())


if __name__ == "__main__":
  main()
