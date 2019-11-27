from itertools import permutations
import random
from Fight import Fight, import_player
import players

player_classes = {module_name: import_player(
    module_name) for module_name in players.__all__}
print(f'loaded {", ".join(player_classes)}')

players = {name: 0 for name in players.__all__}
perm = permutations([e for e in players.keys()], 2)


def get_players(tup):
    to_ret = []
    for i, name in enumerate(tup):
        to_ret.append(player_classes[name](str(i + 1)))
    return to_ret


longestname = ""
totalgames = 0
for i in list(perm):
    # print(f"Games between {i[0]} and {i[1]}")
    if len(i[0]) >= len(i[1]):
        if len(i[0]) > len(longestname):
            longestname = i[0]
    else:
        if len(i[1]) > len(longestname):
            longestname = i[1]
    games = 100
    while games > 0:
        totalgames += 1
        # print(f"games: {games}")
        f = Fight(random.randint(15, 35))
        p1, p2 = get_players(i)
        f.add_players([p1, p2])
        # f.print_board()
        f.fight()
        # print(f"player {winner[0]} wins!")
        # print(f"game: {games} in turns: {winner[1]}")
        # print(f"{f.winner} wins!")
        players[f.winner] += 1
        games -= 1

for k, v in players.items():
    spaces = (len(longestname) - len(k)) * " "
    print("{}{} {:>4} {:6}".format(spaces, k, round(100 * v / totalgames, 2), v))
