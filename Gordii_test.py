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


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input().replace(':','')
    size = l.split()
    # debug(f'{size}')
    debug(f"Description of the field: {int(size[1]), int(size[2])}")
    return int(size[1]), int(size[2])

def parse_field(player: int, map_size:tuple):
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
    _=input()
    for _ in range(map_size[0]):
        l = input()
        debug(f"Field: {l}")
        field.append(l[3:])
        # debug(f'{l[3:]}')
    return field

def all_move_algorithm(player:int, parsed_field:dict, parsed_figure: list, endgame = False):
    '''
    Top left corner
    '''
    par = 'O' if player == 1 else 'X'

    possible_coords = []

    for i in range(len(parsed_field)-len(parsed_figure)+1):
        for j in range(len(parsed_field[0])-len(parsed_figure[0])+1):
            counts = 0
            par_counts = 0
            dot_counts = 0
            height = len(parsed_figure)
            for k in range(height):
                width = len(parsed_figure[0])
                for m in range(width):
                    if parsed_figure[k][m] == '*':
                        if parsed_field[i+k][j+m] == par:
                            par_counts+=1
                        elif parsed_field[i+k][j+m] != '.':
                            counts+=1
                    # else:
                    #     if parsed_field[i+k][j+m] == par:
                    #         dot_counts+=1

            if counts == 0 and par_counts==1:
                if (len(parsed_field)-1)>=i>=0 and (len(parsed_field[0])-1)>=j-1>=0:
                    possible_coords.append((i,j-1))
            # OPTIONAL AND CAN BE USED IN THE ENDGAME
            # elif endgame:
            #     if dot_counts>=1 and counts == 0:
            #         if (len(parsed_field)-1)>=i>=0 and (len(parsed_field[0])-1)>=j-1>=0:
            #             possible_coords.append((i,j))


    debug(f"possible coordes: {possible_coords}")
    return possible_coords

def choosing_move(player, field, map_size, all_moves):
    '''
    
    '''
    # def closest_move(my_coord, enemy_coord):
    #     # y = map_size[0]/2
    #     # x = map_size[1]/2
    #     move = None
    #     close_list = []
    #     debug(f'all move:{all_moves}')
    #     if all_moves:
    #         for i in all_moves:
    #             distance = ((abs(my_coord[0]-enemy_coord[0]))**2 + (abs(my_coord[1]-enemy_coord[1]))**2)**(1/2)
    #             close_list.append(distance)
    #         move = all_moves[close_list.index(min(close_list))]
    #     return move
    # debug(f'{move}')
    move = None
    my_pl = 'O' if player ==1 else 'X'
    enemy = 'X' if player ==1 else 'O'

    enemy_coords = []
    my_coords = []

    height = len(field)
    width = len(field[0])

    for i in range(height):
        for j in range(width):
            if field[i][j] == enemy:
                enemy_coords.append((i,j))
            if field[i][j] == my_pl:
                my_coords.append((i,j))

    # for i in enemy_coords:
    #     close_list = []
    #     for j in my_coords:
    #         distance = ((abs(i[0]-j[0]))**2 + (abs(i[1]-j[1]))**2)**(1/2)
    #         close_list.append(distance)
    #     move = all_moves[close_list.index(min(close_list))]

    min_ = []

    for i in all_moves:
        close_list = []
        # debug(f'all move:{all_moves}')
        if all_moves:
            for j in enemy_coords:
                distance = ((abs(j[0]-i[0]))**2 + (abs(j[1]-i[1]))**2)**(1/2)
                close_list.append(distance)
            move_dist = min(close_list)
            min_.append(move_dist)
    if min_:
        move = all_moves[min_.index(min(min_))]
    # if all_moves:
    #     move = random.choice(all_moves)
    # debug(f'move:{min_}')
    assert move is not None

    return move

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
    parse_fig = []
    l = input()
    debug(f"Piece: {l}")
    height = int(l.split()[1])
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")
        parse_fig.append(l)
    debug(f'{parse_fig}')
    return parse_fig

def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    map_size = parse_field_info()
    parsed_field = parse_field(player, map_size)
    parsed_fig = parse_figure()
    all_moves = all_move_algorithm(player, parsed_field, parsed_fig, True)
    move = choosing_move(player, parsed_field, map_size, all_moves)
    return move

def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        debug(f'{move}')
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