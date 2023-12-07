#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
import random

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)

def main():
    """
    The main function of the bot.
    """
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")

def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2

def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)

def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    # field, figure = parse_field(player)
    # field.pop(0)
    # piece = parse_figure()
    # all_possible_coordinates = all_possible_coor(player, field, piece, figure)
    # my_ter = [[y, x] for y in range(len(field)) for x in range(len(field[y])) if field[y][x].upper() == figure]
    # model_of_play = None
    # if any(x == ((len(field)//2)-4 or (len(field)//2)+4) and y == ((len(field[0])//2)-4, (len(field[0])//2)+4) for k in my_ter for x, y in k):
    #     model_of_play = "clews"
    # else:
    #     model_of_play = "move"
    # if model_of_play == "move":
    #     return all_possible_coordinates[0]
    # else:
    #     return random.choice(all_possible_coordinates)
    field, figure = parse_field(player)
    field.pop(0)
    piece = parse_figure()
    all_possible_coordinates = all_possible_coor(player, field, piece, figure)
    my_ter = [[y, x] for y in range(len(field)) for x in range(len(field[y])) if field[y][x].upper() == figure]
    model_of_play = None
    center_coords = (len(field) // 2, len(field[0]) // 2)
    target_coords = ((center_coords[0] - 4, center_coords[1]), (center_coords[0] + 4, center_coords[1]),
                    (center_coords[0], center_coords[1] - 4), (center_coords[0], center_coords[1] + 4))
    if any(coord in target_coords for coord in my_ter):
        model_of_play = "clews"
    else:
        model_of_play = "move"

    if model_of_play == "move":
        return all_possible_coordinates[0] if all_possible_coordinates else None
    else:
        return random.choice(all_possible_coordinates) if all_possible_coordinates else None



def move(field, player, all_possible_coordinates):
    if player == 1:
        return sorted(all_possible_coordinates, key=lambda x:(x[0], x[1]))[-1]
    else:
        return sorted(all_possible_coordinates, key=lambda x:(x[0], x[1]))[0]



def all_possible_coor(player, field, piece, figure):
    result = []
    for i in range(len(field) - len(piece) + 1):
        for k in range(len(field[i]) - len(piece[0]) + 1):
            num = 0
            for item in range(len(piece)):
                for el in range(len(piece[0])):
                    if piece[item][el] == '*':
                        if field[i + item][k + el] == figure:
                            num += 1
                        elif field[i + item][k + el] != '.':
                            num += 2
            if num == 1:
                result.append([i, k])
    return result




def parse_field(player: int):
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
    field = []
    length_of_field = parse_field_info()
    length = int(length_of_field[0])
    for i in range(length + 1):
        l = input()
        debug(f"Field: {l}")
        field.append([j for j in l [4::]])
        figure = ("O" if player == 1 else "X")
    return field, figure


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    l = l.replace(":","").replace("Plateau", "").strip()
    l = l.split(" ")
    debug(f"Description of the field: {l}")
    return l




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
    piece = []
    l = input()
    debug(f"Piece: {l}")
    height = int(l.split()[1])
    for _ in range(height):
        l = input()
        piece.append([j for j in l])
        debug(f"Piece: {l}")
    return piece









if __name__ == "__main__":
    main()
