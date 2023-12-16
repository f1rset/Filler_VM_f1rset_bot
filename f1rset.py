#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importing copy, random and math to calculate and choose best options
and also importing Debug and getlogger from logging
"""
import copy
import random
import math
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
def find_closest(result: list, enemy_pos: list, figure_mid: tuple) -> list:
    """Function searches for closest position of figure to enemy

    Args:
        result (list): all possible coords
        enemy_pos (list): all enemy coords
        figure_mid (tuple): max y and x of figure divided by 2

    Returns:
        tuple: chosed coordinates
    """
    distances = {}
    for x in result:
        coords_1 = (figure_mid[0]+x[0], figure_mid[1]+x[1])
        for i in enemy_pos:
            distances[math.sqrt((coords_1[0]-i[0])**2 + (coords_1[1]-i[1])**2)] = x

    return distances[min(distances.keys())]

def choose_best(result: list,
                used_coords: list,
                size: list,
                one_coord: list,
                enemy_pos: list,
                size_f: list) -> list:
    """Function returns choosed best coord

    Args:
        result (list): all possible coords
        used_coords (list): coords on map that are already used
        size (list): size of the map
        one_coord (tuple): coordinates of one player
        enemy_pos (list): coordinates of all enemy positions
        size_f (list): size of the figure

    Returns:
        list: coordinates to be placed
    """
    if size[0] + size[1] > 130:
        if len(used_coords)-len(enemy_pos) - 100 > len(enemy_pos):
            result = sorted(result, key=lambda x: (x[0]+x[1]), reverse=True)
            return result[0]
        if len(used_coords) - len(enemy_pos) < 300:
            res_count_y: float = 0
            counter = 0
            for j in one_coord:
                res_count_y += j[0]
                counter+=1
            res_count_y = res_count_y/counter
            if res_count_y < size[0]/2:
                if random.randint(0,1):
                    result = sorted(result, key=lambda x: x[0], reverse=True)
                else:
                    result = sorted(result, key=lambda x: x[1], reverse=True)
            elif res_count_y > size[0]/2:
                if random.randint(0,1):
                    result = sorted(result, key=lambda x: x[0])
                else:
                    result = sorted(result, key=lambda x: x[1])
            try:
                return result[0]
            except IndexError:
                return [0, 0]
        else:
            figure_mid = (size_f[0]//2, size_f[1]//2)
            return find_closest(result, enemy_pos, figure_mid)
    if (size[0]+ size[1] < 130) and (size[0]+ size[1] > 40): # algorithm for middle map
        if size[0]+10< size[1] or size[0]+10< size[1]: # if map size is not identical
            if len(used_coords)-len(enemy_pos) - 80 > len(enemy_pos):
                result = sorted(result, key=lambda x: (x[0]+x[1]), reverse=True)
                return result[0]
            if len(used_coords) - len(enemy_pos) < 100:
                res_count_y = 0
                counter = 0
                for j in one_coord:
                    res_count_y += j[0]
                    counter+=1
                res_count_y = res_count_y/counter
                if res_count_y < size[0]/2:
                    result = sorted(result, key=lambda x: x[1]+x[0]/2, reverse=True)
                elif res_count_y > size[0]/2:
                    result = sorted(result, key=lambda x: x[0]+x[1])
                try:
                    return result[0]
                except IndexError:
                    return [0, 0]
            else:
                figure_mid = (size_f[0]//2, size_f[1]//2)
                return find_closest(result, enemy_pos, figure_mid)
        else:
            if len(used_coords)-len(enemy_pos) - 80 > len(enemy_pos):
                result = sorted(result, key=lambda x: (x[0]+x[1]), reverse=True)
                try:
                    return result[0]
                except IndexError:
                    return [0, 0]
            if len(used_coords) - len(enemy_pos) < 200:
                res_count_y = 0
                counter = 0
                for j in one_coord:
                    res_count_y += j[0]
                    counter+=1
                res_count_y = res_count_y/counter
                if res_count_y < size[0]/2:
                    result = sorted(result, key=lambda x: x[1]+x[0]/2, reverse=True)
                elif res_count_y > size[0]/2:
                    if len(used_coords) - len(enemy_pos) < 40:
                        result = sorted(result, key=lambda x: x[0])
                    else:
                        result = sorted(result, key=lambda x: x[0]+x[1])
                try:
                    return result[0]
                except IndexError:
                    return [0, 0]
            else:
                figure_mid = (size_f[0]//2, size_f[1]//2)
                return find_closest(result, enemy_pos, figure_mid)
    else: # algorithm for minimal map
        figure_mid = (size_f[0]//2, size_f[1]//2)
        return find_closest(result, enemy_pos, figure_mid)

def coords(field: list, figure: list, player: int):
    """Function searches for every coord of field and figure

    Args:
        field (list): list interpertation of map
        figure (list): list interpertation of figure
        player (int): player

    Returns:
        list: coordinates of player
        list: coordinates of enemy 
        list: coordinates of figure
    """
    x_coords = []
    o_coords = []
    star_coords = []
    for y_f, line_f in enumerate(figure):
        for x_f, symbol_f in enumerate(line_f):
            if symbol_f == '*':
                star_coords.append((y_f, x_f))
    for y, line in enumerate(field):
        for x, symbol in enumerate(line):
            if symbol == 'O':
                o_coords.append((y, x))
            elif symbol == 'X':
                x_coords.append((y, x))
    if player == 1:
        return o_coords, x_coords, star_coords
    if player == 2:
        return x_coords, o_coords, star_coords
    return None

def check_avialable(placed_coord: list,
                    to_be_placed: list,
                    unavilable_coords: list,
                    figure_coords: list,
                    size: list,
                    size_f: list):
    """Checks if coord is available to place figure

    Args:
        placed_coord (list): coord on the field
        to_be_placed (list): coord of star in figure
        unavilable_coords (list): coords on the field that are already used
        figure_coords (list): coords of every star in figure
        size (list): size of field
        size_f (list): size of figure

    Returns:
        list or None: available coord
    """
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

def decision(player_coords: list,
             enemy_coords: list,
             figure_coords: list,
             player_coords_copy: list,
             size: list,
             size_f: list) -> list:
    """Function starts all other functions of decision and gives only correct coord

    Args:
        player_coords (list): coords of player
        enemy_coords (list): coords of enemy
        figure_coords (list): coords of stars in figure
        player_coords_copy (list): copy of player coords
        size (list): size of field
        size_f (list): size of figure

    Returns:
        list: coordinate
    """
    result = []
    for placed_coord in player_coords_copy:
        for to_be_placed in figure_coords:
            result.append(check_avialable(placed_coord, to_be_placed, \
player_coords+enemy_coords, figure_coords, size, size_f))
    result = [k for k in result if k is not None]
    # debug(f'possible = {result}')
    try:
        # debug(f'{choose_best(result, player_coords+enemy_coords, size, figure_coords[0])}')
        return choose_best(result, player_coords+enemy_coords, \
size, player_coords, enemy_coords, size_f)
    except ValueError:
        return [0, 0]
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


def parse_field(size:list):
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
    field = parse_field(size)
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
        try:
            move = step(player)
            print(*move)
        except TypeError:
            print(*(0,0))


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
    """
    Main function of program
    """
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
