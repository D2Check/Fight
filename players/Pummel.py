import random
import math
import sys
from player import Player


class Pummel(Player):
    # Monk
    boardsize = None

    def __init__(self, c):
        role = "Monk"
        # print(f"Pummel {c}")

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
        # movesize is how far you can move this turn. you can chose to move 0 <= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = movesize
        #
        # EDIT DOWN
        #

        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']

        if y == ey:
            if x < ex:
                move_direction = 1
                attack_direction = 1
            else:
                move_direction = 3
                attack_direction = 3
        elif x == ex:
            if y < ey:
                move_direction = 2
                attack_direction = 2
            else:
                move_direction = 0
                attack_direction = 0
        elif y > ey:
            move_direction = 0
            attack_direction = 0
        elif ey > y:
            move_direction = 2
            attack_direction = 2
        if 0 <= chosen_move_size <= movesize:
            # print("yes")
            return move_direction, attack_direction, chosen_move_size