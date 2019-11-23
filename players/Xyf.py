import random
import math
import sys
from players.player import Player


class Xyf(Player):
    # THIEF

    def __init__(self, role, c):
        role = "Thief"
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def get_neighbors(self, board, x, y):
        # Return 0-4: 0-Up, 1-Right, 2-Down, 3-Left
        neighbors = [None for e in range(4)]
        if x + 1 < 20:
            # right
            if board[x + 1][y] != self.enemy:
                neighbors[1] = Tile(x + 1, y, board[x + 1][y])
        if x - 1 >= 0:
            # Left
            if board[x - 1][y] != self.enemy:
                neighbors[3] = Tile(x - 1, y, board[x - 1][y])
        if y - 1 >= 0:
            # up
            if board[x][y - 1] != self.enemy:
                neighbors[0] = Tile(x, y - 1, board[x][y - 1])

        if y + 1 < 20:
            # down
            if board[x][y + 1] != self.enemy:
                neighbors[2] = Tile(x, y + 1, board[x][y + 1])
        return neighbors

    def find_enemy(self, board):
        for i in range(len(board)):
            for k in range(len(board)):
                if board[i][k] == self.enemy:
                    return i, k

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player, 4-7 ATTACKS in that direction
    # 0-Up, 1-Right, 2-Down, 3-Left
    directions = {
        "up": 0,
        "right": 1,
        "down": 2,
        "left": 3
    }

    def getMove(self, board, x, y, movesize):
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        #
        # EDIT DOWN
        #
        distance_to_enemy = abs(self.enemy_stats.x - self.x) + abs(self.enemy_stats.y - self.y)
        move_possible = []
        ex, ey = self.find_enemy(board)
        print(f"enemy is at ({ex},{ey})")
        if x < ex:
            move_possible.append("right")
        if x > ex:
            move_possible.append("left")
        if y < ey:
            move_possible.append("down")
        if y > ey:
            move_possible.append("up")
        move_direction = self.directions[move_possible[random.randint(0, len(move_possible) - 1)]]

        if distance_to_enemy >= movesize:
            chosen_move_size = movesize
        else:
            chosen_move_size = distance_to_enemy
        futurex, futurey = 0, 0
        if move_direction == 0:
            futurey = y - chosen_move_size
        elif move_direction == 1:
            futurex = x + chosen_move_size
        elif move_direction == 2:
            futurey = y + chosen_move_size
        elif move_direction == 3:
            futurex = x - chosen_move_size

        future_neighbors = self.get_neighbors(futurex, futurey)

        for i in range(len(future_neighbors)):
            if future_neighbors[i] is not None:
                if future_neighbors[i].c == self.enemy:
                    attack_direction = i

        neighbors = self.get_neighbors(board, x, y)
        for i in range(len(neighbors)):
            if neighbors[i] is not None:
                if neighbors[i].c == self.enemy:
                    # my enemy is standing next to me? Still?
                    chosen_move_size = 0
                    attack_direction = i
        if 0 < chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size


class Tile(object):
    distance_from_me = 0
    distance_from_enemy = 0
    x = 0
    y = 0
    c = " "

    def __init__(self, x, y, c):
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
