from enum import Enum

from player import Player, PlayerState



class Game:
  def __init__(self, pid):
    self.id = id
    self.players = {pid: Player(pid)}
    self.ready = False
    self.moves = {}


  def addPlayer(self, pid):
    self.players[pid] = Player(pid)

  def allSubmitted(self):
    for pid in self.players:
      if self.players[pid].player_state == PlayerState.WAITING:
        return False
    return True


  def connected(self):
    return self.ready


  def play(self, pid, text):
    self.moves[pid] = text
    self.players[pid].player_state = PlayerState.WENT


  def reset_player_states(self):
    for pid in self.players:
      self.players[pid].player_state = PlayerState.WAITING
    print('done resetting')


  def winner(self):
    for pid in self.players:
      if self.players[pid].points >= 7:
        return pid
    return -1
