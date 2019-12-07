from player import Player
import random
import math

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SPELL = 4
import sys


class Timekeeper(Player):
    turns = 0
    rounds_attacked = 0
    rounds_attacked_limit = None
    tele_health = None
    boardsize = None
    distances = []
    directions = {
        "up": 0,
        "right": 1,
        "down": 2,
        "left": 3
    }
    goal = None
    sdirections = ["up", "right", "down", "left", "spell"]
    healths = []

    def __init__(self, c):

        role = "Mage"
        # print(f"Timekeeper {c}")
        super().__init__(self.__class__.__name__,role, c)




    def get_metrics(self, x, y, ex, ey):
        # print(f"dist abs({ex} - {x}) + abs({ey}-{y})")
        distance_to_enemy = math.sqrt((ex - x)**2 + (ey - y)**2)
        return (distance_to_enemy, self.can_enemy_target_me(x, y, ex, ey), self.can_I_target_enemy(x, y, ex, ey),(ex,ey))
        # return 0,0, self.can_I_target_enemy(x, y,ex,ey)

    def print_possible_moves(self, possible):
        for k, v in possible.items():
            if v is not None:
                dist, din, dout = v
                dist = f"enemy is {dist} away"

                if din == -1:
                    enemy = "enemy can't hit me"
                else:
                    enemy = "enemy can hit me"

                if dout == -1:
                    me = "I cant hit enemy"
                else:
                    me = "I can hit enemy"
                print(f"{k} {dist} {din} {enemy} {me}")

            else:
                print(f"{k} is invalid")
            # print(k,me,dout)
    def get_move(self, board, x, y, movesize):
        global UP,DOWN,LEFT,RIGHT,SPELL
        chosen_move_size = movesize
        move_direction = 3
        attack_direction = random.randint(0, 3)

        if 0 <= chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
    def can_I_target_enemy(self, x, y, ex, ey):
        drange = 4

        # up
        if x == ex and abs(y - ey) <= drange:
            # print(f"({x},{y}) ({ex},{ey}) up")
            return 0

        # right
        if y == ey and abs(ex - x) <= drange:
            # print(f"({x},{y}) ({ex},{ey}) right")
            return 1

        # down
        if x == ex and abs(ey + y) <= drange:
            # print(f"({x},{y}) ({ex},{ey}) down")
            return 2
        # left
        if y == ey and abs(ex - x) <= drange:
            # print(f"({x},{y}) ({ex},{ey}) left")
            return 3
        return -1

    def can_enemy_target_me(self, x, y, ex, ey):
        erole = self.enemy_stats["role"]
        drange = 0
        if erole == "Warrior" or erole == "Thief":
            drange = 2
        elif erole == "Monk":
            drange = 3
        else:
            drange = 5
        # up
        if x == ex and abs(ey - y) <= drange:
            # print(f"{erole} ({x},{y}) ({ex},{ey}) up")
            return 0

        # right
        if y == ey and abs(ex + x) <= drange:
            # print(f"{erole} ({x},{y}) ({ex},{ey}) right")
            return 1

        # down
        if x == ex and abs(ey + y) <= drange:
            # print(f"{erole} ({x},{y}) ({ex},{ey}) down")
            return 2
        # left
        if y == ey and abs(ex - x) <= drange:
            # print(f"{erole} ({x},{y}) ({ex},{ey}) left")
            return 3
        return -1

    def set_goal(self, x, y, ex, ey):
        possible = {
            "up": None,
            "right": None,
            "down": None,
            "left": None
        }
        for key in possible.keys():
            if key == "up":
                if ey - 5 >= 0:
                    possible[key] = self.get_metrics(x, y, ex, ey-5)
            if key == "right":
                if ex + 5 < self.boardsize:
                    possible[key] = self.get_metrics(x, y, ex + 5, ey)
            if key == "down":
                if ey + 5 < self.boardsize:
                    possible[key] = self.get_metrics(x, y, ex, ey + 5)
            if key == "left":
                if ex - 5 >= 0:
                    possible[key] = self.get_metrics(x, y, ex - 5, ey)
        dist = None
        for k, v in possible.items():
            if v is not None:
                # print(f"evaluating {v[3]} at {v[0]}")
                if dist is None:
                    dist = v[0]
                    self.goal = v[3]
                elif v[0] < dist:
                    self.goal = v[3]
        # print(f"Goal is now({self.goal[0]},{self.goal[1]})")
