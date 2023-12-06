#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""
import sys
from logging import DEBUG, debug, getLogger
sys.setrecursionlimit(10000)
# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)

#___________________________________________________________
#decision funcs
#___________________________________________________________
"""TO DO"""
def coords(figure: list, field: list, player: int):
    figure_coords = []
    for y_f, line_f in enumerate(figure):
        for x_f, symbol_f in enumerate(line_f):
            if symbol_f == '*':
                figure_coords.append((x_f, y_f))
    field_coords = []
    field_coords_enemy = []
    for y, line in enumerate(field):
        for x, symbol in enumerate(line):
            # debug(player)
            if symbol == 'O':
                field_coords.append((x, y))
            if symbol == 'X':
                field_coords_enemy.append((x, y))
    if player != 1:
        field_coords, field_coords_enemy = field_coords_enemy, field_coords
    return figure_coords, field_coords, field_coords_enemy

def parse_move(figure_coords, field_coords, size, size_f, player, field_enemy):
    if field_coords == []:
        return None
    # if player == 1:
    x, y = field_coords[0][0], field_coords[0][1]
    # else:
        # x, y = field_coords[-1][0], field_coords[-1][1]
    dx = x-figure_coords[0][0]
    dy = y - figure_coords[0][1]
    for coord in figure_coords:
        if coord != figure_coords[0]:
            if (coord[0] + dx, coord[1]+dy) in field_coords + field_enemy:
                field_coords.remove((x, y))
                return parse_move(figure_coords, field_coords, size, size_f, player, field_enemy)
    if dx+size_f[1] > size[0]-1 or dy+size_f[0] > size[1]-1 or dx < 0 or dy < 0:
        field_coords.remove((x, y))
        return parse_move(figure_coords, field_coords, size, size_f, player, field_enemy)
    return [dy, dx]

"""TO DO"""
#___________________________________________________________
#Input funcs
#___________________________________________________________
def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    l = l.replace(':', '').split(' ')
    l = [int(l[-2]), int(l[-1])]
    debug(f"Description of the field: {l}")
    return l


def parse_field(player: int, size:list):
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
    move = None
    res = []
    for i in range(size[0]+1):
        l = input()
        if i != 0:
            l = l.split()[1]
            res.append([i for i in l])
        debug(f"Field: {l}")
        if move is None:
            c = l.lower().find("o" if player == 1 else "x")
            if c != -1:
                move = i - 1, c - 4
    # debug(res)
    assert move is not None
    return move, res


def parse_figure():
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    result = []
    l = input()
    debug(f"Piece: {l}")
    height = int(l.split()[1])
    width = int(l.replace(':', '').split()[-1])
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")
        result.append([i for i in l])
    # debug(result)
    return result, [height, width]


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    size = parse_field_info()
    move, field = parse_field(player, size)
    figure, size_f = parse_figure()
    # debug(figure)
    figure_coords, field_coords, field_coords_enemy = coords(figure, field, player)
    move = parse_move(figure_coords, field_coords, size, size_f, player, field_coords_enemy)
    return move


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
