#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
from math import sqrt

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = [k.replace(':','') for k in input().split()[-2:]]
    debug(f"Description of the field: {l}")
    return l


def parse_field(size: list[str]) -> list[list]:
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
    height = int(size[0])
    field = []
    _ = input()
    for _ in range(height):
        l = input()
        # debug(f"LINE!!!!!!!!!: {l.strip().split()}")
        field.append(list(l.strip().split()[1]))
        debug(f"Field: {l}")
    # assert move is not None
    return field


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
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")
        result.append(list(l.strip()))
    return result


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    size = parse_field_info()
    field = parse_field(size)
    if player == 1:
        player_symbol = 'O'
    else:
        player_symbol = 'X'
    figure = parse_figure()

    move = choose_best(find_possible(figure, field, player_symbol), field, player_symbol)
    debug(f"COORDINATES: {move}") #mod
    return move # return type - tuple of coordinates


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        try:
            move = step(player)
            print(*move)
        except IndexError:
            print(None)


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
    '''
    Main function
    '''
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


def find_possible(figure: list[list], field: list[list], player_sign: str) -> list[tuple]:
    '''
    Returns all possible positions for placing the figure.
    Example figure:

    .....
    ..**.
    ..*..
    ..**.
    .....

    Example field:
    .............................
    .............................
    .......................O.....
    .............................
    .............................
    .............................
    .............................
    .............................
    ...x.........................
    .............................

    '''
    # calculating last possible position by length
    x_last = len(field[0]) - len(figure[0]) + 1
    y_last = len(field) - len(figure) + 1

    # creating list of possible positions coord-s
    possible = []

    # iterating over all possible by size coord-s and checking them
    y_current_pos = 0

    while y_current_pos < y_last:
        x_current_pos = 0
        while x_current_pos < x_last:
            if check_for_placability(figure, field, x_current_pos, y_current_pos, player_sign):
                possible.append((y_current_pos, x_current_pos))
            x_current_pos += 1
        y_current_pos += 1

    return possible


def check_for_placability(figure: list[list], field: list[list], x_coord: int, \
                          y_coord: int, player_sign: str) -> bool:
    '''
    Checks whether it is possible to place
    figure in given coordinates.
    '''
    # Extracting field indexes for stars
    star_coords_glob = {(pos_y + y_coord, pos_x + x_coord) for pos_y, line in enumerate(figure)
                        for pos_x, char in enumerate(line) if char == '*'}

    # Check whether it is possible to place figure on that coord-s by intersection with your symbols
    player_sign_glob = {(pos_y, pos_x) for pos_y, line in enumerate(field)
                        for pos_x, char in enumerate(line) if char == player_sign}
    if len(star_coords_glob.intersection(player_sign_glob)) != 1:
        return False

    # Check whether it is possible to place figure on that c-s by intersection with enemy's symbols
    enemy_sign_glob = {(pos_y, pos_x) for pos_y, line in enumerate(field)
                       for pos_x, char in enumerate(line) if char not in [player_sign, '.']}
    if len(star_coords_glob.intersection(enemy_sign_glob)) >= 1:
        return False

    return True


def choose_best(possible_options: list[tuple], field: list[list], player_sign: str) -> tuple:
    '''
    Returns the best option to place figure.
    '''
    def get_distance(placing_pos: tuple[int], enemies_pos: tuple[int]) -> float:
        '''
        Returns distance from placing_pos
        to enemies_pos as a float value.
        '''
        return sqrt((enemies_pos[0] - placing_pos[0])**2 + (enemies_pos[1] - placing_pos[1])**2)

    enemies = [(pos_y, pos_x) for pos_y, line in enumerate(field)
                       for pos_x, char in enumerate(line) if char not in [player_sign, '.']]

    possible_with_dist = sorted([(point_, min(get_distance(point_, enemy) for enemy in enemies)) \
                                 for point_ in possible_options], key=lambda x: x[1])
    return possible_with_dist[0][0]


if __name__ == "__main__":
    main()
