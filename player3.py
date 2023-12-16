import random

def parse_field_info():
    entered_data = input()
    entered_data = entered_data.replace('Plateau', '').replace(':', '')
    entered_data = entered_data.strip().split(' ')
    return entered_data

def parse_field(player: int):
    board = []
    board_data = parse_field_info()
    length = int(board_data[0])
    for _ in range(length + 1):
        entered_data = input()
        board.append([j for j in entered_data[4:]])
        figure = ('O' if player == 1 else 'X')
    return board, figure

def parse_figure():
    piece = []
    entered_data = input()
    height = int(entered_data.split()[1])
    for _ in range(height):
        entered_data = input()
        piece.append([j for j in entered_data])
    return piece

def distance_to_opponent(board, row, col, opponent_figure):
    distances = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == opponent_figure:
                distances.append(abs(row - i) + abs(col - j))
    return min(distances) if distances else float('inf')

def can_block_opponent(board, piece, row, col, player):
    opponent_figure = 'X' if player == 1 else 'O'
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == '*' and 0 <= row + i < len(board) and 0 <= col + j < len(board[row]):
                if board[row + i][col + j] == opponent_figure:
                    return True
    return False

def evaluate_move(board, piece, row, col, player):
    if can_block_opponent(board, piece, row, col, player):
        block_priority = 0.9
    else:
        block_priority = 0.0
    score = random.uniform(0, 1) + block_priority
    return score

def find_best_placement(board, piece):
    best_placement = None
    max_surrounding_cells = -1
    for i in range(len(board)):
        for k in range(len(board[i])):
            if board[i][k] == '.':
                surrounding_cells = count_surrounding_cells(board, piece, i, k)
                if surrounding_cells > max_surrounding_cells:
                    max_surrounding_cells = surrounding_cells
                    best_placement = (i, k)
    return best_placement

def count_surrounding_cells(board, piece, row, col):
    count = 0
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == '*' and 0 <= row + i < len(board) and 0 <= col + j < len(board[row]):
                count += 1 if board[row + i][col + j] == '.' else 0
    return count

def step(player: int):
    board, figure = parse_field(player)
    board.pop(0)
    piece = parse_figure()
    result = []

    opponent_figure = 'X' if player == 1 else 'O'

    # Switch algorithm if the map is smaller than 20x20
    if len(board) < 20 and len(board[0]) < 20:
        return find_best_placement(board, piece)

    if all('.' not in row for row in board):
        best_placement = find_best_placement(board, piece)
        return best_placement

    elif len(board) < 20 and len(board[0]) < 20:
        for i in range(len(board) - len(piece) + 1):
            for k in range(len(board[i]) - len(piece[0]) + 1):
                score = evaluate_move(board, piece, i, k, player)
                result.append((i, k, score))

        result.sort(key=lambda x: x[2], reverse=True)
        if result:
            return result[0][:2]

    elif distance_to_opponent(board, 0, 0, opponent_figure) <= 3:
        for i in range(len(board) - len(piece) + 1):
            for k in range(len(board[i]) - len(piece[0]) + 1):
                score = evaluate_move(board, piece, i, k, player)
                result.append((i, k, score))

        result.sort(key=lambda x: x[2], reverse=True)
        if result:
            return result[0][:2]

    else:
        for i in range(len(board) - len(piece) + 1):
            for k in range(len(board[i]) - len(piece[0]) + 1):
                num = 0
                opponent_moves = 0
                surrounding_opponent_cells = 0
                for item in range(len(piece)):
                    for el in range(len(piece[0])):
                        if piece[item][el] == '*':
                            if board[i + item][k + el] == figure:
                                num += 1
                            elif board[i + item][k + el] != '.':
                                num += 3
                            if board[i + item][k + el] == opponent_figure:
                                opponent_moves += 2

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
    while True:
        move = step(player)
        print(*move)

def parse_info_about_player():
    i = input()
    return 1 if "p1 :" in i else 2

def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        print("Cannot get input. Seems that we've lost ):(")

if __name__ == "__main__":
    main()