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
          print('thread_client: reset')
          game.reset_player_states()
        elif data == "get":
          print('thread_client: get')
        elif data == "play":
          print('thread_client: send')
          game.play(p, data)
        conn.sendall(pickle.dumps(game))
    except:
        break

  print("Lost connection")
  print("Closing Game")
  conn.close()


def main():
  server = ""
  port = 3000
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.bind((server, port))
  except socket.error as e:
    str(e)

  s.listen(10)
  print("Waiting for a connection, Server Started")
  player_id = 0

  while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if player_id == 0:
      print("Creating a new game...")
      game = Game(player_id)
      game.ready=True
    else:
      player_id += 1
      game.addPlayer(player_id)

      # # can start game when more than 3 players
      # if player_id > 2:
      #   game.ready = True

    start_new_thread(threaded_client, (conn, player_id, game))

if __name__ == '__main__':
  main()
