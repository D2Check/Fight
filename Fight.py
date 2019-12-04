import random
import players
from player import Player
import sys
import time
import colorama
import multiprocessing
colorama.init()

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
            "dmg": [4, 14],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,

        },
        "Warrior": {
            "dmg": [8, 10],
            "move_size": [1, 1, 2],
            "dmg_range": 1,
            "health": 100,
            "mana": 0,
        },
        "Monk": {
            "dmg": [2, 8],
            "move_size": [1, 2],
            "dmg_range": 2,
            "mana": 100,
            "health": 100,
            "heal": 43  # Your action will heal you

            # costs 50 mana
        },
        "Mage": {
            "dmg": [10, 10],
            "move_size": [1, 1, 2],
            "dmg_range": 4,
            "mana": 100,
            "health": 60
            # don't get hit
            # Your action will teleport you to a random corner that the enemy isn't in
            # costs 50 mana
        },

    }


import_player = lambda name: getattr(
    __import__('players.' + name, fromlist=['']), name)


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
    last_events = None

    def __init__(self, size: int) -> None:
        """
        Board size in width and length.
        - Calls __setup
        :param size: int
        """
        # print("Fight is made")
        self.__setup(size)

    def __setup(self, size: int) -> None:
        """
        Decide who goes first
        - Calls __build_board
        :param size: int
        """
        # print("setup")
        coin_flip = random.randint(1, 2)
        self.next_player_turn = coin_flip
        self.board = self.__build_board(size)

    def __build_board(self, size: int) -> list:
        """
        Build 2D list of size: size
        :param size: int
        :return: list of lists
        """
        # print("build board")

        self.board_size = size
        return [["."] * size for i in range(size)]

    def set_space(self, x: int, y: int, character_to_use: str) -> None:
        """
        Used in testing. Alters self.board directly.
        :param x: x coord
        :param y: y coord
        :param character_to_use: what character to put there
        :return: None
        """
        if self.board is not None:
            self.board[x][y] = character_to_use
        else:
            raise AttributeError("Board is not yet made")

    def print_board(self) -> None:
        """
        Print the board with stats about the players.
        Used in testing
        :return: None
        """
        board_string = f"{str(self.players[1])}, {str(self.players[2])}"
        board_string += "\n   "

        board_string += " ".join(["{:<2}".format(e) for e in range(0, 20)])
        board_string += "\n"
        for y in range(0, self.board_size):
            board_string += "{:2} ".format(y)
            for x in range(0, self.board_size):
                board_string += self.board[x][y] + "  "
            board_string += "\n"
        board_string += f'Last Events: P1 {self.last_events[0]}, P2 {self.last_events[1]}'
        print(board_string)

    def add_players(self, players_to_add: list) -> None:
        """
        Should contain 2 elements of the object Player or a class that inherits from player.
        Sets in the initial position of players locations as well as their health and mana.
        Updates the other player about the status of each player
        - Calls update_players
        :param players_to_add: list of players
        :return: None
        """
        global roles
        # STARTING LOCATIONS
        players_to_add[0].x, players_to_add[0].y = 0, 0
        players_to_add[1].x, players_to_add[1].y = self.board_size - \
            1, self.board_size - 1

        # WHAT WILL BE USED TO KEEP Fight AUTHORITATIVE OVER PLAYER OBJECTS
        new_players = [" "]
        new_healths = [" "]
        new_mana = [" "]
        new_moves_index = [" "]

        # SET PLAYERS INITIAL DETAILS
        i = 1
        for player in players_to_add[0:]:
            new_players.append(player)
            new_healths.append(roles[player.role]["health"])
            player.health = roles[player.role]["health"]
            new_mana.append(roles[player.role]["mana"])
            player.mana = roles[player.role]["mana"]

            self.set_space(player.x, player.y, player.me)

            # TODO Allow classes to choose when to move farther
            new_moves_index.append(random.randint(
                0, len(roles[player.role]["move_size"]) - 1))
            i += 1
        # SET Fight's VARIABLES
        self.players = new_players
        self.healths = new_healths
        self.manas = new_mana
        self.moves_index = new_moves_index

        # UPDATE THE PLAYERS OF EACH OTHERS STATS
        self.update_players()

    def update_players(self):
        """
        Update each player about themselves and the other player
        :return:
        """
        p1 = self.players[1]
        p2 = self.players[2]
        for i in range(1, 3):
            # THIS ENSURES THAT FIGHT ALWAYS CONTROLS HEALTH / MANA
            self.players[i].health = self.healths[i]
            self.players[i].mana = self.manas[i]
        p1.update_stats(p1.to_dict(), p2.to_dict())
        p2.update_stats(p2.to_dict(), p1.to_dict())

    def fight(self, print_board=0, interval=0):
        """
        Main game loop.
        Set's self.winner upon finishing.
        Calls
        - update_players 2x
        - make_move
        :param print_board: if the board should be printed (0/False = no, 1/True = yes, 2 =  yes, but don't overwrite console lines)
        :param interval: interval between rounds in seconds
        :return (Player's character, Amount of turns):
        """
        # print(self.players)
        assert len(self.players) == 3, "Players aren't the right size: {}".format(
            len(self.players))

        p1 = self.players[1]
        p2 = self.players[2]
        self.turns = 0

        # MAIN GAME LOOP
        timeout = False
        while self.healths[1] > 0 and self.healths[2] > 0:
            self.last_events = ['-', '-']
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
            if self.turns == 4500:  # each player gets half of these turns to kill the other player.
                # There's a long explanation for how I ended up at 3500 turns but, long story short,
                # if you move literally randomly and just "aim" intelligently, the amount of turns both players could
                # need will essentially NEVER be higher than 3500
                timeout = True
                break
            if print_board:
                self.print_board()
            time.sleep(interval)
            if print_board == 1:
                # move cursor back up
                print(f"\x1b[{25}A")
                print(f"\x1b[{21}D")
                # clear console
                print("\x1b[2J")
        # SOMEONE HAS WON
        if timeout:
            # print("QUIT DUE TO TIMEOUT")
            return None
        if self.healths[1] <= 0:
            self.winner = self.players[2].name
            return self.players[2].name, self.turns
        else:
            self.winner = self.players[1].name
            return self.players[1].name, self.turns

    def make_move(self, player: Player, index: int) -> None:
        global roles
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
        allowable_size = roles[player.role]["move_size"][int(
            self.moves_index[me])]
        self.moves_index[me] = (
            self.moves_index[me] + 1) % len(roles[player.role]["move_size"])
        # print(f"move:{movesize},allowable:{allowable_size}")
        # GET THEIR FEEDBACK

        movesize = 0
        move = 0
        attack = 0
        # print("Attemping to get a move")
        start = time.time()
        move, attack, movesize = player.get_move(tempboard, player.x, player.y, allowable_size)
        end = time.time()
        if end - start > .005:
            self.healths[me] = 0
            print(f"player {me} took too long, they lose")
        if 0 > movesize > allowable_size:
            # print("failed move_size")
            self.healths[me] = 0
            # print("Player {} decided to cheat. They lose.")
        # print("Yay")
        #
        # MOVEMENT HAPPENS HERE
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
            # YOUR MOVE WAS INVALID, YOU STAY STILL
            new_x = current_x
            new_y = current_y

        if new_x < 0 or \
                new_x >= self.board_size or \
                new_y < 0 or \
                new_y >= self.board_size:
            # TRIED TO MOVE OFF THE BOARD, STAY STILL
            # print(f"{index} invalid move off board")
            new_x = current_x
            new_y = current_y

        if self.board[new_x][new_y] == "1" or self.board[new_x][new_y] == "2":
            # TRIED TO MOVE ONTO A PLAYER, STAY STILL
            # print(f"{index} invalid move onto player")

            new_x = current_x
            new_y = current_y

        # MOVE IS VALID AND SQUARE IS UNOCCUPIED
        # print(f"curr:({current_x},{current_y}) new:({new_x},{new_y})")
        if current_x != new_x or new_y != current_y:
            # Valid move and some type of movement happened
            # print(f"({currx},{curry}) set to .")
            self.board[current_x][current_y] = "."
        self.board[new_x][new_y] = str(index)
        player.x, player.y = new_x, new_y

        #
        # ATTACK HAPPENS HERE
        #
        attack_size = roles[player.role]["dmg_range"]
        skill = False
        targets = []

        if attack == 0:
            # up
            # print(f"{me} attack up")
            self.last_events[index - 1] = 'attacked up'

            i = new_y
            while len(targets) < attack_size:
                i -= 1
                if i < 0:
                    break
                # print(f"adding ({newx},{i}) {self.board[newx][i]}")
                targets.append(self.board[new_x][i])

        elif attack == 1:
            # right
            # print(f"{me} attack right")
            self.last_events[index - 1] = 'attacked right'

            i = new_x
            while len(targets) < attack_size:
                i += 1
                if i > self.board_size - 1:
                    break
                # print(f"adding ({i},{newy}) {self.board[i][newy]}")
                targets.append(self.board[i][new_y])

        elif attack == 2:
            # print(f"{me} attack down")
            # down
            self.last_events[index - 1] = 'attacked down'

            i = new_y
            while len(targets) < attack_size:
                i += 1
                if i > self.board_size - 1:
                    break
                # print(f"adding ({newx},{i}) {self.board[newx][i]}")
                targets.append(self.board[new_x][i])
        elif attack == 3:
            # left
            # print(f"{me} attack left")
            self.last_events[index - 1] = 'attacked left'

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

            # IF THE ENEMY WAS ABLE TO HIT YOU
            if self.players[enemy].me in targets:
                # print("hit")
                # HOW MUCH DMG THE DO THIS TURN
                min, max = roles[player.role]['dmg']
                dmg = random.randint(min, max)
                # print(self.healths)
                # THIS PERFORMS THE ACTUAL DMG
                self.healths[enemy] -= dmg
                # print(self.healths)
                self.last_events[enemy - 1] = 'took damage'

                # print(f"Player{enemy} got hit for {dmg}")
                # print(self.healths)
        else:
            if self.manas[me] >= 50:
                self.last_events[index - 1] = 'used skill'
                if player.role == "Monk":
                    # print("heal used")
                    # HEAL FOR HEAL AMOUNT
                    self.healths[me] += roles["Monk"]["heal"]
                    if self.healths[me] > 100:
                        self.healths[me] = 100
                elif player.role == "Mage":
                    # THE MAGE TELEPORTS TO A RANDOM, UNOCCUPIED CORNER
                    ex, ey = self.players[enemy].x, self.players[enemy].y
                    enemy_location = [ex, ey]
                    locations = [[0, 0], [0, self.board_size - 1], [self.board_size - 1, 0],
                                 [self.board_size - 1, self.board_size - 1]]
                    if enemy_location in locations:
                        # The other player put themselves in a corner we can't go there
                        locations.remove(enemy_location)
                    # tele
                    self.board[new_x][new_y] = "."
                    random.shuffle(locations)
                    new_x, new_y = locations[random.randint(
                        0, len(locations) - 1)]
                    self.board[new_x][new_y] = str(index)
                    player.x, player.y = new_x, new_y
                self.manas[me] -= 50
        return

    def set_player_location(self, player: Player, x: int, y: int) -> None:
        """
        Used for testing
        :param player: player object
        :param x: x coord
        :param y: y coord
        :return: None
        """
        assert self.board is not None
        assert player in self.players
        self.board[player.x][player.y] = "."
        player.x = x
        player.y = y
        self.board[player.x][player.y] = player.me
        self.update_players()


if __name__ == "__main__":
    # all = ["Filth","Pummel","Xyf"]
    all = ["Filth"]
    for p in all:
        p1 = import_player(p)("1")
        p2 = import_player("Timekeeper")("2")
        wins = {
            p1.name: 0,
            p2.name: 0
        }
        games = 100
        print(f"{p1.name} and {p2.name}")
        while games > 0:
            # print(f"games: {games}")
            f = Fight(20)
            players = [
                p1,
                p2
            ]
            f.add_players(players)
            # f.print_board()
            winner = f.fight()
            if winner is not None:
                wins[winner[0]] += 1
            # print(f"player {winner[0]} wins!")
            # print(f"game: {games} in turns: {winner[1]}")
            games -= 1
        print(wins)
