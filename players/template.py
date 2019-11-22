from players.player import Player


class YOURNAMEHERE(Player):
    # Feel free to add variables here.
    # You don't need to, it might be helpful

    # DONT CHANGE THIS
    def __init__(self, role, c):
        super().__init__(role, c)
        self.name = self.__class__.__name__

    # DONT CHANGE THIS PART

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
        self.x = x # YOUR X
        self.y = y # YOUR Y
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        ## YOUR CODE HERE

        ## YOUR CODE STOP HERE
        if 0 < chosen_move_size <= movesize:
            return (move_direction, attack_direction, chosen_move_size)

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
