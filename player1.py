#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""
import copy
import random
from logging import DEBUG, debug, getLogger

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
def choose_best(result, used_coords, size, one_coord):
    lst = []
    for x in range(size[1]-1, size[1]+2):
        for y in range(size[0]-1, size[0]+2):
            lst.append((y, x))
    debug(lst)
    count = 0
    for i in lst:
        if i in used_coords:
            count += 1
    if count <=2:
        res_count_y = 0
        counter = 0
        for j in one_coord:
            res_count_y += j[0]
            counter+=1
        res_count_y = res_count_y/counter
        if res_count_y < size[0]/2:
            result = sorted(result, key=lambda x: (x[0]+size[0])/2 + (x[1] + size[1])/2, reverse=True)
        elif res_count_y > size[0]/2:
            result = sorted(result, key=lambda x: (x[0]+size[0])/2 + (x[1] + size[1])/2)
        return result[0]
    else:
        if random.randint(1,3) == 1:
            result = sorted(result, key=lambda x: x[1])
        else:
            result = sorted(result, key=lambda x: x[0])
        return result[0]
def coords(field, figure, player):
    X_coords = []
    O_coords = []
    star_coords = []
    for y_f, line_f in enumerate(figure):
        for x_f, symbol_f in enumerate(line_f):
            if symbol_f == '*':
                star_coords.append((y_f, x_f))
    for y, line in enumerate(field):
        for x, symbol in enumerate(line):
            if symbol == 'O':
                O_coords.append((y, x))
            elif symbol == 'X':
                X_coords.append((y, x))
    if player == 1:
        return O_coords, X_coords, star_coords
    elif player == 2:
        return X_coords, O_coords, star_coords

def check_avialable(placed_coord, to_be_placed, unavilable_coords, figure_coords, size, size_f):
    dy, dx = placed_coord[0]-to_be_placed[0], placed_coord[1]-to_be_placed[1]
    if (dy+size_f[0] > size[0]) or (dx+size_f[1] > size[1]) or dy < 0 or dx < 0:
        return None
    for coord in figure_coords:
        if coord != to_be_placed:
            if (coord[0]+dy, coord[1]+dx) in unavilable_coords:
                return None
    # debug(f'{dy+size_f[0]} > {size[0]-1}')
    # debug(f'{dx+size_f[1]} > {size[1]-1}')
    return [dy, dx]

def decision(player_coords: list, enemy_coords: list, figure_coords: list, player_coords_copy: list, size: list, size_f) -> list:
    result = []
    for placed_coord in player_coords_copy:
        for to_be_placed in figure_coords:
            result.append(check_avialable(placed_coord, to_be_placed, player_coords+enemy_coords, figure_coords, size, size_f))
    result = [k for k in result if k is not None]
    # debug(f'possible = {result}')
    try:
        # debug(f'{choose_best(result, player_coords+enemy_coords, size, figure_coords[0])}')
        return choose_best(result, player_coords+enemy_coords, size, player_coords)
    except ValueError:
        return [0, 0]
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
    # debug(f"Description of the field: {l}")
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
    # move = None
    res = []
    for i in range(size[0]+1):
        l = input()
        if i != 0:
            l = l.split()[1]
            res.append([i for i in l])
        # debug(f"Field: {l}")
    # debug(res)
    # assert move is not None
    return res


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
    size = [int(l.replace(':','').split()[1]),int(l.replace(':','').split()[2])]
    # debug(f'size = {size}')
    height = int(l.split()[1])
    for _ in range(height):
        l = input()
        # debug(f"Piece: {l}")
        result.append([i for i in l])
    # debug(result)
    return result, size


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    size = parse_field_info()
    field = parse_field(player, size)
    figure, size_f = parse_figure()
    player_coords, enemy_coords, figure_coords = coords(field, figure, player)
    move = decision(player_coords, enemy_coords, figure_coords, copy.deepcopy(player_coords), size, size_f)
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
