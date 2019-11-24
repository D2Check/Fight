import random
import math
import sys
from players.player import Player


class Xyf(Player):
    # THIEF

    def __init__(self, c):
        role = "Thief"
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def print_board(self,board):
        boardstr = "  "

        boardstr += "".join(["{:2}".format(e) for e in range(0, 20)])
        boardstr += "\n"
        for y in range(0, len(board)):
            boardstr += "{:2} ".format(y)
            for x in range(0, len(board[0])):
                boardstr += board[x][y] + " "
            boardstr += "\n"
        print(boardstr)
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
            if x + chosen_move_size <= 19:
                move_possible.append("right")
        if x > ex:
            # print(f"left")
            if x - chosen_move_size >=0:
                move_possible.append("left")

        if y < ey:
            # print(f"down")
            if y + chosen_move_size <=19:

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
        try:
            future_neighbors = self.get_neighbors(board,futurex, futurey)
        except:
            sys.exit()

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
        # print(f"==={chosen_move_size} {movesize}")
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
