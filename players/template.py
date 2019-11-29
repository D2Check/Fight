from player import Player
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SPELL = 4

class YOURNAMEHERE(Player):
    # Feel free to add variables here.
    # You don't need to, it might be helpful


    def __init__(self,  c):
        role = "CHOSE YOUR ROLE" # You can replace this with Warrior or Thief or Mage or Monk
        super().__init__(self.__class__.__name__,role, c)

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
        global UP, DOWN, LEFT, RIGHT, SPELL
        self.x = x # YOUR X
        self.y = y # YOUR Y
        # movesize is how far you can move this turn. you can chose to move 0 <= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        #
        # Feel free to use the UP, DOWN, LEFT and RIGHT constants for movement and attacking
        # move_direction = RIGHT for example
        #
        ## YOUR CODE HERE

        ## YOUR CODE STOP HERE
        if 0 <= chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
