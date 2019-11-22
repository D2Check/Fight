import random
class Player(object):
    name = None
    enemy_stats = None
    health = None
    mana = None
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

    def getMove(self, board, x, y, movesize):
        self.x = x
        self.y = y
        # attack and move randomly. This will work, right?
        return (random.randint(0, 3),random.randint(0.3), random.randint(1, movesize))

    def to_dict(self):
        return {
            "role"  :self.role,
            "x"     :self.x,
            "y"     :self.y,
            "health":self.health,
            "mana"  :self.mana,
        }

    def update_stats(self,me,enemy):
        self.enemy_stats = enemy
        self.my_stats = me
        # Fight keeps track of both players health and mana independently. This is for YOU.
        # What I'm saying is, don't try to cheat
        self.mana = me['mana']
        self.health = me['mana']
