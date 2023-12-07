from logging import DEBUG, debug, getLogger

getLogger().setLevel(DEBUG)


def parse_info_about_player():
    i = input()
    debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def parse_field_info():
    l = input()
    debug(f"Description of the field: {l}")


def parse_field(player: int):
    move = None
    for i in range(16):
        l = input()
        debug(f"Field: {l}")
        if move is None:
            c = l.lower().find("o" if player == 1 else "x")
            if c != -1:
                move = i - 1, c - 4
    assert move is not None
    return move


def parse_figure():
    l = input()
    debug(f"Piece: {l}")
    height = int(l.split()[1])
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")


def place_piece(board, piece, row, col):
    for i in range(piece[1]):
        for j in range(piece[0]):
            if piece[2 + i][j] != '.':
                board[row + i][col + j] = piece[2 + i][j]


def is_valid_move(board, piece, row, col):
    for i in range(piece[1]):
        for j in range(piece[0]):
            if (
                row + i >= len(board) or col + j >= len(board[0]) or
                board[row + i][col + j] != '.' or
                piece[2 + i][j] == '.'
            ):
                return False
    return True


def count_player_cells(board, player):
    return sum(row.count(player) for row in board)


def play_game(bot_as_player):
    player = 1 if bot_as_player == 'first' else 2
    parse_field_info()

    # Assuming you know the initial dimensions of the board
    width, height = 17, 15
    board = [['.' for _ in range(width)] for _ in range(height)]

    while True:
        move = None
        parse_field(player)
        parse_figure()

        piece_width, piece_height = 3, 2  # Replace with actual piece dimensions
        piece = (piece_width, piece_height, [])

        for _ in range(piece_height):
            row = input()
            piece[2].append(row)

        if player == 1:
            # Bot strategy for Player 1: Place piece at the top-left corner
            for i in range(height):
                for j in range(width):
                    if is_valid_move(board, piece, i, j):
                        move = (i, j)
                        break
                if move:
                    break
        else:
            # Bot strategy for Player 2: Place piece at the bottom-right corner
            for i in range(height - 1, -1, -1):
                for j in range(width - 1, -1, -1):
                    if is_valid_move(board, piece, i, j):
                        move = (i, j)
                        break
                if move:
                    break

        if not move:
            print(f"Player {player} loses!")
            break

        place_piece(board, piece, move[0], move[1])
        player_cells = count_player_cells(board, 'O' if player == 1 else 'X')
        print(f"Player {player} placed a piece at: {move}")
        print(f"Player {player} current score: {player_cells}")

        player = 3 - player  # Switch player


if __name__ == "__main__":
    bot_position = input("Enter 'first' if the bot should play as Player 1, 'second' otherwise: ")
    play_game(bot_position.lower())