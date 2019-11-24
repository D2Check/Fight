from players.player import Player


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
        role = "Mage"  # You can replace this with Warrior or Thief or Mage or Monk
        super().__init__(role, c)
        self.name = self.__class__.__name__

    def get_metrics(self, x, y, ex, ey):
        distance_to_enemy = abs(ex - x) + abs(ey - y)
        return (distance_to_enemy, self.can_enemy_target_me(x, y,ex,ey), self.can_I_target_enemy(x, y,ex,ey))
        # return 0,0, self.can_I_target_enemy(x, y,ex,ey)

    def print_possible_moves(self,possible):
        for k,v in possible.items():
            dist,din,dout = v
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
    def getMove(self, board, x, y, movesize):
        self.turns += 1
        self.turns_since_tele += 1
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        ## YOUR CODE HERE
        if self.boardsize is None:
            self.boardsize = len(board)

        possible = {
            "up": self.get_metrics(x, y - 1, ex, ey),
            "right": self.get_metrics(x + 1, y, ex, ey),
            "down": self.get_metrics(x, y + 1, ex, ey),
            "left": self.get_metrics(x - 1, y, ex, ey),
        }
        self.print_possible_moves(possible)
        # if self.turns <= 4:
        #     chosen_move_size = 1
        #     # move towards the center
        #     if self.me == "1":
        #         if self.turns % 2 == 0:
        #             move_direction = 2
        #         else:
        #             move_direction = 1
        #     else:
        #         if self.turns % 2 == 0:
        #             move_direction = 0
        #         else:
        #             move_direction = 3
        # else:
        #     chosen_move_size = 1
        #     # Is there a space where I can hit you and you can't hit me?
        #     possible = {
        #         "up": self.get_metrics(board, x, y - 1, ex, ey),
        #         "right": self.get_metrics(board, x + 1, y, ex, ey),
        #         "down": self.get_metrics(board, x, y + 1, ex, ey),
        #         "left": self.get_metrics(board, x - 1, y, ex, ey),
        #     }
        #     self.print_possible_moves(possible)
        #     i = 0
        #     better = []
        #     for k, v in possible.items():
        #         dist, din, dout = v
        #         if dout != -1 and din == -1:
        #             better.append((dist, k))
        #         i += 1
        #     maxd = -1
        #     for e in better:
        #         if e[0] > maxd:
        #             move_direction = e[1]
        #     if self.turns >= 10 and self.turns_since_tele == -1 or self.turns_since_tele >= 10:
        #         if maxd == -1 and self.mana >= 50:
        #             self.turns_since_tele = 0
        #             attack_direction = 4
        #             move_direction = 0
        #             chosen_move_size = 0
        # etargetable = self.can_I_target_enemy(board, x, y)
        # targetable = self.can_enemy_target_me(board, ex, ey)
        # if etargetable != -1 and targetable == -1:
        #     # I can hit them, they can't hit me
        #     attack_direction = etargetable
        #     chosen_move_size = 0

        # "move_size": [1, 1],
        # "dmg_range": 4,
        # attack_direction = etargetable
        # print(f"{self.name} {self.me} h:{self.health} m:{self.mana}\n"
        #       f" \tmoving {chosen_move_size} towards {move_direction} {self.sdirections[move_direction]}\n"
        #       f"\tattacking {attack_direction} {attack_direction} {self.sdirections[attack_direction]}")
        if 0 <= chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
    def can_I_target_enemy(self, x, y,ex,ey):
        drange = 4

        # up
        if x == ex and abs(y - ey) <= drange:
            print(f"({x},{y}) ({ex},{ey}) up")
            return 0

        # right
        if y == ey and abs(ex-x) <= drange:
            print(f"({x},{y}) ({ex},{ey}) right")
            return 1

        # down
        if x == ex and abs(ey + y) <= drange:
            print(f"({x},{y}) ({ex},{ey}) down")
            return 2
        # left
        if y == ey and abs(ex - x) <= drange:
            print(f"({x},{y}) ({ex},{ey}) left")
            return 3
        return -1


    def can_enemy_target_me(self, x, y,ex,ey):
        erole = self.enemy_stats["role"]
        drange = 0
        if erole == "Warrior" or erole == "Thief":
            drange = 1
        elif erole == "Monk":
            drange = 2
        else:
            drange = 4
        #up
        if x == ex and (ey - y) <= drange:
            print(f"{erole} ({x},{y}) ({ex},{ey}) up")
            return 0

        # right
        if y == ey and (ex + x) <= drange:
            print(f"{erole} ({x},{y}) ({ex},{ey}) right")
            return 1

        # down
        if x == ex and (ey + y) <= drange:
            print(f"{erole} ({x},{y}) ({ex},{ey}) down")
            return 2
        # left
        if y == ey and (ex - x) <= drange:
            print(f"{erole} ({x},{y}) ({ex},{ey}) left")
            return 3
        return -1
