import random
class Player(object):
    name = None
    enemy_stats = None
    __health = None
    __mana = None
    my_stats = None
    role = None
    me = None # THIS IS YOUR SYMBOL
    enemy = None # THIS IS THEIR SYMBOL
    x = None
    y = None

    def __init__(self, role, c):
        self.me = c
        self.name = self.__class__.__name__
        if self.me == '1':
            self.enemy = '2'
        else:
            self.enemy = '1'
        roles = ["Thief", "Warrior", "Monk", "Mage"]
        if role not in roles:
            raise AttributeError("Bad Role Chosen", role)
        self.role = role

    def get_name(self):
        return self.name

    def get_char(self):
        return self.me

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player, -1 to stay still
    # 0-3 ATTACKS in that direction,
    #   if you are mage 4 moves you randomly (not near your enemy),
    #   if you are monk 4 gets health back

    def getMove(self, board, x, y, movesize):
        self.x = x
        self.y = y
        # Moves: 0-Up, 1-Right, 2-Down, 3-Left


        # return (move, move size)
            # If you use a spell, you can't move again
        return (random.randint(0, 7), random.randint(1, movesize))

    def to_dict(self):
        return {
            "role"  :self.role,
            "x"     :self.x,
            "y"     :self.y,
            "health":self.__health,
            "mana"  :self.__mana,
        }

    def update_stats(self,me,enemy):
        self.enemy_stats = enemy
        self.my_stats = me
        # Fight keeps track of both players health and mana independently. This is for YOU.
        self.__mana = me['mana']
        self.__health = me['mana']
