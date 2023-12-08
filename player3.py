#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""
import random
from logging import DEBUG, debug, getLogger

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
    entered_data = input()
    entered_data = entered_data.replace('Plateau','').replace(':','')
    entered_data = entered_data.strip().split(' ')
    debug(f"Description of the field: {entered_data}")
    return entered_data

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
    board = []
    board_data = parse_field_info()
    length = int(board_data[0])
    for _ in range(length+1):
        entered_data = input()
        debug(f"Field: {board_data}")
        board.append([j for j in entered_data[4::]])
        figure = ('O' if player == 1 else 'X')
    return board,figure

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
    entered_data = input()
    debug(f"Piece: {entered_data}")
    height = int(entered_data.split()[1])
    for _ in range(height):
        entered_data = input()
        piece.append([j for j in entered_data])
        debug(f"Piece: {entered_data}")
    return piece

def distance_to_opponent(board, row, col, opponent_figure):
    """
    Calculate the Manhattan distance from the specified position to the closest opponent's figure.
    """
    distances = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == opponent_figure:
                distances.append(abs(row - i) + abs(col - j))
    return min(distances) if distances else float('inf')

def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    board, figure = parse_field(player)
    board.pop(0)
    piece = parse_figure()
    result = []

    opponent_figure = 'X' if player == 1 else 'O'
    for i in range(len(board) - len(piece) + 1):
        for k in range(len(board[i]) - len(piece[0]) + 1):
            num = 0
            opponent_moves = 0  # restriction
            surrounding_opponent_cells = 0  # new metric

            for item in range(len(piece)):
                for el in range(len(piece[0])):
                    if piece[item][el] == '*':
                        if board[i + item][k + el] == figure:
                            num += 1
                        elif board[i + item][k + el] != '.':
                            num += 3
                        # opponent restriction
                        if board[i + item][k + el] == opponent_figure:
                            opponent_moves += 2

                        # Check if the move surrounds opponent's figure
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                ni, nk = i + item + x, k + el + y
                                if 0 <= ni < len(board) and 0 <= nk < len(board[i]) and board[ni][nk] == opponent_figure:
                                    surrounding_opponent_cells += 1

            if num == 1:
                result.append((i, k, opponent_moves + surrounding_opponent_cells))

    result.sort(key=lambda x: (
        distance_to_opponent(board, x[0], x[1], opponent_figure),
        -min(x[0], len(board) - x[0], x[1], len(board[0]) - x[1])
    ))

    result.sort(key=lambda x: x[2], reverse=True) 

    if result:
        return result[0][:2]

    return random.choice(result) if result else None





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