import random
import math
import sys
from players.player import Player


class Xyf(Player):
    # THIEF
    boardsize = None

    def __init__(self, c):
        role = "Thief"
        # print(f"Xyf {c}")
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
    sdirections = ["up", "right", "down", "left", "spell"]
    def get_move(self, board, x, y, movesize):
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        #
        # EDIT DOWN
        #
        if self.boardsize is None:
            self.boardsize = len(board)

        # print("+"*50)
        distance_to_enemy = abs(self.enemy_stats['x'] - self.x) + abs(self.enemy_stats['y'] - self.y)
        if distance_to_enemy >= movesize:
            chosen_move_size = movesize
        else:
            chosen_move_size = distance_to_enemy
        move_possible = []
        ex, ey = self.enemy_stats['x'],self.enemy_stats['y']
        # print(f"dist to e {distance_to_enemy}")
        if distance_to_enemy == 2:
            chosen_move_size = 1
        # print(f"enemy is at ({ex},{ey})")
        # print(f"I am at {x},{y}")
        if x < ex:
            # print(f"right")
            if x + chosen_move_size <= self.boardsize-1:
                move_possible.append("right")
        if x > ex:
            # print(f"left")
            if x - chosen_move_size >=0:
                move_possible.append("left")

        if y < ey:
            # print(f"down")
            if y + chosen_move_size <=self.boardsize-1:

                move_possible.append("down")
        if y > ey:
            # print(f"up")
            if y - chosen_move_size >= 0:

                move_possible.append("up")
        # self.print_board(board)


        move_direction = self.directions[move_possible[random.randint(0, len(move_possible)-1)]]

        # print("move dir",move_direction)
        # print(f"Want to move {move_possible[move_direction]}")
        futurex, futurey = 0, 0
        if move_direction == 0:
            futurey = y - chosen_move_size
        elif move_direction == 1:
            futurex = x + chosen_move_size
        elif move_direction == 2:
            futurey = y + chosen_move_size
        elif move_direction == 3:
            futurex = x - chosen_move_size
        # print(f"future is ({futurex},{futurey})")
        future_neighbors = self.get_neighbors(board,futurex, futurey)


        neighbors = self.get_neighbors(board, x, y)
        for i in range(len(neighbors)):
            if neighbors[i] is not None:
                if neighbors[i].c == self.enemy:
                    # my enemy is standing next to me? Still?
                    chosen_move_size = 0
                    break
        if x + 1 == ex:
            # print("attack right")
            attack_direction = 1
        elif x - 1 == ex:
            # print("attack left")

            attack_direction = 3
        elif y + 1 == ey:
            # print("attack down")

            attack_direction = 2
        else:
            # print("attack up")

            attack_direction = 0

        # print(f"{self.name} {self.me}\n \tmoving {chosen_move_size} towards {move_direction} {self.sdirections[move_direction]}\n"
        #       f"\tattacking {attack_direction} {self.sdirections[attack_direction]}")
        if 0 <= chosen_move_size <= movesize:
            # print("yes")
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
