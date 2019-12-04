from player import Player
import random
import math

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SPELL = 4

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
        if self.tele_health is None:
            if self.enemy_stats['role'] == "Thief":
                self.tele_health = 21
                self.rounds_attacked_limit = 0
            elif self.enemy_stats['role'] == "Warrior":
                self.tele_health = 27
                self.rounds_attacked_limit = 3
            else:
                self.tele_health = 25
                self.rounds_attacked_limit = 2
        global UP,DOWN,LEFT,RIGHT,SPELL
        self.healths.append(self.health)
        self.turns += 1
        if len(self.healths) > 3:
            if self.healths[self.turns-2] != self.healths[self.turns-1]:
                self.rounds_attacked += 1
            else:
                self.rounds_attacked = 0
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']
        distance_to_enemy = math.sqrt((ex - x)**2 + (ey - y)**2)
        self.distances.append(round(distance_to_enemy,1))
        chosen_move_size = 1
        if distance_to_enemy > 7:
            chosen_move_size = movesize

        # print(f"enemy is at ({ex},{ey})")
        move_direction = 0
        attack_direction = 0
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']

        if self.boardsize is None:
            self.boardsize = len(board)
        if self.turns == 1 or self.turns % 3 == 0 or distance_to_enemy <= 3:
            self.set_goal(x, y, ex, ey)
        tx,ty = self.goal
        if y == ty:
            # print("Timekeeper move y=ty")
            if x < tx:
                # print("Timekeeper move right")
                move_direction = RIGHT
            else:
                # print("Timekeeper move left")
                move_direction = LEFT
        elif x == tx:
            # print("Timekeeper move x=tx")
            if y < ty:
                # print("Timekeeper move down")
                move_direction = DOWN
            else:
                # print("Timekeeper move up")
                move_direction = UP
        elif y > ty:
            # print("Timekeeper moving up")
            move_direction = UP
        elif ty > y:
            # print("Timekeeper moving down")
            move_direction = DOWN

        newx = x
        newy = y
        if move_direction == 0:
            newy = y - chosen_move_size
        elif move_direction == 1:
            newx = x + chosen_move_size
        elif move_direction == 2:
            newy = y + chosen_move_size
        elif move_direction == 3:
            newx = x - chosen_move_size

        if newx == tx and newy == ty:
            chosen_move_size = 0
            newx = x
            newy = y
        # print(f"x,y = ({newx},{newy}) ex,ey({ex},{ey})")
        if newy == ey:
            # print("Timekeeper attack newy=ey")
            if newx < ex:
                # print("Timekeeper attack right")
                attack_direction = RIGHT
            else:
                # print("Timekeeper attack left")
                attack_direction = LEFT
        elif newx == ex:
            # print("Timekeeper attack newx=ex")
            if newy < ey:
                # print("Timekeeper attack down")
                attack_direction = DOWN
            else:
                # print("Timekeeper attack up")
                attack_direction = UP
        elif newy > ey:
            # print("Timekeeper attacking up")
            attack_direction = UP
        elif ey > newy:
            # print("Timekeeper attacking down")
            attack_direction = DOWN
        if self.mana >= 50 and self.rounds_attacked > self.rounds_attacked_limit and self.health <= self.tele_health:
                attack_direction = SPELL
        # print(self.distances)
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
