import math
from itertools import permutations


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
    dont_change = ["1","2","#"]
    for center in cross_centers:
        tx, ty = center
        # Get the points of the cross
        pnts = [(tx + 1, ty), (tx, ty + 1), (tx - 1, ty), (tx, ty - 1)]
        # TODO this will not work when the player is next to the cross
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
        # TODO this will not work when the player is directly above a cross

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
        # We need the slope and y_intercept for each of those pnts to the player
        for corner in save:
            tx, ty = corner
            if triangle_details["direction"] is None:
                if tx > x:
                    triangle_details["direction"] = 1
                else:
                    triangle_details["direction"] = -1
            if tx - x != 0:
                slope = (ty - y) / (tx - x)
                y_int = y - (slope * x)
                temp = (tx, ty)
                line = (slope, y_int)
                triangle_details["cross_corners"].append(temp)
                triangle_details["line_details"].append(line)
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
                ax,ay,bx,by,cx,cy = small_triangle
                inside_small = isInside(ax,ay,bx,by,cx,cy,testx,testy)
                ax, ay, bx, by, cx, cy = large_triangle
                inside_large = isInside(ax, ay, bx, by, cx, cy, testx, testy)
                if inside_large and not inside_small and board[testx][testy] not in dont_change:
                    board[testx][testy] = ","
    return board


size = 20
board = [["."] * size for i in range(size)]
board[0][0] = "1"
board[15][5] = "2"
board = add_cross(board, 12, 12)
board = add_cross(board, 4, 3)
print_board(board, 20)
cross_centers = [(12, 12), (4, 3)]
board = get_sight(board, 15, 5, 20, cross_centers)
print_board(board, 20)
