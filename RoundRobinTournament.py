from itertools import permutations
import random
from Fight import Fight, import_player
import players
import multiprocessing
import time
import sys

games_per_matchup = 2000

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
    games_skipped = 0
    times = []
    start = time.time()
    for i, game_players in enumerate(matchups):
        # print(f"Games between {game_players[0]} and {game_players[1]}")
        games = 0
        last_winner = None
        consecutive_wins = 0
        while games < games_per_matchup:
            f = Fight(random.randint(15, 35))
            p1, p2 = get_players(game_players)
            f.add_players([p1, p2])

            winner = f.fight()
            games_finished += 1

            if winner is not None:
                players[winner[0]][0] += 1

                if last_winner == winner[0]:
                    consecutive_wins += 1
                else:
                    consecutive_wins = 0
                last_winner = winner[0]
            players[p1.name][1] += 1
            players[p2.name][1] += 1

            times.append(time.time() - start)
            games += 1
            print(
                f'GAMES: {games_finished} played, {games_skipped} skipped, {games_per_matchup * len(matchups)} total needed ' +
                f'|| {i + 1}/{len(matchups)} matchups ({game_players[0]} vs {game_players[1]})' +
                ' ' * 30, end='\r')
            if consecutive_wins == 200:
                games_skipped += games_per_matchup - games
                break
    print('\n')
    print(f"took {time.time()-start} seconds")
    if len(sys.argv) > 1 and sys.argv[1] == '--export':
        if(len(sys.argv) == 2):
            path = 'leaderboard.txt'
        else:
            path = sys.argv[2]

        f = open(path, "w")
        for name, game_stats in players.items():
            f.write(
                f'{name}\t{game_stats[0]}\t{game_stats[1]}\t{round(100 * game_stats[0] / game_stats[1], 2)}\n')
        f.close()
        print(f'leaderboard was exported to {path}')
    else:
        longestname = ""
        for player in player_classes:
            if len(longestname) < len(player.__class__.__name__):
                longestname = player.__class__.__name__

        for name, game_stats in players.items():
            spaces = (len(longestname) - len(name)) * " "
            print("{}{} {:>5} {:8} {:8}".format(spaces, name, round(
                100 * game_stats[0] / game_stats[1], 2), game_stats[0], game_stats[1]))
