#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
import random
import copy
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
    l = l.split()
    # debug(f"Description of the field: {int(l[1]),int(l[2])}")
    return (int(l[1]),int(l[2]))

def parse_field(size: tuple):
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
    _=input()
    lines=[]
    for _ in range(size[0]):
        line=input().split()
        # debug(f"Field: {line}")
        row=[]
        for i in range(size[1]):
            row.append(line[1][i])
        lines.append(row)
    return lines
    # for i in range(16):
    #     l = input()
    #     debug(f"Field: {l}")
    #     if move is None:
    #         c = l.lower().find("o" if player == 1 else "x")
    #         if c != -1:
    #             move = i - 1, c - 4
    # assert move is not None
    # return move


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
    
    l = input().replace(':','')
    
    l = l.split()
    lines=[]
    for _ in range(int(l[1])):
        line=input()
        # debug(f'llllll {line}')
        row=[]
        for i in range(int(l[2])):
            row.append(line[i])
        lines.append(row)
    # debug(f"Piece1111111111: {lines}")
    return lines

    # height = int(l[1])
    # for _ in range(height):
    #     l = input()
    #     debug(f"Piece: {l}")
    # return lines
def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    info=parse_field_info()
    field =parse_field(info)

    figure=parse_figure()
    # debug(f"Piece1111111111: {field}")

    count=0
    l=[]
    for x, line in enumerate(field):
        for y, _ in enumerate(line):

            for x1, line1 in enumerate(figure):
                for y1, _ in enumerate(line1):
                    try:
                        if player == 1 and field[x+x1][y+y1].lower()=='o' and figure[x1][y1] == '*':
                            count+=1
                        if player == 1 and field[x+x1][y+y1].lower()=='x':
                            count-=200
                        if player == 2 and field[x+x1][y+y1].lower()=='x' and figure[x1][y1] == '*':
                            count+=1
                        if player == 2 and field[x+x1][y+y1].lower()=='o':
                            count-=200
                    except IndexError:
                        count+=2
            if count==1:
                l.append((x,y))
            count=0
    min_1=10000
    to_app=(0,0)
    for x,m in enumerate(field):
        for y,k in enumerate(m):
            if k == 'O' and player==2:
                for x1,y1 in l:
                    leng=0
                    for x_f, line1 in enumerate(figure):
                        for y_f, _ in enumerate(line1):
                            a=(((x1+x_f)-x)**2+((y1+y_f)-y)**2)**0.5
                            leng+=a
                    if leng<min_1 and leng>20:
                        min_1 = leng
                        to_app = (x1,y1)
            if k == 'X' and player==1:
                for x1,y1 in l:
                    leng=0
                    for x_f, line1 in enumerate(figure):
                        for y_f, _ in enumerate(line1):
                            a=(((x1+x_f)-x)**2+((y1+y_f)-y)**2)**0.5
                            leng+=a
                    if leng<min_1 and leng>20:
                        min_1 = leng
                        to_app = (x1,y1)
            # if k == 'O' and player==2:
            #     for x1,y1 in l:
            #         a=((x1-x)**2+(y1-y)**2)**0.5
            #         if a<min_1:
            #             min_1 = a
            #             to_app = (x1,y1)
            # if k == 'X' and player==1:
            #     for x1,y1 in l:
            #         a=((x1-x)**2+(y1-y)**2)**0.5
            #         if a<min_1:
            #             min_1 = a
            #             to_app = (x1,y1)
    # debug(f'llllll {l}')
    move = to_app
    # parse_field_info()
    # move = parse_field(player)
    # parse_figure()
    # debug(f"Info a: {move}")
    return move


def play(player: int):
    """
    Main game loop.
    # ruby ./filler_vm -f ./map01 -p1 'python ./player1.py' -p2 'python ./player1.py' | python visualizer.py
    :param player int: Represents whether we're the first or second player
    """
    m=0
    while True:
        m+=1
        move = step(player)
        print(*move)
        # debug(f"Info a: {m}")


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
        if player == 1:
            debug("Cannot get input. Seems that first player lost ):")
        else:
            debug("Cannot get input. Seems that second player lost ):")

if __name__ == "__main__":
    main()