# cuRATE

A Cards Against Humanity-style, multiplayer, turn-based online game. Or at
least, that is the vision.

This game was developed as a final project for the Spring 2022 offering of
ARHI186A Perspectives in Contemporary Art at Pitzer College in Claremont, CA.
It was born out of the idea that the experience of art is shaped at least in
part by the audience, and the curator is only there as a guide.

### Wireframes & Demo
[Wireframe & Demo](https://docs.google.com/presentation/d/1JYIKw08Qmi-51llbBYGNFbLb4nSHqCvT6yqFlkURXBU/edit?usp=sharing)

<video width="320" height="240" controls>
  <source src="cuRATE demo.mp4" type="video/mp4">
</video>

## Running the Game

For the game to work, the server must be running. In the cuRATE directory on
the command line, run

```python
python3 server.py
```

then open as many new command line windows as you would like clients (also in
the cuRATE directory) and run

```python
python3 client.py
```

The minimum number of players is 3. Eventually this may be hosted online
somewhere, but this approach allows for local testing and development.

## Implementation

This is a project developed in Python3.

### Game Framework
The game itself relies on the [`pygame` module](https://www.pygame.org/news)
and [`pygame-textinput` module](https://pypi.org/project/pygame-textinput/),
which can be installed using `pip3` on the command line.

```python3
pip3 install pygame pygame-textinput
```

### Multiplayer Support
The multiplayer support relies on the [`websockets`
module](https://pypi.org/project/websockets/), which can also be installed via
`pip3' on the command line.

```python3
pip3 install asyncio websockets
```

For the multiplayer aspect, the game is coordinated and updated by a central
server and individual players have their own clients. Game information is
pickled and then transmitted via the network between server and clients.


## Contributors
Kip Lim, Harvey Mudd College

Vivian Pou, Harvey Mudd College
