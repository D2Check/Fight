import random
import numpy as np
import math
import statistics
""" import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow, Circle """
from player import Player
from Fight import roles
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SPELL = 4


""" cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 800, 800) """


class Codec(Player):
    move_index = -1
    enemy_move_index = -1
    last_enemy_position = None
    boardsize = None
    last_health = 0
    last_position = None
    consecutive_minus_positions = 0
    strength_comparison = 0
    max_distance = 0

    def __init__(self, c):
        role = "Mage"
        super().__init__(self.__class__.__name__, role, c)

    def get_relative_position(self, x, y, direction, move_size):
        global UP, DOWN, LEFT, RIGHT
        if direction == UP:
            y -= move_size
        elif direction == DOWN:
            y += move_size
        elif direction == LEFT:
            x -= move_size
        elif direction == RIGHT:
            x += move_size
        else:
            raise ValueError(
                f'get_relative_position() direction param expected between 0 and 3 but got {direction}')
        # prevent invlaid positions
        x = max(min(self.boardsize - 1, x), 0)
        y = max(min(self.boardsize - 1, y), 0)
        return (x, y)

    def can_target_position(self, role, x, y, ex, ey):
        global UP, DOWN, LEFT, RIGHT
        target_aligned = self.is_target_aligned(x, y, ex, ey)
        if target_aligned == -1 or target_aligned > roles[role]['dmg_range']:
            return -1
        return self.get_direction(x, y, ex, ey)

    def is_target_aligned(self, x, y, ex, ey):
        if x == ex or y == ey:
            return abs(x - ex) + abs(y - ey)
        return -1

    def get_possible_move_positions(self, x, y, max_move_size):
        poss_move_pos = [(x, y)]
        for direction in range(4):
            for move_size in range(max_move_size):
                position = self.get_relative_position(
                    x, y, direction, move_size + 1)
                if not position in poss_move_pos:
                    poss_move_pos.append(position)
        return poss_move_pos

    def calculate_distance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    def get_direction(self, x, y, tx, ty):
        global UP, DOWN, LEFT, RIGHT
        if x > tx:
            return LEFT
        if x < tx:
            return RIGHT
        if y > ty:
            return UP
        if y < ty:
            return DOWN
        return -1

    # OVERRIDE THIS in your class!
    # board - current state of the board
    # x,y - your current row and column on the board
    # You can move a MAX of movesize in a SINGLE direction
    # 0-3 MOVES a player,
    # Moves: 0-Up, 1-Right, 2-Down, 3-Left
    # 0-3 ATTACKS in that direction,
    #   if you are mage 4 moves you randomly (not near your enemy),
    #   if you are monk 4 gets health back

    def get_move(self, board, x, y, max_move_size):
        global UP, DOWN, LEFT, RIGHT, SPELL
        self.x = x  # YOUR X
        self.y = y  # YOUR Y
        # max_move_size is how far you can move this turn. you can chose to move 0 <= choice <= max_move_size
        move_direction = 0
        attack_direction = 0
        chosen_move_size = 0
        #
        # Feel free to use the UP, DOWN, LEFT and RIGHT constants for movement and attacking
        # move_direction = RIGHT for example
        #

        # only gets executed at the first move
        if self.boardsize is None:
            self.boardsize = len(board)

            # get max distance the players could have
            self.max_distance = self.calculate_distance(
                0, 0, self.boardsize, self.boardsize)

            # calculate how strong the enemy is compared to the player
            enemy_strength = statistics.mean(
                roles[self.enemy_stats['role']]['dmg'])
            if self.enemy_stats['role'] == 'Monk':
                enemy_strength *= 1 + (roles['Monk']['heal'] * 2 / 100)
            self.strength_comparison = statistics.mean(
                roles[self.role]['dmg']) / enemy_strength

        # this part tries to figure out on what move index the enemy current is
        if self.enemy_move_index == -1:
            if self.last_enemy_position:
                last_move_size = abs(self.enemy_stats['x'] - self.last_enemy_position[0]) + abs(
                    self.enemy_stats['y'] - self.last_enemy_position[1])

                for i, max_enemy_move_size in enumerate(roles[self.enemy_stats['role']]['move_size']):
                    if max_enemy_move_size >= last_move_size:
                        if self.enemy_move_index == -1:
                            self.enemy_move_index = i
                        else:
                            self.enemy_move_index = -1
                            break
        else:
            self.enemy_move_index = (
                self.enemy_move_index + 1) % len(roles[self.enemy_stats['role']]['move_size'])

        self.last_enemy_position = (
            self.enemy_stats['x'], self.enemy_stats['y'])

        # get possible positions the enemy could move to
        enemy_move_size = 1
        # if move index is known, use the move size specified
        if self.enemy_move_index != -1:
            enemy_move_size = roles[self.enemy_stats['role']
                                    ]['move_size'][self.enemy_move_index]
        poss_enemy_move_pos = self.get_possible_move_positions(
            self.enemy_stats['x'], self.enemy_stats['y'], enemy_move_size)

        # generate score grid for how good each position is
        score_grid = np.zeros((self.boardsize, self.boardsize))
        for index, value in np.ndenumerate(score_grid):
            x, y = index

            # don't need to calulate the score if it isn't near both players
            if self.calculate_distance(x,y, self.enemy_stats['x'], self.enemy_stats['y']) > 6 \
                and self.calculate_distance(x,y, self.x, self.y) > 3:
                continue
            score_grid[x][y]+= 0.01
            # if enemy can be attacked from position
            if self.can_target_position(self.role, x, y, self.enemy_stats['x'], self.enemy_stats['y']) != -1:
                score_grid[x][y] += 1 * self.strength_comparison
            else:
                # if block is aligned with target
                if self.is_target_aligned(x, y, self.enemy_stats['x'], self.enemy_stats['y']) != -1:
                    score_grid[x][y] += 0.1

            # how many ways the player could be attacked
            possible_enemy_attacks = 0
            # how many ways the player could attack
            possible_attacks = 0
            for poss_ex, poss_ey in poss_enemy_move_pos:
                if self.can_target_position(self.enemy_stats['role'], poss_ex, poss_ey, x, y) != -1:
                    possible_enemy_attacks += 1
                if self.can_target_position(self.role, x, y, poss_ex, poss_ey) != -1:
                    possible_attacks += 1
            score_grid[x][y] -= 3 / self.strength_comparison + \
                possible_enemy_attacks / 20 if possible_enemy_attacks else 0
            #score_grid[x][y] += possible_attacks / 4

            #score_grid[x][y] -= self.calculate_distance(x, y, self.x, self.y) / self.max_distance / 10
            #score_grid[x][y] += self.calculate_distance(x,y, self.enemy_stats['x'], self.enemy_stats['y']) / self.max_distance /100

        # get the best goal position from score grid
        best_goal = None
        best_goal_distance = np.Infinity
        for goal_x, goal_y in np.argwhere(score_grid == np.amax(score_grid)):
            if self.calculate_distance(goal_x, goal_y, self.x, self.y) < best_goal_distance:
                best_goal = goal_x, goal_y

        # get possible positions the player can move to
        poss_move_pos = self.get_possible_move_positions(
            self.x, self.y, max_move_size)

        # calculate score for each possible position
        score_move_pos = np.zeros((len(poss_move_pos),))
        for i, position in enumerate(poss_move_pos):
            score_move_pos[i] += score_grid[position[0]][position[1]]
            score_move_pos[i] -= self.calculate_distance(
                *position, *best_goal) / self.max_distance
        best_move_pos = poss_move_pos[np.argmax(score_move_pos)]

        """ visual_score_grid = np.copy(score_grid)
        for i, score in enumerate(score_move_pos):
            move_pos = poss_move_pos[i]
            visual_score_grid[move_pos[0]][move_pos[1]] = score
        #visual_score_grid = (visual_score_grid + 5) / 10
        #visual_score_grid[self.enemy_stats['x']][self.enemy_stats['y']] = 0
        #visual_score_grid[self.x][self.y] = 1
        visual_score_grid[0][0] = 1.5
        visual_score_grid[self.boardsize - 1][self.boardsize - 1] = -3
        fig, ax = plt.subplots(1)
        ax.imshow(visual_score_grid.T)
        ax.add_patch(Circle((self.x, self.y), radius=0.5, color='red'))
        ax.add_patch(Circle(best_move_pos, radius=0.1, color='black'))
        plt.show(fig)
        # cv2.imshow('frame', visual_score_grid)
        # cv2.waitKey(1) """

        # check if skill should be used
        if self.mana >= 50:
            if self.last_health > self.health and score_grid[best_move_pos[0]][best_move_pos[1]] < -0.5:
                self.consecutive_minus_positions += 1
            else:
                self.consecutive_minus_positions = 0
            if np.max(score_move_pos) < min(np.min(score_grid) + 1, -1) \
                or (self.last_health > self.health and self.last_position == (self.x, self.y))\
                    or self.consecutive_minus_positions > 4:
                return 0, SPELL, 0
        self.last_position = (self.x, self.y)
        self.last_health = self.health

        # move towards best move position
        move_direction = self.get_direction(self.x, self.y, *best_move_pos)
        if move_direction == -1:
            move_direction = 0
        chosen_move_size = abs(self.x - best_move_pos[0]) + abs(
            self.y - best_move_pos[1])

        attack_direction = self.get_direction(
            *best_move_pos, self.enemy_stats['x'], self.enemy_stats['y'])

        if 0 <= chosen_move_size <= max_move_size:
            return move_direction, attack_direction, chosen_move_size

    # Feel free to add helper functions here.
    # You don't need to, it might be helpful
