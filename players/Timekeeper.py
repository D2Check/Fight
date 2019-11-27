from players.Player import Player
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

    sdirections = ["up", "right", "down", "left", "spell"]

    def __init__(self, c):
        role = "Mage"
        # print(f"Timekeeper {c}")
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def get_metrics(self, x, y, ex, ey):
        # print(f"dist abs({ex} - {x}) + abs({ey}-{y})")
        distance_to_enemy = abs(ex - x) + abs(ey - y)
        return (distance_to_enemy, self.can_enemy_target_me(x, y, ex, ey), self.can_I_target_enemy(x, y, ex, ey))
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
        if self.boardsize is None:
            self.boardsize = len(board)

        possible = {
            "up": None,
            "right": None,
            "down": None,
            "left": None,
        }
        for key in possible.keys():
            if key == "up":
                if y - 1 >= 0 and not (x == ex and y - 1 == ey):
                    possible[key] = self.get_metrics(x, y - 1, ex, ey)
            if key == "right":
                if x + 1 < self.boardsize and not (y == ey and x + 1 == ex):
                    possible[key] = self.get_metrics(x + 1, y, ex, ey)
            if key == "down":
                if y + 1 < self.boardsize and not (x == ex and y + 1 == ey):
                    possible[key] = self.get_metrics(x, y + 1, ex, ey)
            if key == "left":
                if x - 1 >= 0 and not (y == ey and x - 1 == ex):
                    possible[key] = self.get_metrics(x - 1, y, ex, ey)

        # self.print_possible_moves(possible)
        better = []
        for k, v in possible.items():
            if v is not None:
                dist, din, dout = v
                if dout != -1 and din == -1:
                    # print(f"safe: move:{k} attack:{self.sdirections[dout]}")
                    better.append((dist,k, dout))

        else:
            # TODO
            # LOOP FOR WHEN WE CAN BOTH HIT EACH OTHER, WE ARE FACING ANOTHER MAGE
            pass
        # print("better",better)
        sorted_possibles = sorted(better, key=lambda tup: tup[0])
        # print("sorted better",sorted_possibles)
        if len(better) == 0:
            # GET OUT OF THE CORNERS
            # print("no safe")
            choice = -1
            if x < 4 and y < 4:
                # print("corner top left")
                choice = random.randint(1, 2)
                if choice == 1:
                    if x + 1 == ex and y == ey:
                        choice = 2
                else:
                    if x == ex and y + 1 == ey:
                        choice = 1

            elif x < 4 and y > self.boardsize - 4:
                # print("corner bottom left")
                choice = random.randint(0, 1)
                if choice == 1:
                    if x + 1 == ex and y == ey:
                        choice = 0
                else:
                    if x == ex and y - 1 == ey:
                        choice = 1
            elif x > self.boardsize - 4 and y < 4:
                # print("corner top right")
                choice = random.randint(2, 3)
                if choice == 2:
                    if x == ex and y - 1 == ey:
                        choice = 3
                else:
                    if y == ey and x - 1 == ex:
                        choice = 2
            elif x > self.boardsize - 4 and y > self.boardsize - 4:
                # print("corner bottom right")

                toss = random.randint(0, 1)
                if toss == 1:
                    choice = 0
                else:
                    choice = 3
                if choice == 0:
                    if x == ex and y - 1 == ey:
                        choice = 3
                else:
                    if x - -1 == ex and y == ey:
                        choice = 0

            # IM NOT IN A CORNER, RUN LIKE HELL
            elif 0 <= x < int(self.boardsize / 2) and 0 <= y < int(self.boardsize / 2) - 1:
                # print("top left, move right or up")
                choice = 1
                if y == ey and x + 1 == ex:
                    choice = 0
            elif int(self.boardsize / 2) <= x <= self.boardsize - 1 and 0 <= y < int(self.boardsize / 2) - 1:
                # print("top right, move down or right")

                choice = 0
                if y + 1 == ey and x == ex:
                    choice = 1
            elif int(self.boardsize / 2) <= x <= self.boardsize - 1 and int(
                    self.boardsize / 2) <= y <= self.boardsize - 1:
                # print("bottom right, move left or down")
                choice = 3

                if x - 1 == ex and y == ey:
                    choice = 2
            elif 0 <= x < int(self.boardsize / 2) and int(self.boardsize / 2) <= y <= self.boardsize - 1:
                # print("bottom left, move up or left")

                choice = 0
                if y - 1 == ey and x == ex:
                    choice = 3
            else:
                pass
                # print(f"Something went wrong")
                # print(f"Im at ({x},{y})")
                # print(f"int(self.boardsize / 2) = {int(self.boardsize / 2)}")
                # print(f"self.boardsize-1 = {self.boardsize - 1}")

            if 9 <= x <= 10 and 9 <= y <= 10:
                # IM IN THE CENTER OF THE MAP
                # print("Center of the map")
                if self.can_I_tele() and self.health <= 40:
                    # print("Teled out")
                    attack_direction = 4
            # print(f"I chose to move {self.sdirections[choice]}")
            move_direction = choice
            chosen_move_size = 1
        else:

            move_direction = self.directions[better[0][1]]
            attack_direction = better[0][2]

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
            drange = 1
        elif erole == "Monk":
            drange = 2
        else:
            drange = 4
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
