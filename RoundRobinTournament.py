from itertools import permutations
import random
from Fight import Fight, import_player
import players
import multiprocessing
from multiprocessing import Pool, Value, Manager, Lock
import time
import sys

games_per_matchup = 1000
consec_wins_before_skip = 200


def get_players(tup):
    to_ret = []
    for i, name in enumerate(tup):
        to_ret.append(player_classes[name](str(i + 1)))
    return to_ret


def split_array(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def worker(matchups):
    global lock, total_games_played, total_games_skipped, player_classes, games_won, games_played
    for i, game_players in enumerate(matchups):
        # print(f"Games between {game_players[0]} and {game_players[1]}")
        games_count = 0
        last_winner = None
        consecutive_wins = 0
        while games_count < games_per_matchup:
            # game setup
            f = Fight(random.randint(15, 35))
            p1, p2 = get_players(game_players)
            f.add_players([p1, p2])

            # play game
            winner = f.fight()
            with lock:
                total_games_played.value += 1

            # evaluate winner
            if winner is not None:
                games_won[winner[0]] += 1

                # count consecutive wins
                if last_winner == winner[0]:
                    consecutive_wins += 1
                else:
                    consecutive_wins = 0
                last_winner = winner[0]
            
            # count games played up
            games_played[p1.name] += 1
            games_played[p2.name] += 1

            games_count += 1
            # check if next games can be skipped because of consecutive wins
            if consecutive_wins == consec_wins_before_skip:
                with lock:
                    total_games_skipped.value += games_per_matchup - games_count
                break


def worker_init(l, tgp, tgs, pc, gw, gp):
    global lock, total_games_played, total_games_skipped, player_classes, games_won, games_played
    lock = l
    total_games_played = tgp
    total_games_skipped = tgs
    player_classes = pc
    games_won = gw
    games_played = gp


if __name__ == '__main__':
    multiprocessing.freeze_support()

    # for performance measuring  
    start = time.time()

    # import all players
    player_classes = {module_name: import_player(
        module_name) for module_name in players.__all__}
    print(f'loaded {", ".join(player_classes)}')

    # stuff for synced variables
    manager = Manager()
    lock = Lock()

    # games won and played for each player
    games_won = manager.dict()
    games_played = manager.dict()
    for name in players.__all__:
        games_won[name] = 0
        games_played[name] = 0

    # total games played and skipped
    total_games_played = manager.Value("i", 0)
    total_games_skipped = manager.Value("i", 0)

    # create and split matchups
    all_matchups = list(permutations(players.__all__, 2))
    split_matchups = list(split_array(
        all_matchups, multiprocessing.cpu_count()))

    # create pool and start all processes
    pool = Pool(processes=multiprocessing.cpu_count(), initializer=worker_init, initargs=(
        lock, total_games_played, total_games_skipped, player_classes, games_won, games_played))
    result = pool.map_async(worker, split_matchups)
    pool.close()

    # print progress while processes are running (also prints once after they finished)
    while True:
        with lock:
            print(
                f'GAMES: {total_games_played.value} played, {total_games_skipped.value} skipped, ' +
                f'{total_games_played.value+total_games_skipped.value}/{games_per_matchup * len(all_matchups)} total needed' +
                ' ' * 30, end='\r')
        if result.ready():
            break
        time.sleep(0.05)
    print('\n')

    # print performance stat
    print(f"took {time.time()-start} seconds")

    # output results
    if len(sys.argv) > 1 and sys.argv[1] == '--export':
        # save results to file
        if(len(sys.argv) == 2):
            path = 'leaderboard.txt'
        else:
            path = sys.argv[2]

        f = open(path, "w")
        for name in players.__all__:
            f.write(
                f'{name}\t{games_won[name]}\t{games_played[name]}\t{round(100 * games_won[name] / games_played[name], 2)}\n')
        f.close()
        print(f'leaderboard was exported to {path}')
    else:
        # output results to the console
        longestname = ""
        for player in player_classes:
            if len(longestname) < len(str(player)):
                longestname = str(player)

        for name in players.__all__:
            spaces = (len(longestname) - len(name)) * " "
            print("{}{} {:>5} {:8} {:8}".format(spaces, name, round(
                100 * games_won[name] / games_played[name], 2), games_won[name], games_played[name]))
