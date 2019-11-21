import random
from players.Xyf import Xyf


class Fight(object):
    board = None
    __board_size = None
    next_player_turn = None
    __players = [" "]
    healths = [" ",None,None]
    manas = [" ", None, None]
    roles = {
        # "CLASS":{
        #   "move_size": the MAX spaces you can move,
        #               it rotates, so for thief, if you moved up to three spaces last time
        #               you can only move a max of 1 for the next 2 turns
        #   "dmg": min,max dmg you do if you attack the player
        # },
        "Thief":{
            "move_size": [1, 1, 3],
            "dmg": [1, 12],
            "dmg_range": 1,
            "health": 100

        },
        "Warrior":{
            "dmg":[6,10],
            "move_size": [1, 1],
            "dmg_range": 1,
            "health": 100
        },
        "Monk": {
            "dmg": [5, 8],
            "move_size": [1, 2],
            "dmg_range": 2,
            "mana":100,
            "health":100
        },
        "Mage": {
            "dmg": [4,5],
            "move_size": [1, 2],
            "dmg_range": 4,
            "mana": 100,
            "health": 100
        },

    }

    def __init__(self, size):
        self.__setup(size)

    def __build_board(self, size):
        self.__board_size = size
        return [["."] * size for i in range(size)]

    def __setup(self, size):
        coin_flip = random.randint(1, 2)
        self.next_player_turn = coin_flip
        self.board = self.__build_board(size)

    def set_space(self, x, y, c):
        self.board[x][y] = c

    def print_board(self):
        boardstr = "  "

        boardstr += "".join(["{:2}".format(e) for e in range(0, 20)])
        boardstr += "\n"
        for y in range(0, self.__board_size):
            boardstr += "{:2} ".format(y)
            for x in range(0, self.__board_size):
                boardstr += self.board[x][y] + " "
            boardstr += "\n"
        print(boardstr)

    def add_players(self, players):
        players[0].x, players[0].y = 0, 0
        players[1].x, players[1].y = 19, 19
        self.__players += players
        i = 1
        for player in players[0:]:
            self.healths[i] = 100
            if player.role == "Mage" or player.role == "Monk":
                self.manas[i] = 100
            i+= 1
            self.set_space(player.x, player.y, player.c)

    def fight(self):
        assert len(self.__players) == 3, "Players aren't the right size: {}".format(len(self.__players))
        p1 = self.__players[1]
        p2 = self.__players[2]

        while p1.health >= 0 and p2.health >= 0:
            if self.next_player_turn == 1:
                # p1 move
                self.makeMove(p1)
                self.next_player_turn +=1
            else:
                # p2 move
                self.makeMove(p2)
                self.next_player_turn -= 1

    def makeMove(self,player):
        tempboard = [row[:] for row in self.board]  # faster than deepcopy
        move,attack = player.getMove(tempboard, player.x, player.y)
        # TODO HERE




if __name__ == "__main__":
    f = Fight(20)
    players = [
        Xyf("Thief", "1"),
        Xyf("Warrior", "2")
    ]
    f.add_players(players)
    f.print_board()
