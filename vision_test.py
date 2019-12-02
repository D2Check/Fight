import math
from itertools import permutations
import sys


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


def area_of_triangle(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


def isInside(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = area_of_triangle(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = area_of_triangle(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = area_of_triangle(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = area_of_triangle(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if (A == A1 + A2 + A3):
        return True
    else:
        return False


def get_sight(board, x, y, size, cross_centers):
    for center in cross_centers:
        centx, centy = center
        # Get the points of the cross
        pnts = [(centx + 1, centy), (centx, centy + 1), (centx - 1, centy), (centx, centy - 1)]
        to_check = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        pnts_check = [tuple(e) for e in pnts]
        touching = False
        if set(pnts_check) & set(to_check):
            for pnt in pnts:
                try:
                    to_check.remove(tuple(pnt))
                except:
                    continue
            if len(to_check) <= 2:
                touching = True
        if not touching:
            d = None
            to_elim = None
            # eliminate the closest point
            for pnt in pnts:
                px, py = pnt
                dist = math.sqrt((px - x) ** 2 + (py - y) ** 2)
                if d is None or dist < d:
                    d = dist
                    to_elim = pnt
            pnts.remove(to_elim)

            # for all permutations of points, find the largest triangle made with the player
            perms = permutations(pnts, 2)
            area = None
            save = None
            for i in list(perms):
                a, b = i
                ax, ay = a
                bx, by = b
                cx, cy = x, y
                curr_area = area_of_triangle(ax, ay, bx, by, cx, cy)
                if area is None or curr_area >= area:
                    area = curr_area
                    save = i

            # for those 2 points, draw a line that goes from player out of the board
            # TODO this will not work when the player is directly below a cross

            # This dict is the point of this function. It will save the details of the large and small triangles, as well
            # as the slope and y_intercept for the lines
            triangle_details = {
                "corner_player": {
                    "x": x,
                    "y": y
                },
                "cross_corners": [],
                "line_details": [],
                "outside_corners": [],
                "direction": None
            }
            # print(centx,x)
            if centx > x:
                triangle_details["direction"] = 1
            else:
                triangle_details["direction"] = -1
            # We need the slope and y_intercept for each of those pnts to the player
            for corner in save:
                tx, ty = corner

                if tx - x != 0:
                    slope = (ty - y) / (tx - x)
                    y_int = y - (slope * x)
                    line = (slope, y_int)
                    triangle_details["line_details"].append(line)
                    temp = (tx, ty)
                    triangle_details["cross_corners"].append(temp)
                else:
                    # print(triangle_details["direction"])
                    # print("This happens")
                    if triangle_details["direction"] == -1:
                        slope = float(sys.maxsize)
                        y_int = float(sys.maxsize)
                    else:
                        slope = float(sys.maxsize)
                        y_int = float(sys.maxsize)
                    line = (slope, y_int)
                    temp = (tx, ty)
                    triangle_details["cross_corners"].append(temp)
                    triangle_details["line_details"].append(line)
                    if centy > y:
                        for i in range(size - 1, centy, -1):
                            board[x][i] = " "
                    else:
                        # print("yes to here")
                        pass
                        # for i in range(0,centy):
                        #     board[x][i] = " "
            # using that slope and y_intercept. find 1 point each line that is OUTSIDE of the board
            ctr = 0
            for cross_pnt in triangle_details["cross_corners"]:
                tx, ty = cross_pnt
                slope, y_int = triangle_details["line_details"][ctr]
                if triangle_details["direction"] == -1:
                    for j in range(0, -51, -1):
                        k = j * slope + y_int
                        if k.is_integer():
                            triangle_details["outside_corners"].append((j, k))
                            break
                else:
                    for j in range(size, size + 50):
                        k = j * slope + y_int
                        if k.is_integer():
                            triangle_details["outside_corners"].append((j, k))
                            break
                ctr += 1
            # We have now found the 5 points we need
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

            # print(triangle_details)
            # for every location on the board
            for testy in range(size):
                for testx in range(size):
                    ax, ay, bx, by, cx, cy = small_triangle
                    inside_small = isInside(ax, ay, bx, by, cx, cy, testx, testy)
                    ax, ay, bx, by, cx, cy = large_triangle
                    inside_large = isInside(ax, ay, bx, by, cx, cy, testx, testy)
                    # if that point is inside the large triangle and not inside the small triangle we cant see there
                    if inside_large and not inside_small and board[testx][testy]:
                        board[testx][testy] = " "

        else:
            # some points ARE touching
            # print("Points are touching")
            # print(f"player at ({x},{y})")
            # print(pnts)
            up, down, left, right = False, False, False, False

            me = board[x][y]
            if (x - 1, y) in pnts:
                left = True
            if (x + 1, y) in pnts:
                right = True
            if (x, y + 1) in pnts:
                down = True
            if (x, y - 1) in pnts:
                up = True
            # print(up,down,left,right)
            if down and left:
                for k in range(y, size):
                    for j in range(x, -1, -1):
                        board[j][k] = " "
                board[x - 1][y] = "#"
                board[x - 1][y + 1] = "#"
                board[x][y + 1] = "#"
                board[x][y] = me

            if right and down:
                for k in range(y, size):
                    for j in range(x, size):
                        board[j][k] = " "
                board[x + 1][y] = "#"
                board[x + 1][y + 1] = "#"
                board[x][y + 1] = "#"
                board[x][y] = me
            if up and right:
                for k in range(y, -1, -1):
                    for j in range(x, size):
                        board[j][k] = " "
                board[x + 1][y] = "#"
                board[x + 1][y - 1] = "#"
                board[x][y - 1] = "#"
                board[x][y] = me
            if up and left:
                for k in range(y, -1, -1):
                    for j in range(x, -1, -1):
                        board[j][k] = " "
                board[x - 1][y] = "#"
                board[x - 1][y - 1] = "#"
                board[x][y - 1] = "#"
                board[x][y] = me
    return board


size = 20
board = [["."] * size for i in range(size)]
board[0][0] = "1"
p2x, p2y = 5, 5
board[p2x][p2y] = "2"
cross_centers = [(4, 3),(6,6)]
for cr in cross_centers:
    x, y = cr
    board = add_cross(board, x, y)
print_board(board, 20)
board = get_sight(board, p2x, p2y, 20, cross_centers)
print_board(board, 20)
