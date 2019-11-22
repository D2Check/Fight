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


        def getName(self):
            return self.name

        def getChar(self):
            return self.c

        # OVERRIDE THIS in your class!
        # board - current state of the board
        # x,y - your current row and column on the board
        # You can move a MAX of movesize in a SINGLE direction
        # 0-3 MOVES a player, -1 to stay still
        # 0-3 ATTACKS in that direction,
        #   if you are mage 4 moves you randomly (not near your enemy),
        #   if you are monk 4 gets health back

        def getMove(self, board, x, y, movesize):
            # Moves: 0-Up, 1-Right, 2-Down, 3-Left


            # return (move, move size)
                # If you use a spell, you can't move again
            return (random.randint(0, 7), random.randint(1, movesize))
