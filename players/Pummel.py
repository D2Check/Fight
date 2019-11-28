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
        # print(f"Pummel Im at ({x},{y}) E at ({ex},{ey})")
        if y == ey:
            # print("Pummel move y=ey")
            if x < ex:
                # print("Pummel move right")
                move_direction = 1
            else:
                # print("Pummel move left")
                move_direction = 3
        elif x == ex:
            # print("Pummel move x=ex")
            if y < ey:
                # print("Pummel move down")
                move_direction = 2
            else:
                # print("Pummel move up")
                move_direction = 0
        elif y > ey:
            # print("Pummel moving up")
            move_direction = 0
        elif ey > y:
            # print("Pummel moving down")
            move_direction = 2

        newx = x
        newy = y
        if move_direction == 0:
            newy = y - 1
        elif move_direction == 1:
            newx = x + 1
        elif move_direction == 2:
            newy = y + 1
        elif move_direction == 3:
            newx = x - 1

        if board[newx][newy] == self.enemy:
            chosen_move_size = 0
            newx = x
            newy = y

        if newy == ey:
            # print("Pummel attack y=ey")
            if newx < ex:
                # print("Pummel attack right")
                attack_direction = 1
            else:
                # print("Pummel move left")
                attack_direction = 3
        elif newx == ex:
            # print("Pummel attack x=ex")
            if newy < ey:
                # print("Pummel attack down")
                attack_direction = 2
            else:
                # print("Pummel attack up")
                attack_direction = 0
        elif newy > ey:
            # print("Pummel attacking up")
            attack_direction = 0
        elif ey > newy:
            # print("Pummel attacking down")
            attack_direction = 2
        if self.health <= 20 and self.mana >= 50 :
            attack_direction = 4
        if 0 <= chosen_move_size <= movesize:
            # print("yes")
            return move_direction, attack_direction, chosen_move_size
