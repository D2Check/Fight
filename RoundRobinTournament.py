from itertools import permutations
import random
from Fight import Fight, import_player
import players

games_per_matchup = 10


player_classes = {module_name: import_player(
    module_name) for module_name in players.__all__}
print(f'loaded {", ".join(player_classes)}')

players = {name: 0 for name in players.__all__}
matchups = list(permutations([e for e in players.keys()], 2))


def get_players(tup):
    to_ret = []
    for i, name in enumerate(tup):
        to_ret.append(player_classes[name](str(i + 1)))
    return to_ret


longestname = ""
totalgames = 0
for i, game_players in enumerate(matchups):
    print(f"Games between {game_players[0]} and {game_players[1]}")
    if len(game_players[0]) >= len(game_players[1]):
        if len(game_players[0]) > len(longestname):
            longestname = game_players[0]
    else:
        if len(game_players[1]) > len(longestname):
            longestname = game_players[1]
    games = 0
    while games < games_per_matchup:
        totalgames += 1
        # print(f"games: {games}")
        f = Fight(random.randint(15, 35))
        p1, p2 = get_players(game_players)
        f.add_players([p1, p2])
        # f.print_board()
        f.fight()
        # print(f"player {winner[0]} wins!")
        # print(f"game: {games} in turns: {winner[1]}")
        # print(f"{f.winner} wins!")
        players[f.winner] += 1
        games += 1
        print(
            f'{games+games_per_matchup*i}/{games_per_matchup*len(matchups)} games played '
            + f'|| {i+1}/{len(matchups)} matchups ({game_players[0]} vs {game_players[1]})'
            + ' ' * 30, end='\r')
print('\n')

for name, victories in players.items():
    spaces = (len(longestname) - len(name)) * " "
    print("{}{} {:>4} {:6}".format(spaces, name, round(
        100 * victories / totalgames, 2), victories))
