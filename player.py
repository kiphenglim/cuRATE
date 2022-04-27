from enum import Enum

class PlayerState(Enum):
  WAITING = 0
  WENT = 1

class Player():
  def __init__(self, id):
    self.id = id
    self.player_state = PlayerState.WAITING
    self.text = ''
    self.points = 0


  def update(self, new_text):
    self.text = new_text
