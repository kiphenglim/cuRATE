import os
import pygame
from random import randint

class Exhibition():
  def __init__(self, x, y, width, height):
    self.artworks = []
    self.x = x
    self.y = y
    self.width = width
    self.height = height


  def reset_artworks(self):
    self.artworks = []


  def generate_exhibition(self):
    self.reset_artworks()
    files = os.listdir('art')
    artwork_names = []

    while len(self.artworks) < 3:
      new_art = files[randint(0, len(files)-1)]
      if new_art not in artwork_names:
        artwork_names.append(new_art)
        self.artworks.append(
          Art('art/'+new_art, (self.width/3)*len(self.artworks), 100, 500, 500)
        )
    print(f'{len(self.artworks)} artworks in exhibition')


  def draw(self, win):
    for art in self.artworks:
      art.draw(win)



class Art():
  def __init__(self, img_path, x, y, width, height):
    self.img_path = img_path
    self.rect = (x, y, width, height)


  def draw(self, win):
    img = pygame.image.load(self.img_path).convert()
    win.blit(img, self.rect)
