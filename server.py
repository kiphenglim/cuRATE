#!/usr/bin/env python3
import socket
from _thread import *
import pickle
from game import Game


def threaded_client(conn, p, game):
  conn.send(str.encode(str(p)))

  while True:
    try:
      data = conn.recv(4096).decode()
      if not data:
        print('no data')
        break
      else:
        if data == "reset":
          game.reset_player_states()
        elif data == "get":
          game.play(p, data)
        conn.sendall(pickle.dumps(game))
    except:
        break

  print("Lost connection")
  print("Closing Game")
  conn.close()
  num_players -= 1


def main():
  num_players = 0
  server = ""
  port = 3000
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind((server, port))
  except socket.error as e:
    str(e)

  s.listen(10)
  print("Waiting for a connection, Server Started")

  while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    num_players += 1

    if num_players == 1:
      print("Creating a new game...")
      game = Game(num_players)
      game.ready = True
    else:
      game.addPlayer(num_players)
    print(num_players)
    start_new_thread(threaded_client, (conn, num_players, game))

if __name__ == '__main__':
  main()
