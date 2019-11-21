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

        # OVERRIDE THIS in your class!
        # board - current state of the board
        # x,y - your current row and column on the board
        # You can move a MAX of movesize in a SINGLE direction
        # 0-3 MOVES a player, 4-7 ATTACKS in that direction,
        #   if you are mage 8 gets mana back,
        #   if you are monk 8 gets health back

        def getMove(self, board, x, y, movesize):
            # Moves: 0-Up, 1-Right, 2-Down, 3-Left


            # return (action, move size)
                # If you attack/spell , THAT IS YOUR ACTION, you cannot move as well
            return (random.randint(0, 7), random.randint(1, movesize))
