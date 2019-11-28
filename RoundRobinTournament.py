from itertools import permutations
import random
from Fight import Fight, import_player
import players
import multiprocessing
import time

games_per_matchup = 100

if __name__ == '__main__':
    multiprocessing.freeze_support()
    player_classes = {module_name: import_player(
        module_name) for module_name in players.__all__}
    print(f'loaded {", ".join(player_classes)}')

    players = {name: [0, 0] for name in players.__all__}
    matchups = list(permutations([e for e in players.keys()], 2))


    def get_players(tup):
        to_ret = []
        for i, name in enumerate(tup):
            to_ret.append(player_classes[name](str(i + 1)))
        return to_ret


    games_finished = 0
    longestname = ""
    # totalgames = len(matchups) * games_per_matchup
    times = []
    p = multiprocessing.Pool()
    for i, game_players in enumerate(matchups):
        # print(f"Games between {game_players[0]} and {game_players[1]}")
        if len(game_players[0]) >= len(game_players[1]):
            if len(game_players[0]) > len(longestname):
                longestname = game_players[0]
        else:
            if len(game_players[1]) > len(longestname):
                longestname = game_players[1]
        games = 0
        while games < games_per_matchup:
            f = Fight(random.randint(15, 35))
            p1, p2 = get_players(game_players)
            f.add_players([p1, p2])
            start = time.time()
            # winner = p.apply(f.fight)
            winner = f.fight()
            if winner is not None:
                games_finished += 1
                players[winner[0]][0] += 1
            players[p1.name][1] += 1
            players[p2.name][1] += 1
            times.append(time.time() - start)
            games += 1
            print(
                f'{games_finished}/{games_per_matchup * len(matchups)} games played '
                + f'|| {i + 1}/{len(matchups)} matchups ({game_players[0]} vs {game_players[1]})'
                + ' ' * 30, end='\r')
    print('\n')

    for name, game_stats in players.items():
        spaces = (len(longestname) - len(name)) * " "
        print("{}{} {:>5} {:8}".format(spaces, name, round(
            100 * game_stats[0] / game_stats[1], 2), game_stats[0]))
