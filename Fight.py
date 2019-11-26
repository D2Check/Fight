import random
from players.player import Player
from players.Xyf import Xyf
from players.Pummel import Pummel
from players.RShields import Rshields
from players.Timekeeper import Timekeeper
from players.Filth import Filth


class Fight(object):
    winner = None
    board = None
    board_size = None
    next_player_turn = None
    players = None
    healths = None
    manas = None
    moves_index = None
    turns = 0
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
            "move_size": [1, 1, 3],
            "dmg": [4, 15],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,

        },
        "Warrior": {
            "dmg": [7, 10],
            "move_size": [1, 1, 2],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,
        },
        "Monk": {
            "dmg": [1, 9],
            "move_size": [1, 2],
            "dmg_range": 2,
            "mana": 100,
            "health": 100,
            "heal": 55# Your action will heal you

            # costs 50 mana
        },
        "Mage": {
            "dmg": [3, 4],
            "move_size": [1, 1, 2],
            "dmg_range": 4,
            "mana": 100,
            "health": 60
            # don't get hit
            # Your action will teleport you to a random corner that the enemy isn't in
            # costs 50 mana
        },

    }

    def __init__(self, size):
        # print("Fight is made")
        self.__setup(size)

    def __setup(self, size):
        # print("setup")
        coin_flip = random.randint(1, 2)
        self.next_player_turn = coin_flip
        self.board = self.__build_board(size)

    def __build_board(self, size):
        # print("build board")

        self.board_size = size
        return [["."] * size for i in range(size)]

    def set_space(self, x, y, character_to_use):
        if self.board is not None:
            self.board[x][y] = character_to_use
        else:
            raise AttributeError("Board is not yet made")

    def print_board(self):
        board_string = self.get_stats_of_game()
        board_string += "\n  "

        board_string += "".join(["{:2}".format(e) for e in range(0, 20)])
        board_string += "\n"
        for y in range(0, self.board_size):
            board_string += "{:2} ".format(y)
            for x in range(0, self.board_size):
                board_string += self.board[x][y] + " "
            board_string += "\n"
        print(board_string)

    def add_players(self, players):
        players[0].x, players[0].y = 0, 0
        players[1].x, players[1].y = 19, 19
        new_players = [" "]
        new_healths = [" "]
        new_mana = [" "]
        new_moves_index = [" "]

        i = 1
        for player in players[0:]:
            new_players.append(player)
            new_healths.append(self.roles[player.role]["health"])
            player.health = self.roles[player.role]["health"]
            new_mana.append(self.roles[player.role]["mana"])
            player.mana = self.roles[player.role]["mana"]

            self.set_space(player.x, player.y, player.me)
            new_moves_index.append(random.randint(0, len(self.roles[player.role]["move_size"]) - 1))
            i += 1
        self.players = new_players
        self.healths = new_healths
        self.manas = new_mana
        self.moves_index = new_moves_index
        self.update_players()

    def get_stats_of_game(self):
        return f"{str(self.players[1])} {str(self.players[2])}"

    def update_players(self):
        p1 = self.players[1]
        p2 = self.players[2]
        for i in range(1, 3):
            self.players[i].health = self.healths[i]
            self.players[i].mana = self.manas[i]
        p1.update_stats(p1.to_dict(), p2.to_dict())
        p2.update_stats(p2.to_dict(), p1.to_dict())

    def fight(self):
        # print(self.players)
        assert len(self.players) == 3, "Players aren't the right size: {}".format(len(self.players))

        p1 = self.players[1]
        p2 = self.players[2]
        self.turns = 0

        while self.healths[1] > 0 and self.healths[2] > 0:

            self.turns += 1
            self.update_players()
            if self.next_player_turn == 1:
                # p1 move
                # self.print_board()
                self.make_move(p1, 1)
                self.next_player_turn += 1
            else:
                # p2 move
                # self.print_board()
                self.make_move(p2, 2)
                self.next_player_turn -= 1
            self.update_players()
        if self.healths[1] <= 0:
            self.winner = self.players[2].name
            return 2, self.turns
        else:
            self.winner = self.players[1].name
            return 1, self.turns

    def make_move(self, player: Player, index):
        #
        # SETUP
        #
        current_x = player.x
        current_y = player.y
        target_x, target_y = None, None
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
        move, attack, movesize = player.get_move(tempboard, player.x, player.y, allowable_size)
        if 0 > movesize > allowable_size:
            self.healths[me] = 0
            # print("Player {} decided to cheat. They lose.")
        #
        # MOVEMENT
        #
        # Moves: 0-Up, 1-Right, 2-Down, 3-Left
        new_x = current_x
        new_y = current_y
        if move == 0:
            # print(f"{index} move up")

            # up
            new_y = current_y - movesize
        elif move == 1:
            # print(f"{index} move right")

            # right
            new_x = current_x + movesize
        elif move == 2:
            # print(f"{index} move down")

            # down
            new_y = current_y + movesize
        elif move == 3:
            # print(f"{index} move left")

            # left
            new_x = current_x - movesize
            # print("moving left")
        else:
            new_x = current_x
            new_y = current_y

        if new_x < 0 or \
                new_x >= self.board_size or \
                new_y < 0 or \
                new_y >= self.board_size:
            # Tried to move off the board
            # print(f"{index} invalid move off board")
            new_x = current_x
            new_y = current_y

        if self.board[new_x][new_y] == "1" or self.board[new_x][new_y] == "2":
            # Tried to move onto a player
            # print(f"{index} invalid move onto player")

            new_x = current_x
            new_y = current_y

        # If the move is valid, mark that square as unoccupied
        # print(f"curr:({currx},{curry}) new:({newx},{newy})")
        if current_x != new_x or new_y != current_y:
            # Valid move and some type of movement happened
            # print(f"({currx},{curry}) set to .")
            self.board[current_x][current_y] = "."
        self.board[new_x][new_y] = str(index)
        player.x, player.y = new_x, new_y

        #
        # ATTACK
        #
        attack_size = self.roles[player.role]["dmg_range"]
        skill = False
        targets = []

        if attack == 0:
            # up

            # print("attack up")

            i = new_y
            while len(targets) < attack_size:
                i -= 1
                if i < 0:
                    break
                # print(f"adding ({newx},{i}) {self.board[newx][i]}")
                targets.append(self.board[new_x][i])


        elif attack == 1:
            # right
            # print("attack right")
            i = new_x
            while len(targets) < attack_size:
                i += 1
                if i > self.board_size - 1:
                    break
                # print(f"adding ({i},{newy}) {self.board[i][newy]}")
                targets.append(self.board[i][new_y])

        elif attack == 2:
            # print("attack down")

            # DOWN
            # print(f"size {attack_size}")
            i = new_y
            while len(targets) < attack_size:
                i += 1
                if i > self.board_size - 1:
                    break
                # print(f"adding ({newx},{i}) {self.board[newx][i]}")
                targets.append(self.board[new_x][i])
        elif attack == 3:
            # left
            # print("attack left")

            i = new_x
            while len(targets) < attack_size:
                i -= 1
                if i < 0:
                    break
                # print(f"adding ({i},{newy}) {self.board[i][newy]}")
                targets.append(self.board[i][new_y])
        elif attack == 4:
            #
            # THIS IS A SPECIAL CASE DO NOT TARGET
            #
            skill = True

        if not skill:
            # print("Using attack")
            # print(f"me{me}")
            # print(f"enemy{enemy}")
            # print(self.players[enemy].me,targets)

            if self.players[enemy].me in targets:
                # print("hit")
                min, max = self.roles[player.role]['dmg']
                dmg = random.randint(min, max)
                # print(self.healths)
                self.healths[enemy] -= dmg
                # print(self.healths)

                # print(f"Player{enemy} got hit for {dmg}")
                # print(self.healths)
        else:
            if self.manas[me] is not None:
                if self.manas[me] >= 50:
                    if player.role == "Monk":
                        # print("heal used")
                        self.healths[me] += self.roles["Monk"]["heal"]
                    elif player.role == "Mage":
                        ex, ey = self.players[enemy].x, self.players[enemy].y
                        eloc = [ex, ey]
                        locations = [[0, 0], [0, 19], [19, 0], [19, 19]]
                        if eloc in locations:
                            # The other player put themselves in a corner we can't go there
                            locations.remove(eloc)
                        # BLINK
                        self.board[new_x][new_y] = "."
                        random.shuffle(locations)
                        new_x, new_y = locations[random.randint(0, len(locations) - 1)]
                        self.board[new_x][new_y] = str(index)
                        player.x, player.y = new_x, new_y
                    self.manas[me] -= 50
        return

    def set_player_location(self, player, x, y):
        self.board[player.x][player.y] = "."
        player.x = x
        player.y = y
        self.board[player.x][player.y] = player.me
        self.update_players()


if __name__ == "__main__":
    wins = [0, 0]
    games = 1
    while games > 0:
        # print(f"games: {games}")
        f = Fight(20)
        players = [
            Filth("1"),
            Timekeeper("2")
        ]

        f.add_players(players)
        # f.print_board()
        winner = f.fight()
        # print(f"player {winner[0]} wins!")
        # print(f"game: {games} in turns: {winner[1]}")
        wins[winner[0] - 1] += 1
        games -= 1
    print(wins)
    # f = Fight(20)
    #
    # p1 = Timekeeper("1")
    # p2 = Rshields("2")
    # f.add_players([p1,p2])
    # f.print_board()
    # f.makeMove(p1, 2, 2, 2, 1)
    # f.set_player_location(p1,5,6)
    # f.set_player_location(p2,4,4)
    # f.print_board()
    #
    # p1.getMove(f.board,p1.x,p1.y,1)
    # f.print_board()
