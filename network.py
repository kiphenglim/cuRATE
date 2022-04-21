from multiprocessing.connection import Connection
import socket
import pickle


class Network:
  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "127.0.0.1"
    self.port = 3000
    self.addr = (self.server, self.port)
    self.p = self.connect()


  def getP(self):
    return self.p

  def connect(self):
    self.client.connect(self.addr)
    return self.client.recv(2048).decode()

  def send(self, data):
    try:
      self.client.send(str.encode(data))
      return pickle.loads(self.client.recv(2048*2))
    except socket.error as e:
      print(e)