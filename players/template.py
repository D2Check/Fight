from players.player import Player

class YOURNAMEHERE(Player):

    def __init__(self, role, c):
        # print("Xyf {},{}".format(role,c))
        super().__init__(role, c)
        self.name = self.__class__.__name__

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player, -1 to stay still
    # Moves: 0-Up, 1-Right, 2-Down, 3-Left
    # 0-3 ATTACKS in that direction,
    #   if you are mage 4 moves you randomly (not near your enemy),
    #   if you are monk 4 gets health back

    def getMove(self, board, x, y, movesize):
        self.x = x
        self.y = y
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        ## YOUR CODE HERE






        ## YOUR CODE STOP HERE
        if 0<chosen_move_size<=movesize:
            return (move_direction,attack_direction,chosen_move_size)