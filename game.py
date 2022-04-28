from enum import Enum

from player import Player, PlayerState
from art import Exhibition



class Game:
  def __init__(self, pid):
    self.id = id
    self.players = {pid: Player(pid)}
    self.ready = False
    self.moves = {}
    self.gamemaster = 0
    self.generate_new_exhibition()


  def addPlayer(self, pid):
    self.players[pid] = Player(pid)

  def allSubmitted(self):
    for pid in self.players:
      if self.players[pid].player_state == PlayerState.WAITING:
        return False
    return True

  def generate_new_exhibition(self):
    e = Exhibition(0, 0, 1600, 800)
    e.generate_exhibition()
    self.exhibition = e

  def draw_exhibition(self, win):
    self.exhibition.draw(win)


  def connected(self):
    return self.ready


  def play(self, pid, text):
    self.moves[pid] = text
    self.players[pid].text = text
    self.players[pid].player_state = PlayerState.WENT

  def is_best_chosen(self):
    return False

  def reset_player_states(self):
    for pid in self.players:
      self.players[pid].player_state = PlayerState.WAITING
    self.moves = {}
    print('done resetting')

  def increment_gamemaster(self):
    self.gamemaster = (self.gamemaster+1)%len(self.players)


  def winner(self):
    for pid in self.players:
      if self.players[pid].points >= 7:
        return pid
    return -1
