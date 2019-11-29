import random
from player import Player

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SPELL = 4
class Xyf(Player):
    # THIEF
    boardsize = None

    def __init__(self, c):
        role = "Thief"
        # print(f"Xyf {c}")
        super().__init__(self.__class__.__name__,role, c)



    def get_neighbors(self, board, x, y):
        # Return 0-4: 0-Up, 1-Right, 2-Down, 3-Left
        neighbors = [None for e in range(4)]
        if x + 1 < self.boardsize:
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

        if y + 1 < self.boardsize:
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
        chosen_move_size = movesize
        #
        # EDIT DOWN
        #
        if self.boardsize is None:
            self.boardsize = len(board)

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
            newy = y - movesize
        elif move_direction == 1:
            newx = x + movesize
        elif move_direction == 2:
            newy = y + movesize
        elif move_direction == 3:
            newx = x - movesize

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
