from itertools import permutations
from Fight import Fight
from players.Xyf import Xyf
from players.Pummel import Pummel
from players.RShields import Rshields
from players.Timekeeper import Timekeeper
from players.Filth import Filth

players = {
    "Xyf": 0,
    "Pummel": 0,
    "Rshields": 0,
    "Timekeeper": 0,
    "Filth": 0
}
perm = permutations([e for e in players.keys()], 2)


def getplayers(tup):
    to_ret = []
    i = 1
    for name in tup:
        if name == "Filth":
            to_ret.append(Filth(str(i)))
        if name == "Xyf":
            to_ret.append(Xyf(str(i)))
        if name == "Pummel":
            to_ret.append(Pummel(str(i)))
        if name == "Rshields":
            to_ret.append(Rshields(str(i)))
        if name == "Timekeeper":
            to_ret.append(Timekeeper(str(i)))

        i += 1
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
    games = 1000
    while games > 0:
        totalgames += 1
        # print(f"games: {games}")
        f = Fight(20)
        p1, p2 = getplayers(i)
        f.add_players([p1, p2])
        # f.print_board()
        f.fight()
        # print(f"player {winner[0]} wins!")
        # print(f"game: {games} in turns: {winner[1]}")
        # print(f"{f.winner} wins!")
        players[f.winner] += 1
        games -= 1

for k,v in players.items():
    spaces = (len(longestname)-len(k)) * " "
    print("{}{} {:4} {:6}".format(spaces,k,round(100*v/totalgames,2),v))
