import random
from players.player import Player
from players.Xyf import Xyf


class Fight(object):
    board = None
    board_size = None
    next_player_turn = None
    players = [" "]
    healths = [" ", None, None]
    manas = [" ", None, None]
    moves_index = [" ", None, None]
    roles = {
        # "CLASS":{
        #   "move_size": the MAX spaces you can move,
        #               it rotates, so for thief, if you moved up to three spaces last time
        #               you can only move a max of 1 for the next 2 turns
        #   "dmg": min,max dmg you do if you attack the player
        #   "dmg_range": your attacks will go "this far" in the direction you choose
        #   "health: Starting health
        #   "mana": Starting mana if thats a thing
        # },
        "Thief": {
            "move_size": [2, 2, 3],
            "dmg": [1, 12],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,

        },
        "Warrior": {
            "dmg": [6, 10],
            "move_size": [1, 1],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,
        },
        "Monk": {
            "dmg": [5, 8],
            "move_size": [1, 2],
            "dmg_range": 2,
            "mana": 100,
            "health": 100
            # Your action will heal you for 30 health
            # costs 50 mana
        },
        "Mage": {
            "dmg": [3, 4],
            "move_size": [1, 1],
            "dmg_range": 4,
            "mana": 100,
            "health": 60
            # don't get hit
            # Your action will teleport you to a random corner that the enemy isn't in
            # costs 50 mana
        },

    }

    def __init__(self, size):
        self.__setup(size)

    def __build_board(self, size):
        self.board_size = size
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
        for y in range(0, self.board_size):
            boardstr += "{:2} ".format(y)
            for x in range(0, self.board_size):
                boardstr += self.board[x][y] + " "
            boardstr += "\n"
        print(boardstr)

    def add_players(self, players):
        players[0].x, players[0].y = 17, 18
        players[1].x, players[1].y = 1, 4
        self.players += players
        i = 1
        for player in players[0:]:
            self.healths[i] = 100
            if player.role == "Mage" or player.role == "Monk":
                self.manas[i] = 100
            self.set_space(player.x, player.y, player.me)
            self.moves_index[i] = random.randint(0, len(self.roles[player.role]["move_size"]) - 1)
            i += 1

    def fight(self):
        assert len(self.players) == 3, "Players aren't the right size: {}".format(len(self.players))

        p1 = self.players[1]
        p2 = self.players[2]

        while self.healths[1] > 0 and self.healths[2] > 0:
            for i in range(1, 3):
                self.players[i].health = self.healths[i]
                self.players[i].mana = self.manas[i]
            p1.update_stats(p1.to_dict(), p2.to_dict())
            p2.update_stats(p2.to_dict(), p2.to_dict())
            if self.next_player_turn == 1:
                # p1 move
                self.makeMove(p1, 1)
                self.next_player_turn += 1
            else:
                # p2 move
                self.makeMove(p2, 2)
                self.next_player_turn -= 1
            for i in range(1, 3):
                self.players[i].health = self.healths[i]
                self.players[i].mana = self.manas[i]
            p1.update_stats(p1.to_dict(), p2.to_dict())
            p2.update_stats(p2.to_dict(), p2.to_dict())
        if self.healths[1] <= 0:
            print("Player 2 won!")
        else:
            print("Player 1 won!")

    def makeMove(self, player: Player, index):
        #
        # SETUP
        #
        newx = None
        newy = None
        currx = player.x
        curry = player.y
        tarx, tary = None, None
        me = None
        enemy = None
        if index == 1:
            me = index
            enemy = 2
        else:
            me = 2
            enemy = 1

        # DATA TO SEND THE PLAYER
        tempboard = [row[:] for row in self.board]  # faster than deepcopy
        allowable_size = self.roles[player.role]["move_size"][int(self.moves_index[me])]
        self.moves_index[me] = (self.moves_index[me] + 1) % (len(self.roles[player.role]["move_size"]) - 1)
        # print(f"move:{movesize},allowable:{allowable_size}")
        # GET THEIR FEEDBACK
        try:
            move, attack, movesize = player.getMove(tempboard, player.x, player.y, allowable_size)
            pass
        except:
            return
        if 0 > movesize > allowable_size:
            self.healths[me] = 0
            # print("Player {} decided to cheat. They lose.")
        #
        # MOVEMENT
        #

        if move == 0:
            # up
            newx = currx
            newy = curry - movesize
        elif move == 1:
            # right
            newx = currx + movesize
            newy = curry
        elif move == 2:
            # down
            newx = currx
            newy = curry + movesize
        elif move == 3:

            # left
            newx = currx - movesize
            newy = curry
            # print("moving left")
        elif move == -1:
            newx = currx
            newy = curry
        else:
            newx = currx
            newy = curry

        if newx < 0 or \
                newx >= self.board_size or \
                newy < 0 or \
                newy >= self.board_size:
            # Tried to move off the board
            # print("invalid move")
            newx = currx
            newy = curry

        if self.board[newx][newy] == "1" or self.board[newx][newy] == "2":
            # Tried to move onto a player
            newx = currx
            newy = curry

        # If the move is valid, mark that square as unoccupied
        # print(f"curr:({currx},{curry}) new:({newx},{newy})")
        if currx != newx or newy != curry:
            # Valid move and some type of movement happened
            # print(f"({currx},{curry}) set to .")
            self.board[currx][curry] = "."
        self.board[newx][newy] = str(index)
        player.x, player.y = newx, newy

        #
        # ATTACK
        #

        attack_size = self.roles[player.role]["dmg_range"]
        tarx, tary = None, None
        skill = False
        if attack == 0:
            # up
            tary = newy - attack_size
            tarx = newx
            # print(f"targeting from ({newx},{newy}) to ({tarx},{tary})")
            targets = self.board[newx][tary:newy]

        elif attack == 1:
            # right
            tary = newy
            tarx = newx + attack_size
            targets = self.board[newx:tarx][newy]

        elif attack == 2:
            # down
            tary = newy + attack_size
            tarx = newx
            targets = self.board[newx][tary:newy]
        elif attack == 3:
            # left
            tary = newy
            tarx = newx - attack_size
            targets = self.board[tarx:newx][newy]
        elif attack == 4:
            tary = newy
            tarx = newx
            #
            # THIS IS A SPECIAL CASE DO NOT TARGET
            #
            skill = True

        if not skill:
            # print("Using attack")
            # print(enemy.me,targets)
            if self.players[enemy].me in targets:
                # print("hit")
                min, max = self.roles[player.role]['dmg']
                dmg = random.randint(min, max)
                # print(self.healths)
                self.healths[enemy] -= dmg

                # print(f"hit for {dmg}")
                # print(self.healths)
        else:
            if self.manas[me] is not None:
                if self.manas[me] >= 50:
                    if player.role == "Monk":
                        player.health += 30
                    elif player.role == "Mage":
                        ex, ey = self.players[enemy].x, self.players[enemy].y
                        eloc = [ex, ey]
                        locations = [[0, 0], [0, 19], [19, 0], [19, 19]]
                        if eloc in locations:
                            # The other player put themselves in a corner we can't go there
                            locations.remove(eloc)
                        # BLINK
                        self.board[newx][newy] = "."
                        random.shuffle(locations)
                        newx, newy = locations[random.randint(0, len(locations) - 1)]
                        self.board[newx][newy] = str(index)
                        player.x, player.y = newx, newy
                    self.manas[me] -= 50
        return


if __name__ == "__main__":
    f = Fight(20)
    players = [
        Xyf("Thief", "1"),
        Xyf("Mage", "2")
    ]
    p1 = players[0]
    p2 = players[1]
    f.add_players(players)
    f.print_board()
    f.makeMove(p2, 2)
    f.print_board()
