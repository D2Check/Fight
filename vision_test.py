from itertools import permutations
import sys
import random
from player import Player
import sys
import time
import colorama
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
def print_board(board, size):
    board_string = "  "
    board_string += "".join(["{:2}".format(e) for e in range(0, 20)])
    board_string += "\n"
    for y in range(0, size):
        board_string += "{:2} ".format(y)
        for x in range(0, size):
            board_string += board[x][y] + " "
        board_string += "\n"
    print(board_string)


def add_cross(board, x, y):
    board[x][y] = "#"
    board[x + 1][y] = "#"
    board[x][y + 1] = "#"
    board[x - 1][y] = "#"
    board[x][y - 1] = "#"
    return board


import time


def __area_of_triangle(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


def __is_inside_triangle(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = __area_of_triangle(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = __area_of_triangle(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = __area_of_triangle(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = __area_of_triangle(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if (A == A1 + A2 + A3):
        return True
    else:
        return False


def get_sight(board, x, y, size, cross_centers):
    originalx,originaly = x,y
    for center in cross_centers:
        centx, centy = center
        # print(f"Working on ({centx},{centy})")
        # Get the points of the cross
        pnts = [(centx + 1, centy), (centx, centy + 1),
                (centx - 1, centy), (centx, centy - 1)]
        to_check = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        touching = False
        pnts_touching = []
        if set(pnts) & set(to_check):
            for pnt in pnts:
                save = False
                try:
                    to_check.remove(pnt)
                    save = True
                except:
                    continue
                if save:
                    pnts_touching.append(pnt)
            if len(to_check) == 2:
                touching = True
        if touching:
            # print("Yes touching")
            save = pnts_touching
        else:
            # print("Not touching")

            d = None
            to_elim = None
            for pnt in pnts:
                px, py = pnt
                dist = math.sqrt((px - x) ** 2 + (py - y) ** 2)
                if d is None or dist < d:
                    d = dist
                    to_elim = pnt
            pnts.remove(to_elim)
            perms = permutations(pnts, 2)
            area = None
            save = None
            for i in list(perms):
                a, b = i
                ax, ay = a
                bx, by = b
                cx, cy = x, y
                curr_area = __area_of_triangle(ax, ay, bx, by, cx, cy)
                if area is None or curr_area >= area:
                    area = curr_area
                    save = i
        triangle_details = {
            "corner_player": {
                "x": x,
                "y": y
            },
            "cross_corners": [],
            "outside_corners": [],
        }
        for corner in save:
            tx, ty = corner
            # board[tx][ty] = "@"
            triangle_details['cross_corners'].append(corner)
            xchange = x - tx
            ychange = y - ty
            # print(f"From ({x},{y}) to corner ({tx},{ty}) with vector ({xchange},{ychange})")
            if xchange == 0 or ychange == 0:
                newx = x
                newy = y
            else:
                newx = tx
                newy = ty
            while True:
                # if x >= tx:
                #     newx -=xchange
                # if y >= ty:
                #     newy -=ychange
                # else:
                #     newy += ychange

                if ychange == 0:
                    # kill = True
                    if xchange > 0:
                        newx = -1 * size
                    else:
                        newx = size * size
                else:
                    if not touching:
                        newx -= xchange

                if xchange == 0:
                    # kill = True
                    if ychange > 0:
                        newy = -1 * size
                    else:
                        newy = size * size
                else:
                    if not touching:
                        newy -= ychange

                # print(f"Eval ({newx},{newy})")
                if (newx < 0 or newx >= size) or (newy < 0 or newy >= size):
                    break
            outside_corner = (newx, newy)
            # print(f"Adding {outside_corner} as an outside corner")

            triangle_details['outside_corners'].append(outside_corner)
        # print(triangle_details)
        small_triangle = (triangle_details["corner_player"]["x"],
                          triangle_details["corner_player"]["y"],
                          triangle_details["cross_corners"][0][0],
                          triangle_details["cross_corners"][0][1],
                          triangle_details["cross_corners"][1][0],
                          triangle_details["cross_corners"][1][1],
                          )
        large_triangle = (triangle_details["corner_player"]["x"],
                          triangle_details["corner_player"]["y"],
                          triangle_details["outside_corners"][0][0],
                          triangle_details["outside_corners"][0][1],
                          triangle_details["outside_corners"][1][0],
                          triangle_details["outside_corners"][1][1],
                          )
        for testy in range(size):
            for testx in range(size):
                ax, ay, bx, by, cx, cy = small_triangle
                inside_small = __is_inside_triangle(
                    ax, ay, bx, by, cx, cy, testx, testy)
                ax, ay, bx, by, cx, cy = large_triangle
                inside_large = __is_inside_triangle(
                    ax, ay, bx, by, cx, cy, testx, testy)
                # if that point is inside the large triangle and not inside the small triangle we cant see there
                if inside_large and not inside_small and board[testx][testy]:
                    board[testx][testy] = " "
    # if kill:
    # string_board = np.array(board).T
    # float_board = np.zeros(string_board.shape + (3,))
    # switch = {
    #     '@': (0, 1, 1),
    #     ' ': (0, 0, 0),
    #     '.': (0.5, 0.5, 0.5),
    #     '#': (0.2, 0.2, 0.2),
    #     '1': (1, 0, 0),
    #     '2': (0, 1, 0)
    # }
    # for index, value in np.ndenumerate(string_board):
    #     x, y = index
    #     float_board[x][y] = switch[value]
    # fig, ax = plt.subplots(1)
    # ax.imshow(float_board)
    # for center in cross_centers:
    #     ax.add_patch(Circle(center, radius=0.4, color='blue'))
    # plt.show()
    #     sys.exit()

    return board


size = 20
board = [["."] * size for i in range(size)]
board[0][0] = "1"
p2x, p2y = 9, 1
board[p2x][p2y] = "2"
cross_centers = [(6,3),(15,17)]
for cr in cross_centers:
    x, y = cr
    board = add_cross(board, x, y)
print_board(board, 20)
board = get_sight(board, p2x, p2y, 20, cross_centers)
print_board(board, 20)
