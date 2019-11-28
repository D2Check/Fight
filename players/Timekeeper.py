from player import Player
import random


class Timekeeper(Player):
    turns = 0
    turns_since_tele = -1
    boardsize = None
    directions = {
        "up": 0,
        "right": 1,
        "down": 2,
        "left": 3
    }
    goal = None

    sdirections = ["up", "right", "down", "left", "spell"]

    def __init__(self, c):
        role = "Mage"
        # print(f"Timekeeper {c}")
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def get_metrics(self, x, y, ex, ey):
        # print(f"dist abs({ex} - {x}) + abs({ey}-{y})")
        distance_to_enemy = abs(ex - x) + abs(ey - y)
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

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player,
    # Moves: 0-Up, 1-Right, 2-Down, 3-Left
    # 0-3 ATTACKS in that direction,
    #   if you are mage 4 moves you randomly (not near your enemy),
    #   if you are monk 4 gets health back
    def get_move(self, board, x, y, movesize):
        self.turns += 1
        self.turns_since_tele += 1
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']
        # print(f"enemy is at ({ex},{ey})")
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 1
        ## YOUR CODE HERE
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']

        if self.boardsize is None:
            self.boardsize = len(board)

        self.set_goal(x, y, ex, ey)
        tx,ty = self.goal
        if y == ty:
            # print("Timekeeper move y=ey")
            if x < tx:
                # print("Timekeeper move right")
                move_direction = 1
            else:
                # print("Timekeeper move left")
                move_direction = 3
        elif x == tx:
            # print("Timekeeper move x=ex")
            if y < ty:
                # print("Timekeeper move down")
                move_direction = 2
            else:
                # print("Timekeeper move up")
                move_direction = 0
        elif y > ty:
            # print("Timekeeper moving up")
            move_direction = 0
        elif ty > y:
            # print("Timekeeper moving down")
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

        if newy == ey:
            # print("Timekeeper attack y=ey")
            if newx < ex:
                # print("Timekeeper attack right")
                attack_direction = 1
            else:
                # print("Timekeeper move left")
                attack_direction = 3
        elif newx == ex:
            # print("Timekeeper attack x=ex")
            if newy < ey:
                # print("Timekeeper attack down")
                attack_direction = 2
            else:
                # print("Timekeeper attack up")
                attack_direction = 0
        elif newy > ey:
            # print("Timekeeper attacking up")
            attack_direction = 0
        elif ey > newy:
            # print("Timekeeper attacking down")
            attack_direction = 2
        if 0 <= chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size

    def can_I_tele(self):
        if self.mana >= 50:
            return True
        return False

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
                    possible[key] = self.get_metrics(x, y, ex - 5, ey)
            if key == "right":
                if ex + 5 < self.boardsize:
                    possible[key] = self.get_metrics(x, y, ex + 5, ey)
            if key == "down":
                if ey + 5 < self.boardsize:
                    possible[key] = self.get_metrics(x, y, ex, ey + 5)
            if key == "left":
                if ex - 5 >= 0:
                    possible[key] = self.get_metrics(x, y, ex - 5, ey)
        move_dir = None
        dist = 0
        for k, v in possible.items():
            if v is not None:
                if v[0] >= dist:
                    move_dir = k
                    self.goal = v[3]
