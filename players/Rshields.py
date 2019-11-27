from player import Player
import random


class Rshields(Player):
    # Feel free to add variables here.
    # You don't need to, it might be helpful
    boardsize = None

    def __init__(self, c):
        role = "Warrior"  # DECLARE YOUR ROLE HERE
        # print(f"Rshields {c}")

        super().__init__(role, c)
        self.name = self.__class__.__name__

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
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        # movesize is how far you can move this turn. you can chose to move 0 >= choice <= movesize
        move_direction = random.randint(0, 3)
        attack_direction = 0
        chosen_move_size = 1
        if self.boardsize is None:
            self.boardsize = len(board)
        ## YOUR CODE HERE
        ex, ey = self.enemy_stats['x'], self.enemy_stats['y']
        newx = x
        newy = y
        if move_direction == 0:
            newy = y - 1
        elif move_direction == 1:
            newx = x + 1
        elif move_direction == 2:
            newy = y + 1
        elif move_direction == 3:
            newx = x - 1
        if 0 <= newx < self.boardsize and 0 <= newy < self.boardsize:
            if board[newx][newy] == self.enemy:
                chosen_move_size = 0
                newx = x
                newy = y
        else:
            newx = x
            newy = y

        if newy == ey:
            # print("Filth attack y=ey")
            if newx < ex:
                # print("Filth attack right")
                attack_direction = 1
            else:
                # print("Filth move left")
                attack_direction = 3
        elif newx == ex:
            # print("Filth attack x=ex")
            if newy < ey:
                # print("Filth attack down")
                attack_direction = 2
            else:
                # print("Filth attack up")
                attack_direction = 0
        elif newy > ey:
            # print("Filth attacking up")
            attack_direction = 0
        elif ey > newy:
            # print("Filth attacking down")
            attack_direction = 2

        ## YOUR CODE STOP HERE
        if 0 <= chosen_move_size <= movesize:
            return move_direction, attack_direction, chosen_move_size

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
