import random
import math
import sys
from players.player import Player


class Xyf(Player):

    def __init__(self, role, c):
        # print("Xyf {},{}".format(role,c))
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def get_neighbors(self, board, x, y):
        # Return 0-4: 0-Up, 1-Right, 2-Down, 3-Left
        neighbors = [None for e in range(4)]
        if x + 1 < 20:
            # right
            if board[x + 1][y] != self.o:
                neighbors[1] = Tile(x + 1, y, board[x + 1][y])
        if x - 1 >= 0:
            # Left
            if board[x - 1][y] != self.o:
                neighbors[3] = Tile(x - 1, y, board[x - 1][y])
        if y - 1 >= 0:
            # up
            if board[x][y - 1] != self.o:
                neighbors[0] = Tile(x, y - 1, board[x][y - 1])

        if y + 1 < 20:
            # down
            if board[x][y + 1] != self.o:
                neighbors[2] = Tile(x, y + 1, board[x][y + 1])
        return neighbors

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player, 4-7 ATTACKS in that direction
    def getMove(self, board, x, y, movesize):
        return (random.randint(0, 7), random.randint(1, movesize))


class Tile(object):
    distance_from_me = 0
    distance_from_enemy = 0
    x = 0
    y = 0
    c = " "

    def __init__(self, x, y, c):
        self.value = self.get_value_of_fruit(c)
        self.x = x
        self.y = y
        self.c = c

    def add_player_locations(self, me, them):
        self.distance_from_me = self.get_distance_to_player(me)
        self.distance_from_enemy = self.get_distance_to_player(them)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_distance_to_player(self, p):
        d = abs(p[0] - self.x) + abs(p[1] - self.y)
        return d

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{}({},{})".format(self.c, self.x, self.y)
