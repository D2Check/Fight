import random


class Player(object):
    name = None
    __health = None
    __mana = None
    __move_size = None
    __dmg = None
    __dmg_range = None
    next_move_size = None
    __move_index = -1

    role = None
    c = None
    o = None

    def __init__(self, role, c):
        self.c = c
        self.name = self.__class__.__name__
        if self.c == '1':
            self.o = '2'
        else:
            self.o = '1'
        roles = ["Thief", "Warrior", "Monk", "Mage"]
        if role not in roles:
            raise AttributeError("Bad Role Chosen", role)
        self.role = role
        self.__move_index = random.randint(0, len(self.__move_size) - 1)
        self.next_move_size = self.__move_size[self.__move_index]


        def getName(self):
            return self.name

        def getChar(self):
            return self.c

        # OVERRIDE THIS in your class, NOTHING ELSE
        # board - current state of the board
        # x,y - your current row and column on the board
        def getMove(self, board, x, y, movesize):
            # Moves: 0-Up, 1-Right, 2-Down, 3-Left
            return random.randint(0, 3)
