#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
import time
from copy import deepcopy

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field(pawn: str) -> list:
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    :param player int: Represents whether we're the first or second player
    """
    description = input().split()
    size = [int(description[1]), int(description[2][:-1])]
    field = [[] for i in range(size[0])]
    trans_field = [[] for _ in range(size[1])]
    for i in range(size[0]+1):
        l = input()
        if i != 0:
            l = list(str(l.split()[1]))
            for j, el in enumerate(l):
                trans_field[j] += [el]
            field[i-1] = l
    return field, trans_field


def parse_figure(pawn: str):
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **.
    ...
    00
    10
    01
    11
    02
    12
    """
    description = input().split()
    size = [int(description[1]), int(description[2][:-1])]
    figure = [[] for i in range(size[0])]
    for i in range(size[0]):
        l = input()
        figure[i] = list(l.replace("*", pawn))
    offset = figure_offset(figure, pawn)
    return figure, offset

def figure_offset(lst: list, important: str) -> list:
    y_off = 0
    x_off = 0
    for i, _ in enumerate(lst):
        if lst[i] == len(lst[i])*["."]:
            y_off += 1
        else:
            break
    for k, _ in enumerate(lst[0]):
        for i, _ in enumerate(lst):
            if lst[i][k] == important:
                break
        else:
            for i, _ in enumerate(lst):
                x_off += 1
    return y_off, x_off

def select_move(moves, enemy_pawns, pawn, field, trans_field, figure):
    debug(figure)
    good_moves = {}
    for move in moves:
        try_field = deepcopy(field)
        try_trans_field = deepcopy(trans_field)
        for y in range(len(figure)):
            for x in range(len(figure[y])):
                if figure[y][x] == pawn:
                    try_field[y+move[0]][x+move[1]] = "*"
                    try_trans_field[x+move[1]][y+move[0]] = "*"
        for el in try_field:
            debug(el)
        count = 0
        for i, direction in enumerate(enemy_pawns):
            for coord in direction:
                q = 1 if i&1 else -1
                if i < 2:
                    if pawn in try_field[coord[0]][::q][:coord[1]] or "*" in try_field[coord[0]][::q][:coord[1]]:
                        count += 1
                else:
                    if pawn in try_trans_field[coord[1]][::q][:coord[0]] or "*" in try_trans_field[coord[1]][::q][:coord[0]]:
                        count += 1
        if count not in good_moves:
            good_moves[count] = move
        debug(count)
    debug(good_moves[max(good_moves)])
    return good_moves[max(good_moves)]
def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    moves = []
    pawn = "O" if player == 1 else "X"
    enemy_pawn = "X" if player == 1 else "O"
    fields = parse_field(pawn)
    figure_info = parse_figure(pawn)
    figure = figure_info[0]
    offset = figure_info[1]
    field = fields[0]
    trans_field = fields[1]
    for x, _ in enumerate(field[:(len(field)-len(figure)+1)]):
        for y, _ in enumerate(field[x][:(len(field[0])-len(figure[0])+1)]):
            count = 0
            for n, _ in enumerate(figure):
                for m, _ in enumerate(figure[n]):
                    if figure[n][m] == pawn and field[x+n][y+m] != ".":
                        if field[x+n][y+m] == pawn:
                            count += 1
                        else:
                            count += 2
            if count == 1:
                moves += [(x, y)]
    if moves:
        # for el in figure:
        #     debug(el)
        new_moves = []
        enemy_pawns = [[], [], [], []] # left right top down\
        for rate, lst in enumerate([field, trans_field]):
            len_line = len(lst[0])
            for y, line in enumerate(lst):
                try:
                    if (found:=line.index(enemy_pawn)) > -1:
                        enemy_pawns[0+rate*2] += [(y, found,)] if rate == 0 else [(found, y,)]
                    if (found:=line[::-1].index(enemy_pawn)) > -1:
                        enemy_pawns[1+rate*2] += [(y, len_line - found - 1,)] if rate == 0 else [(len_line - found - 1, y,)]
                        found = -1
                except ValueError:
                    pass
        my_pawns = [[], [], [], []] # left right top down\
        for rate, lst in enumerate([field, trans_field]):
            len_line = len(lst[0])
            for y, line in enumerate(lst):
                try:
                    if (found:=line.index(pawn)) > -1:
                        my_pawns[0+rate*2] += [(y, found,)] if rate == 0 else [(found, y,)]
                    if (found:=line[::-1].index(pawn)) > -1:
                        my_pawns[1+rate*2] += [(y, len_line - found - 1,)] if rate == 0 else [(len_line - found - 1, y,)]
                        found = -1
                except ValueError:
                    pass
        my_center = (int(sum(y for lst in my_pawns for y, x in lst)/sum(map(len, my_pawns))), int(sum(x for lst in my_pawns for y, x in lst)/sum(map(len, my_pawns))),)
        enemy_center = (int(sum(y for lst in enemy_pawns for y, x in lst)/sum(map(len, enemy_pawns))), int(sum(x for lst in enemy_pawns for y, x in lst)/sum(map(len, enemy_pawns))),)
        enemy_placement = [[0, 1], [3, 2]][int(enemy_center[0]<my_center[0])][int(enemy_center[1]<my_center[1])]
        order = [1, 3, 0, 2][(4-enemy_placement)%4:] + [1, 3, 0, 2][:(4-enemy_placement)%4]
        for i in range(2):
            n = 0
            while n < len(field)+len(field[0]):
                for h, j in enumerate(order[i*2:]):
                    # debug((enemy_pawns[j], j,))
                    q = -1 if j>1 else 1
                    start_enemy_pawns = [(x_y, coord[1],) if not j>1 else (coord[0], x_y,) for coord in [enemy_pawns[j][0]] for x_y in range(coord[::q][0]-n, coord[::q][0]+1)]
                    end_enemy_pawns = [(x_y, coord[1],) if not j>1 else (coord[0], x_y,) for coord in [enemy_pawns[j][-1]] for x_y in range(coord[::q][0], coord[::q][0] + n+1)]
                    # debug(("why", start_enemy_pawns, end_enemy_pawns,))
                    check_moves = start_enemy_pawns+enemy_pawns[j][1:-1]+end_enemy_pawns
                    if j in [0, 3]:
                        check_moves = check_moves[::-1]
                    if h == 0:
                        check_moves = check_moves[::-1]
                    for coord in check_moves:
                        y, x = coord[0], coord[1]
                        n = -n if not j&1 else n
                        if j>1:
                            if (y+n, x,) in moves:
                                if len(new_moves) < 10:
                                    new_moves += [(y+n, x,)]
                                else:
                                    return select_move(new_moves, enemy_pawns, pawn, field, trans_field, figure)
                        else:
                            if (y, x+n,) in moves:
                                if len(new_moves) < 10:
                                    new_moves += [(y, x+n,)]
                                else:
                                    return select_move(new_moves, enemy_pawns, pawn, field, trans_field, figure)
                        n = -n if not j&1 else n
                n += 1
        if new_moves:
            return select_move(new_moves[::-1], enemy_pawns, pawn, field, trans_field, figure)
        return moves[0]
    return None


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        if not move:
            # debug("There is nothing we can do(cover)")
            print(*(0,0))
        else:
            print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    # debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug(f"Cannot get input. Seems that {'O' if player == 1 else 'X'} have lost ):")


if __name__ == "__main__":
    main()
