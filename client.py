#!/usr/bin/env python3
import pygame
import pygame_textinput

from art import Exhibition
from network import Network

clock = pygame.time.Clock()
width = 1600
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
pygame.font.init()
font = pygame.font.SysFont("arial", 80)
textinput = pygame_textinput.TextInputVisualizer()

network = Network()
pid = int(network.getP())


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
      game = on_submission(game, network)
      if is_winner(game):
        break
      exhib = new_ex(game)
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
            game = network.send("get")
      textinput.update(events)
      win.blit(textinput.surface, (800, 800))
      pygame.display.update()
      redrawWindow(win, game, exhib)

def on_submission(game, network):
  # while not game.is_best_chosen():
  #   if pid == game.gamemaster:
  #     for move in game.moves:
  #       win.blit(font.render(game.moves[move], 1, (255,0,0)),
  #         (800,
  #         800))
  try:
    game = network.send("reset")
    return game
  except:
    print("Couldn't reset game")

def new_ex(game):
  exhib = generate_new_exhibition()
  redrawWindow(win, game, exhib)
  textinput.value = ""
  return exhib

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
      game = network.send("play")
    except:
      run = False
      print("Couldn't get game")
      break

    num_clients = len(game.players)

    font = pygame.font.SysFont("arial", 60)
    win.fill((128,128,128))
    text = font.render(f"Number of players: {num_clients}", 1, (255,0,0))
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
  run_game(generate_new_exhibition())


if __name__ == "__main__":
  main()
